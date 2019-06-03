from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from server import app

# test database contains AMC showing info that needs to be updated every Wednesday - the day AMC updates their showings
engine = create_engine(app.config['DATABASE_URI'], convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
                
def init_test_db():
    Base.metadata.create_all(bind=engine)
    from server.database import db_session
    from server.models import Movie, Theater, Showing, Genre, Cast, Director

    Movie.query.delete()
    Theater.query.delete()
    Showing.query.delete()
    Genre.query.delete()
    Cast.query.delete()
    Director.query.delete()

    movie_one = Movie(  
                        'https://www.rottentomatoes.com/m/the_dark_knight',
                        'https://www.imdb.com/title/tt0468569/', 
                        'The Dark Knight', 
                        'PG-13', 
                        152, 
                        'https://upload.wikimedia.org/wikipedia/en/8/8a/Dark_Knight.jpg',
                        9.0, 
                        94,
                        "Christopher Nolan steps back into the director's chair for this sequel to Batman Begins, which finds the titular superhero coming face to face with his greatest nemesis -- the dreaded Joker. Christian Bale returns to the role of Batman, Maggie Gyllenhaal takes over the role of Rachel Dawes (played by Katie Holmes in Batman Begins), and Brokeback Mountain star Heath Ledger dons the ghoulishly gleeful Joker makeup previously worn by Jack Nicholson and Cesar Romero. Just as it begins to appear as if Batman, Lt. James Gordon (Gary Oldman), and District Attorney Harvey Dent (Aaron Eckhart) are making headway in their tireless battle against the criminal element, a maniacal, wisecracking fiend plunges the streets of Gotham City into complete chaos. ~ Jason Buchanan, Rovi"
                    )

    movie_two = Movie(  
                        'https://www.rottentomatoes.com/m/500_days_of_summer',
                        'https://www.imdb.com/title/tt1022603/',
                        '500 Days of Summer', 
                        'PG-13', 
                        95,
                        'https://upload.wikimedia.org/wikipedia/en/d/d1/Five_hundred_days_of_summer.jpg', 
                        7.7, 
                        85, 
                        "Joseph Gordon-Levitt and Zooey Deschanel star in director Marc Webb's wry, nonlinear romantic comedy about a man who falls head over heels for a woman who doesn't believe in love. Tom (Gordon-Levitt) is an aspiring architect who currently earns his living as a greeting card writer. Upon encountering his boss' beautiful new secretary, Summer (Deschanel), Tom discovers that the pair have plenty in common despite the fact that she's seemingly out of his league; for starters, they both love the Smiths, and they're both fans of surrealist artist Magritte. Before long Tom is smitten. All he can think about is Summer. Tom believes deeply in the concept of soul mates, and he's finally found his. Unfortunately for Tom, Summer sees true love as the stuff of fairy tales, and isn't looking for romance. Undaunted and undeterred by his breezy lover's casual stance on relationships, Tom summons all of his might and courage to pursue Summer and convince her that their love is real. ~ Jason Buchanan, Rovi"
                    )

    movie_three = Movie(    
                        'https://www.rottentomatoes.com/m/spirited_away',
                        'https://www.imdb.com/title/tt0245429/',
                        'Spirited Away', 
                        'PG', 
                        124,
                        'https://upload.wikimedia.org/wikipedia/en/d/db/Spirited_Away_Japanese_poster.png', 
                        8.6, 
                        97,
                        "Master animation director Hayao Miyazaki follows up on his record-breaking 1997 opus Princess Mononoke with this surreal Alice in Wonderland-like tale about a lost little girl. The film opens with ten-year-old Chihiro riding along during a family outing as her father races through remote country roads. When they come upon a blocked tunnel, her parents decide to have a look around -- even though Chihiro finds the place very creepy. When they pass through the tunnel, they discover an abandoned amusement park. As Chihiro's bad vibes continue, her parents discover an empty eatery that smells of fresh food. After her mother and father help themselves to some tasty purloined morsels, they turn into giant pigs. Chihiro understandably freaks out and flees. She learns that this very weird place, where all sorts of bizarre gods and monsters reside, is a holiday resort for the supernatural after their exhausting tour of duty in the human world. Soon after befriending a boy named Haku, Chihiro learns the rules of the land: one, she must work , as laziness of any kind is not tolerated; and two, she must take on the new moniker of Sen. If she forgets her real name, Haku tells her, then she will never be permitted to leave. ~ Jonathan Crow, Rovi"
                    )

    movie_four = Movie(
                        'https://www.rottentomatoes.com/m/the_grand_budapest_hotel',
                        'https://www.imdb.com/title/tt2278388/', 
                        'The Grand Budapest Hotel', 
                        'R', 
                        99,
                        'https://upload.wikimedia.org/wikipedia/en/1/1c/The_Grand_Budapest_Hotel.png', 
                        8.1, 
                        91,
                        "THE GRAND BUDAPEST HOTEL recounts the adventures of Gustave H, a legendary concierge at a famous European hotel between the wars, and Zero Moustafa, the lobby boy who becomes his most trusted friend. The story involves the theft and recovery of a priceless Renaissance painting and the battle for an enormous family fortune -- all against the back-drop ofa suddenly and dramatically changing Continent. (c) Fox Searchlight"
                    )

    movie_five = Movie(
                        'https://www.rottentomatoes.com/m/american_psycho',
                        'https://www.imdb.com/title/tt0144084/', 
                        'American Psycho',
                        'R', 
                        97,
                        'https://upload.wikimedia.org/wikipedia/en/0/0c/American_Psycho.png', 
                        7.6, 
                        68,
                        "Patrick Bateman is young, white, beautiful, ivy leagued, and indistinguishable from his Wall Street colleagues. Shielded by conformity, privilege, and wealth, Bateman is also the ultimate serial killer, roaming freely and fearlessly. His murderous impulses are fueled by zealous materialism and piercing envy when he discovers someone else has acquired more than he has. After a colleague presents a business card superior in ink and paper to his, Bateman's blood thirst sharpens, and he steps up his homicidal activities to a frenzied pitch. Hatchets fly, butcher knives chop, chainsaws rip, and surgical instruments mutilate-how far will Bateman go? How much can he get away with?"
                    )

    movie_six = Movie(  
                        'https://www.rottentomatoes.com/m/alita_battle_angel',
                        'https://www.imdb.com/title/tt0437086/', 
                        'Alita: Battle Angel', 
                        'PG-13', 
                        125, 
                        'https://resizing.flixster.com/dL-8X6XHhPBaA60t2zmquQzA6uI=/fit-in/200x296.2962962962963/v1.bTsxMjk4NTcxOTtqOzE3OTcwOzEyMDA7NDA1MDs2MDAw',
                        7.6, 
                        61, 
                        "From visionary filmmakers James Cameron (AVATAR) and Robert Rodriguez (SIN CITY), comes ALITA: BATTLE ANGEL, an epic adventure of hope and empowerment. When Alita (Rosa Salazar) awakens with no memory of who she is in a future world she does not recognize, she is taken in by Ido (Christoph Waltz), a compassionate doctor who realizes that somewhere in this abandoned cyborg shell is the heart and soul of a young woman with an extraordinary past. As Alita learns to navigate her new life and the treacherous streets of Iron City, Ido tries to shield her from her mysterious history while her street-smart new friend Hugo (Keean Johnson) offers instead to help trigger her memories. But it is only when the deadly and corrupt forces that run the city come after Alita that she discovers a clue to her past - she has unique fighting abilities that those in power will stop at nothing to control. If she can stay out of their grasp, she could be the key to saving her friends, her family and the world she's grown to love."
                    )

    theater_one = Theater('https://www.amctheatres.com/movie-theatres/seattle-tacoma/amc-pacific-place-11', 'AMC Pacific Place 11', '600 Pine Street - Ste 400', 'Seattle', 'Washington', 98101)
    theater_two = Theater('https://www.amctheatres.com/movie-theatres/seattle-tacoma/amc-oak-tree-6', 'AMC Oak Tree 6', '10006 Aurora Avenue N.', 'Seattle', 'Washington', 98133)
    theater_three = Theater('https://www.amctheatres.com/movie-theatres/seattle-tacoma/amc-seattle-10', 'AMC Seattle 10', '4500 9th Ave Ne', 'Seattle', 'Washington', 98105)
    db_session.add_all([movie_one, movie_two, movie_three, movie_four, movie_five, movie_six, theater_one, theater_two, theater_three])
    db_session.commit()
    db_session.add_all([
        Genre(movie_one.id, 'Action & Adventure'),
        Genre(movie_one.id, 'Drama'),
        Genre(movie_one.id, 'Science Fiction & Fantasy'),
        Cast(movie_one.id, 'Christian Bale'),
        Cast(movie_one.id, 'Heath Ledger'),
        Cast(movie_one.id, 'Aaron Eckhart'),
        Cast(movie_one.id, 'Maggie Gyllenhaal'),
        Cast(movie_one.id, 'Gary Oldman'),
        Cast(movie_one.id, 'Morgan Freeman'),
        Director(movie_one.id, 'Christopher Nolan'),

        Genre(movie_two.id, 'Comedy'),
        Genre(movie_two.id, 'Drama'),
        Genre(movie_two.id, 'Romance'),
        Cast(movie_two.id, 'Joseph Gordon-Levitt'),
        Cast(movie_two.id, 'Zooey Deschanel'),
        Cast(movie_two.id, 'Geoffrey Arend'),
        Cast(movie_two.id, 'Chloe Grace Moretz'),
        Cast(movie_two.id, 'Matthew Gray Gubler'),
        Cast(movie_two.id, 'Clark Gregg'),
        Director(movie_two.id, 'Marc Webb'),

        Genre(movie_three.id, 'Animation'),
        Genre(movie_three.id, 'Drama'),
        Genre(movie_three.id, 'Kids & Family'),
        Genre(movie_three.id, 'Science Fiction & Fantasy'),
        Cast(movie_three.id, 'Rumi Hiiragi'),
        Cast(movie_three.id, 'Miyu Irino'),
        Cast(movie_three.id, 'Mari Natsuki'),
        Cast(movie_three.id, 'Takashi Naito'),
        Cast(movie_three.id, 'Yasuko Sawaguchi'),
        Cast(movie_three.id, 'Tsunehiko Kamijo'),
        Director(movie_three.id, 'Hayao Miyazaki'),

        Genre(movie_four.id, 'Comedy'),
        Genre(movie_four.id, 'Drama'),
        Cast(movie_four.id, 'Ralph Fiennes'),
        Cast(movie_four.id, 'Tony Revolori'),
        Cast(movie_four.id, 'F. Murray Abraham'),
        Cast(movie_four.id, 'Edward Norton'),
        Cast(movie_four.id, 'Saoirse Ronan'),
        Cast(movie_four.id, 'Tilda Swinton'),
        Director(movie_four.id, 'Wes Anderson'),

        Genre(movie_five.id, 'Comedy'),
        Genre(movie_five.id, 'Drama'),
        Genre(movie_five.id, 'Horror'),
        Genre(movie_five.id, 'Mystery & Suspense'),
        Cast(movie_five.id, 'Christian Bale'),
        Cast(movie_five.id, 'Willem Dafoe'),
        Cast(movie_five.id, 'Jared Leto'),
        Cast(movie_five.id, 'Josh Lucas'),
        Cast(movie_five.id, 'Samantha Mathis'),
        Cast(movie_five.id, 'Chloe Sevigny'),
        Director(movie_five.id, 'Mary Harron'),

        Genre(movie_six.id, 'Action & Adventure'),
        Genre(movie_six.id, 'Romance'),
        Cast(movie_six.id, 'Rosa Salazar'),
        Cast(movie_six.id, 'Christoph Waltz'),
        Cast(movie_six.id, 'Jennifer Connelly'),
        Cast(movie_six.id, 'Mahershala Ali'),
        Cast(movie_six.id, 'Ed Skrein'),
        Cast(movie_six.id, 'Jackie Earle Haley'),
        Director(movie_six.id, 'Robert Rodriguez'),

        Showing(movie_six.id, theater_one.id, 'https://www.amctheatres.com/showtimes/alita-battle-angel-43118/2019-02-13/amc-pacific-place-11/all', '2019-02-13', '7:00pm'),
        Showing(movie_six.id, theater_one.id, 'https://www.amctheatres.com/showtimes/alita-battle-angel-43118/2019-02-13/amc-pacific-place-11/all', '2019-02-13', '9:55pm'),

        Showing(movie_six.id, theater_two.id, 'https://www.amctheatres.com/showtimes/alita-battle-angel-43118/2019-02-13/amc-oak-tree-6/all', '2019-02-13', '7:00pm'),
        Showing(movie_six.id, theater_two.id, 'https://www.amctheatres.com/showtimes/alita-battle-angel-43118/2019-02-13/amc-oak-tree-6/all', '2019-02-13', '9:15pm'),

        Showing(movie_six.id, theater_three.id, 'https://www.amctheatres.com/showtimes/alita-battle-angel-43118/2019-02-13/amc-seattle-10/all', '2019-02-13', '7:00pm'),
        Showing(movie_six.id, theater_three.id, 'https://www.amctheatres.com/showtimes/alita-battle-angel-43118/2019-02-14/amc-seattle-10/all', '2019-02-14', '4:30pm'),
        Showing(movie_six.id, theater_three.id, 'https://www.amctheatres.com/showtimes/alita-battle-angel-43118/2019-02-14/amc-seattle-10/all', '2019-02-14', '7:20pm'),
        Showing(movie_six.id, theater_three.id, 'https://www.amctheatres.com/showtimes/alita-battle-angel-43118/2019-02-14/amc-seattle-10/all', '2019-02-14', '10:10pm')
    ])
    db_session.commit()
