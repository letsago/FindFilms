from server import app
from flask import render_template, request, redirect, url_for, abort
from server.models import Movie, Theater, Showing, Genre, Cast, Director
from sqlalchemy import and_
from server.database import db_session
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
import datetime
import json

def movieSearch(formData):
    constraints = []
    searchKeys = []
    for key, value in formData.items():
        if value != '':
            searchKeys.append(key)
    for key in searchKeys:
        if key == 'length' or key == 'imdb' or key == 'rottenTomatoes':
            try:
                if key == 'length':
                    constraints.append(getattr(Movie, key) <= float(formData[key]))
                else:
                    constraints.append(getattr(Movie, key) >= float(formData[key]))
            except ValueError:
                return []
        elif key == 'cast':
            constraints.append(Cast.name == ' '.join(formData[key].lower().title().split()))
        elif key == 'rating':
            constraints.append(getattr(Movie, key) == formData[key].upper().strip())
        elif key == 'genre':
            constraints.append(Genre.category == ' '.join(formData[key].lower().title().split()))
        elif key == 'director':
            constraints.append(Director.name == ' '.join(formData[key].lower().title().split()))
    movies = []
    for movie in Movie.query.join(Genre, Cast, Director).filter(and_(*constraints)):
        movieData = {}
        movieData.update({'id': movie.id, 'title': movie.title, 'img': movie.img})
        movieData['json'] = json.dumps({'id': movie.id})
        movies.append(movieData)
    return movies

def findOneRowById(table, targetId, strObject):
    try:
        info = table.query.filter(table.id == targetId).one()
    except MultipleResultsFound:
        print('Multiple ' + strObject + ' found with same id')
        abort(404)  
    except NoResultFound:
        print('No ' + strObject + ' found')
        abort(404)
    return info.__dict__

def getTheaterShowing(movieId, theaterId, date):
    theaterShowing = {}
    showings = Showing.query.filter(Showing.pDate == date, Showing.movieId == movieId, Showing.theaterId == theaterId).all()
    if showings != []:
        showingInfo = {'theaterId': theaterId, 'showingDate': date, 'showingUrl': showings[0].url, 'times': [showing.time for showing in showings]}
        theaterShowing['name'] = findOneRowById(Theater, theaterId, 'theaters')['name']
        theaterShowing['json'] = json.dumps(showingInfo)
    return theaterShowing

def showingSearch(formData):
    targetShowings = []
    movies = movieSearch(formData)
    theaterIds = [theater.id for theater in Theater.query.filter(Theater.city == ' '.join(formData['city'].lower().title().split()))]
    for movie in movies:
        theaterShowings = []
        for theaterId in theaterIds:
            theaterShowing = getTheaterShowing(movie['id'], theaterId, formData['date'])
            if theaterShowing:
                theaterShowings.append(theaterShowing)
        if theaterShowings != []:
            allInfo = {}
            allInfo['movie'] = movie
            allInfo['theaterShowings'] = theaterShowings
            targetShowings.append(allInfo)
    return targetShowings

@app.route('/')
def home():
    return redirect(url_for('search'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    rawScores = range(1, 11)
    imdbScores = [''] + rawScores
    rottenTomatoes = [''] + [score * 10 for score in rawScores]
    lengths = [''] + range(60, 210, 30)
    genres = [''] + [genre.category for genre in db_session.query(Genre.category).distinct()]
    ratings = [''] + [movie.rating for movie in db_session.query(Movie.rating).distinct()]
    if request.method == 'POST':
        # if basic search is implemented then date is added into form data as today's date
        formData = request.form.to_dict()
        date_key = 'date'
        if date_key not in formData:
            formData[date_key] = today
        return render_template('results.jade', allData=showingSearch(formData))
    return render_template('search.jade', genreArray=genres, ratingArray=ratings, imdbScores=imdbScores, rottenTomatoes=rottenTomatoes, movieLengths=lengths, date=today)

@app.route('/theaterData', methods=['POST'])
def theaterData():
    formData = request.form
    theaterData = findOneRowById(Theater, formData['theaterId'], 'theater')
    theaterData.pop('_sa_instance_state', None)
    return json.dumps(theaterData)

@app.route('/movieData', methods=['POST'])
def movieData():
    formData = request.form
    movieData = findOneRowById(Movie, formData['movieId'], 'movie')
    movieData.pop('_sa_instance_state', None)
    movieData['genres'] = [genre.category for genre in Genre.query.filter(Genre.movieId == movieData['id']).all()]
    movieData['cast'] = [actor.name for actor in Cast.query.filter(Cast.movieId == movieData['id']).all()]
    movieData['directors'] = [director.name for director in Director.query.filter(Director.movieId == movieData['id']).all()]
    return json.dumps(movieData)

