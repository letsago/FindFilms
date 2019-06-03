# FindFilms Implementation

Hello and welcome to this README! This documents my implementation of FindFilms app. 
The FindFilms app returns relevant AMC movie showings based on date, city, and specific movie criteria user input. 
The app is built using: 

* Flask-SocketIO (Python library) - for the server
* Jade - for page content
* Bootstrap - for page layout
* Sqlite3 - for database

## How to run

```bash
git clone https://flashhire@dev.azure.com/flashhire/PatrickYu/_git/PatrickYu

# To setup working environment
[Virtualenv documentation](https://virtualenv.pypa.io/en/latest/)

# To enter working environment
source path-to-virtualenv/bin/activate

# Please enter appropriate directory and install all necessary packages from requirements.txt file first
cd PatrickYu/FindFilms/server
pip install -r requirements.txt 

# To initialize test database
SERVER_SETTINGS=./configs/test.cfg python -c 'from server.database import init_test_db; init_test_db()'

# To initialize production database
SERVER_SETTINGS=./configs/production.cfg python -c 'from scrapers.prod_db_integration import init_prod_db; init_prod_db()'

# To update showings table in production database
SERVER_SETTINGS=./configs/production.cfg python -c 'from scrapers.prod_db_integration import update_prod_showings; update_prod_showings()'

# To update theaters table in production database
SERVER_SETTINGS=./configs/production.cfg python -c 'from scrapers.prod_db_integration import update_prod_theaters; update_prod_theaters()'

# To run all automated tests using test database
SERVER_SETTINGS=./configs/test.cfg pytest 

# To run site with specific configuration
SERVER_SETTINGS=./configs/production.cfg python launch.py
SERVER_SETTINGS=./configs/test.cfg python launch.py
SERVER_SETTINGS=./configs/development.cfg python launch.py
```

## Run App in Production Mode with Docker
```
docker run -d -p 5000:3001 letsago/findfilm:server
```

## Directory Structure

Note that the main project folders are scrapers, server, and tests modules. 
Each of them has a __init__.py file which allows other modules to import their files and functions.
All test cases were written using [pytest](https://docs.pytest.org/en/latest/) framework.

### Directories
* /server
    * Setup code for Flask deployment
    * Contains production and test databases
    * Launches app 
    * /scrapers
        * Runs all the web scrapers that extracts all the relevant data and inserts the data into the database
        * Contains functions to initialize and update production database
    * /server
        * Contains database structure and session creation
        * Contains functions to initialize test database
        * Runs backend server functionality for search, results, and details pages
        * /configs
            * Contains all configuration files
        * /static
            * Contains personalized CSS style template
            * Contains javascript code
        * /templates
            * Contains all webpages written in Jade
            * /common
                * Contains common functions and layout used in all webpages
    * /tests
        * Contains all test cases

## Known issues
- [ ] No implemented IMDb web scraper so the data is hard-coded

## Completed Ideas
- [x] Flask env setup
- [x] UI templates for search, results, and details pages
- [x] Backend functionality for results and details pages
- [x] Search function that returns relevent movies from user inputted search criteria
- [x] Update website to use [Bootstrap](https://getbootstrap.com/docs/4.2/layout/overview/)
- [x] Movie, Theater, Showing, Genre, Cast, and Director tables in database
- [x] Rotten Tomatoes web scraper that extracts movie info
- [x] AMC web scraper that extracts theater and showing info 
- [x] Production, test, and development configurations
- [x] Integration of web scraped data into production database
- [x] Updated search function to return available showings from user inputted city and date 
- [x] Added basic search feature
- [x] Created pop up modals to show detailed results
- [x] Display active user count
- [x] Pop up modals request detailed results on user clicks
- [x] Parallel processing to speed up web scraping

## Potential future work
- [ ] Find and return minimum distance theater with available showing from user location
- [ ] Create recommendation system with user search history

**Thanks for reading me and have a lovely day!**
