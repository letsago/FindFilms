from server.database import db_session, Base, engine
from server.models import Movie, Theater, Showing, Genre, Cast, Director
from RT_scraper import RTMovie
from AMCShowingInfo_scraper import AMCShowingInfo
from AMCShowingUrls_scraper import AMCShowingUrls
from AMCTheaters_scraper import AMCTheaters
from AMCUrls_scraper import AMCUrls
import datetime
import requests
import time
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial
import threading

lock = threading.Lock()
target_states = {   
                    'Alabama', 'Arizona', 'Arkansas', 'California', 'Colorado', 
                    'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 
                    'Georgia', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 
                    'Kentucky', 'Louisiana', 'Maryland', 'Massachusetts', 'Michigan', 
                    'Minnesota', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 
                    'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina',
                    'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania',  
                    'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah',
                    'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
                }

def get_RT_url(movie_title):
    # RT url format is 'https://www.rottentomatoes.com/m/movie_name*_release_year*'
    # note release year is only necessary for movies with same names
    # priority checking valid, unique RT urls for same name movies released in 2019, then in 2018, then with no year stamp 
    movie_url_id = movie_title.lower().translate(None, '.!?:').replace(' ', '_').replace('-', '_')
    year_increments = 1
    year_url_ids = ['_%d' % (datetime.datetime.today().year - i) for i in range(year_increments)]
    year_url_ids.append('')
    for year_url_id in year_url_ids:
        RT_url = 'https://www.rottentomatoes.com/m/%s%s' % (movie_url_id, year_url_id)
        response = requests.get(RT_url)
        if response.status_code == 200:
            return RT_url
    return None

def commit_theater_info(theater_url):
    theater_info = AMCTheaters(theater_url).get_theater_info()
    if theater_info != None:
        theater_db = Theater(theater_info['url'], theater_info['name'], theater_info['street'], theater_info['city'], theater_info['state'], theater_info['zipCode'])
        print "Committing %s info" % (theater_db.name)
        db_session.add(theater_db)
        db_session.commit()

def commit_all_theaters():
    AMC_theater_urls = AMCUrls().get_theater_urls()
    pool = ThreadPool(12)
    pool.map(commit_theater_info, AMC_theater_urls)
    pool.close()
    pool.join()

def get_or_create_movie_data(RT_url, movie_title):
    # gets movie from database if exists, otherwise commits new movie to database and returns it
    movie_db = Movie.query.filter(Movie.RT_url == RT_url).first()
    if movie_db == None:
        movie = RTMovie(RT_url)
        movie_general_info = movie.get_general_info()
        movie_db = Movie(RT_url, 
                        # add actual imdb_url later
                        None, 
                        movie_title, 
                        movie_general_info['rating'],
                        movie_general_info['length'],
                        movie.get_img(),
                        # add actual imdb_score later
                        None,
                        movie.get_RT_score(),
                        movie.get_synopsis())
        db_session.add(movie_db)
        db_session.commit()

        for genre in movie_general_info['genre']:
            db_session.add(Genre(movie_db.id, genre))
        for cast in movie.get_cast():
            db_session.add(Cast(movie_db.id, cast))
        for director in movie_general_info['director']:
            db_session.add(Director(movie_db.id, director))
        db_session.commit()
    return movie_db

def commit_showing_info(showing_url, theater_db):
    showing_info = AMCShowingInfo(showing_url).get_showing_info()
    # will not commit to database if showing info section is not found when scraping
    if showing_info != None:
        RT_url = get_RT_url(showing_info['movie'])
        if RT_url != None:
            with lock:
                movie_db = get_or_create_movie_data(RT_url, showing_info['movie'])
                for time in showing_info['times']:
                    print "Committing %s" % (showing_url)
                    db_session.add(Showing(movie_db.id, theater_db.id, showing_url, showing_info['date'], time))
                    db_session.commit()

def get_theater_showings(theater_db):
    if theater_db.state in target_states:
        AMC_showing_urls = AMCShowingUrls(theater_db.url).get_showing_urls()
        pool = ThreadPool(12)
        pool.map(partial(commit_showing_info, theater_db=theater_db), AMC_showing_urls)
        pool.close()
        pool.join()

def commit_all_showings(theaters):
    theater_processed_count = 0
    for theater_db in theaters:
        get_theater_showings(theater_db)
        theater_processed_count += 1
        # add static wait time after processing certain number of theaters to prevent timing out of AMC server while scraping
        if theater_processed_count % 25 == 0:
            time.sleep(90)

def update_prod_showings():
    # updates showings database and adds any new movies and related info to their appropriate databases using preexisting theater database info
    start = time.time()
    Showing.query.delete()
    db_session.commit()

    theaters = Theater.query.all()
    commit_all_showings(theaters)
    
    end = time.time()
    print 'Updating showings took %f seconds' % (end - start) 

def update_prod_theaters():
    start = time.time()
    Showing.query.delete()
    Theater.query.delete()
    db_session.commit()

    commit_all_theaters()

    end = time.time()
    print 'Updating theaters took %f seconds' % (end - start)

def init_prod_db():
    # performs a full initialization of the entire production database after deleting all tables
    # added Base back into this function otherwise can't reinitialize database after deleting db file due to schema changes
    Base.metadata.create_all(bind=engine)
    update_prod_theaters()
    Genre.query.delete()
    Cast.query.delete()
    Director.query.delete()
    Movie.query.delete()
    db_session.commit()
    update_prod_showings()
