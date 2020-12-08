# Casting Agency
##### Udacity Full stack Nanodegree Capstone Project

The motivation for this project is to create my capstone project for Udacity's Fullstack Nanodegree program. This project models a Casting Agency company that is responsible for creating movies and managing and assigning actors to those movies.

## API URL 
- **Heroku:** https://casting-agency-sv.herokuapp.com/
- **Localhost:** http://127.0.0.1:5000/

## Features
- Create, Edit and View movies and actors based on access levels

## Authentication and Authorization
Authentication and Authorization implemented using Auth0

#### Roles
- Executive Producer
- Casting Director
- Casting Assistant

#### Permissions
Roles have been assigned the following permissions:
- Casting Assistant
    - get:movies
    - get:actors
- Casting Director
    - get:movies
    - get:actors
    - post:actors
    - delete:actors
    - patch:actors
    - patch:movies
- Exeuctive Producer
    - get:movies
    - get:actors
    - post:actors
    - delete:actors
    - patch:actors
    - patch:movies
    - post:movies
    - delete:movies

#### Three users have been defined for initial review. Each assigned to a different role with relevant permissions. JWT tokens provided below associated with these users will expire after 24 hours
```
Executive Director:
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii13c29yTGJuU3ZkVnZoc1BNeEdDMiJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LXN2LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZmNkMDlhNWMwNThmODAwNmY0NTkzYjEiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNjA3NDQ2NzQ1LCJleHAiOjE2MDc1MzMxNDUsImF6cCI6IkxzN0tqT3pBd0pJTFBwVUplbE13MGhoZVRKSzE3bFlBIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.COS9VzpvckeXPLbX0NFyvDp_TG3nT3KXvgWT5JcZ_oXVMZnkYbcvXa7h8jAC86yaVrHHAyr80TQuSuuwWbxGvmIerXPU4ssYoVi30pg0GAY6PH_l3QvaGWo2WU4orEZSVcTBcJoCrEQHw9HoP3za-szDiJjh87hRkMBiczFYytVWAe4qvA2sy23-SiWCRPUWQtSe17Nw9aPMa9jMGVeFVcQiJyYlHXGOsZrfGFRcTqSKd-wROKBTzW1Z_Kk8jG2jQYPp8Jj9a-GHCn4BtEmzjFK6LOEnfF3LNbKAOyGOTL0eExE1OD9U-t4YIrBA5_LbwkhkO-gw9VlC2YunGmBAQw

Casting Director:
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii13c29yTGJuU3ZkVnZoc1BNeEdDMiJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LXN2LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZmNkMDlmYjRlMmFkMTAwNzE1ZDRhNzUiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNjA3NDQ2ODI1LCJleHAiOjE2MDc1MzMyMjUsImF6cCI6IkxzN0tqT3pBd0pJTFBwVUplbE13MGhoZVRKSzE3bFlBIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.MNaJJk0PV5SKt0-OwBmHIm063GHDxd5k6iy9zPfEg4qNfIZrOGam8Dkgc8RvhFU2rpI6ePyV-SyQDBAgT37pktc18287mveVM1msqqCZp_uezrDZ1V1BILhw7CwHhbNB0e4cIrMeGFiIYCCt_xgekuK2TRcFK_ENCjMTdDMCAZRVscpUVu_AcEojA2v8hJHXEV2tItrX-E95129mypCuEvZZbZxzpBErrOJGoOJlxWbXBGacRPzbCAsxFcuvxVZFmA8vo5Gzs9-buhaVvKAvT3sjwFEoeNLcv9Ve1Txz1cpMFiq1UMsvvDWpOaGM9svAxR3pGeyZtbOpaFLjx0erVw

Casting Assistant
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii13c29yTGJuU3ZkVnZoc1BNeEdDMiJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LXN2LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZmNkMGExNDRlMmFkMTAwNzE1ZDRhOWUiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNjA3NDQ2ODk4LCJleHAiOjE2MDc1MzMyOTgsImF6cCI6IkxzN0tqT3pBd0pJTFBwVUplbE13MGhoZVRKSzE3bFlBIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.uz0y2h0YAlYau2HT_HV_LYgzfHsuUan3e0jbqRJgJ47809EUi62oTYFYgpZIGPe1tWUsxPkZj9DRc4c8ApiKV36Qw9jJYpsXkW9LBohPKOE_El99mNudjJwDf5tSxdVvDVh1viXKxjHg-lRzWkPsCFYvwpCow4orDv06l3pT-U4TuRR5AsdduYsyIg_AVS6xWqEMjrXbMFcA9VvmHcEoWxwDlkycjvhV9BEx8lk7GsM-FlvpEU1WzkSIiI5557qxXdkO2eRLyBT3BaVNRAQNvc2y3wEUShxwH10mo6a6NBxq6wTfPb06nLhEPb0-DyS9YupanEFBtcAvqjkKKpp2cg
```

## Project Dependencies

Project was developed, tested in a Windows 10 OS development enviornment.

### Installing Dependencies

#### Python 3.7 or greater

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

Working within a virtual environment is recommended.

#### PIP Dependencies
- Below will install dependencies using pip
```
pip install -r requirements.txt
```

- Change database_url in setup.bat and run setup.bat (windows batch file) to setup enviornment variables
- setup.bat needs to be run after creating databases in postgresql and prior to running any python code
```
setup.bat
```

- Start flask web server
```
flask run
```

##### Key Dependencies

- Python
- Flask
- Flask-CORS
- Flask-Migrate
- SQLAlchemy
- PostgreSQL
- Auth0

#### Authentication

Authentication is implemented using Auth0, it uses RBAC to assign permissions using roles, these are tokens you could use to access the endpoints.
Note: The tokens expires in 24 hours you can create your own tokens at [Auth0](https://auth0.com/)

#### Database Setup
- Create two databases. One for development and one for testing
- Update database_url in setup.bat and test.bat with development and test databases respectively created above.
- Run setup.bat or test.bat (if running tests) prior to running any python file
- Generate database tables from flask migrate script and include seed data by executing:
```
python manage.py db upgrade
python manage.py seed
```

#### Testing
- Ensure a test database is created and database_url is updated in test.bat.
- Execute test.bat (windows batch file) to upgrade db, seed data and run test_app.py
- To start tests, run
```
test.bat
```

### Endpoints

#### GET /movies

- Returns all movies.
- Roles authorized : Casting Assistant, Casting Director, Executive Producer.
- Sample:  `curl http://127.0.0.1:5000/movies`

```json
{
    "movies": [
        {
            "id": 1,
            "release_date": "Mon, 01 Jan 2018 00:00:00 GMT",
            "title": "Spider Man"
        },
        {
            "id": 2,
            "release_date": "Mon, 01 Jan 2018 00:00:00 GMT",
            "title": "Iron Man"
        },
        {
            "id": 3,
            "release_date": "Mon, 01 Jan 2018 00:00:00 GMT",
            "title": "Thor"
        }
    ],
    "success": true
}
```

#### GET /movies/\<int:id\>

- Route for getting a specific movie.
- Roles authorized : Casting Assistant, Casting Director, Executive Producer.
- Sample:  `curl http://127.0.0.1:5000/movies/1`

```json
{
    "movie": {
        "id": 1,
        "release_date": "Mon, 01 Jan 2018 00:00:00 GMT",
        "title": "Spider Man"
    },
    "success": true
}
```

#### POST /movies

- Creates a new movie.
- Roles authorized : Executive Producer.
- Sample: `curl http://127.0.0.1:5000/movies -X POST -H "Content-Type: application/json" -d '{
"release_date": "01-01-2018",
"title": "Ant Man"
}'`

```json
{
    "movie": {
        "id": 4,
        "release_date": "Mon, 01 Jan 2018 00:00:00 GMT",
        "title": "Ant Man"
    },
    "success": true
}
```

#### PATCH /movies/\<int:id\>

- Patches a movie based on a payload.
- Roles authorized : Casting Director, Executive Producer.
- Sample: `curl http://127.0.0.1:5000/movies/3 -X POST -H "Content-Type: application/json" -d '{
"release_date": "01-01-2018",
"title": "Ant Man 2"
}'`

```json
{
    "movie": {
        "id": 3,
        "release_date": "Mon, 01 Jan 2018 00:00:00 GMT",
        "title": "Ant Man 2"
    },
    "success": true
}
```


#### DELETE /movies/\<int:id\>

- Deletes a movies by id.
- Roles authorized : Executive Producer.
- Sample: `curl http://127.0.0.1:5000/movies/3 -X DELETE`

```json
{
    "message": "movie id 3, titled Ant Man 2 was deleted",
    "success": true
}
```

#### GET /actors

- Returns all actors.
- Roles authorized : Casting Assistant, Casting Director, Executive Producer.
- Sample:  `curl http://127.0.0.1:5000/actors`

```json
{
    "actors": [
        {
            "age": 45,
            "gender": "male",
            "id": 1,
            "name": "Robert Jr"
        },
        {
            "age": 42,
            "gender": "male",
            "id": 2,
            "name": "Chris Evans"
        },
        {
            "age": 38,
            "gender": "female",
            "id": 3,
            "name": "Elizabeth Olsen"
        }
    ],
    "success": true
}
```

#### GET /actors/\<int:id\>

- Route for getting a specific actor.
- Roles authorized : Casting Assistant, Casting Director, Executive Producer.
- Sample:  `curl http://127.0.0.1:5000/actors/1`

```json
{
    "actor": {
        "age": 45,
        "gender": "male",
        "id": 1,
        "name": "Robert Jr"
    },
    "success": true
}
```

#### POST /actors

- Creates a new actor.
- Roles authorized : Casting Director, Executive Producer.
- Sample: `curl http://127.0.0.1:5000/actors -X POST -H "Content-Type: application/json" -d '{
"name": "Chris Hemsworth",
"age": 38,
"gender": "male"
}'`

```json
{
    "actor": {
        "age": 38,
        "gender": "male",
        "id": 4,
        "name": "Chris Hemsworth"
    },
    "success": true
}
```

#### PATCH /actors/\<int:id\>

- Patches an actor.
- Roles authorized : Casting Director, Executive Producer.
- Sample: `curl http://127.0.0.1:5000/actors/4 -X POST -H "Content-Type: application/json" -d '{
"name": "Chris Hemsworth",
"age": 40,
"gender": "male"
}'`

```json
{
    "actor": {
        "age": 40,
        "gender": "male",
        "id": 4,
        "name": "Chris Hemsworth"
    },
    "success": true
}
```


#### DELETE /actors/\<int:id\>

- Deletes an actor by id form the url parameter.
- Roles authorized : Casting Director,Executive Producer.
- Sample: `curl http://127.0.0.1:5000/actors/4 -X DELETE`

```json
{
    "message": "actor id 4, named Chris Hemsworth was deleted",
    "success": true
}
```