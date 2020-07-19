# Full Stack API Final Project

## Full Stack GoalTracker

This project is the final project of the Udacity Full Stack Developer Nano Degree. The goal of this project is to deploy a Flask application with Heroku/PostgreSQL and enable Role Based Authentication and roles-based access control git (RBAC) with Auth0 (third-party authentication systems). 

I decided to implement a RESTful for a GoalTracker app where coaches can assign objectives to athlete and athlete can monitor their progress.

## Getting started

### Pre-requisites and Local Development 

Developers using this project should already have Python3, pip and node installed on their local machines.

To create a virtual environment on Windows:
```
py -m venv env
```
To activate it:
```
.\env\Scripts\activate
```
If running locally on macOS and Linux, look for the commands in the [Python documentation](
https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


## About the Stack

### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file. 

The PostgreSQL database is hosted on Heroku.

To run the application on your local machine, run the following commands from the GoalTracker foler: 
```
set FLASK_APP=app.py
set FLASK_ENV=development
flask run
```
If running locally on macOS and Linux, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is running on `https://goaltrackerhm.herokuapp.com/` and can also be accessed on your local machine at `http://127.0.0.1:5000/`.

### Frontend

Work in Progress

### Authentification set-up:

All required configuration settings are on conf_settings.env
Run these commands in your terminal to update your environment variables

If the token expired, run the `auth/token_generator.py` file to generate a new token for the Coach role.

### Tests

To run the tests locally, make sure you have PostgreSQL installed, [PostgreSQL install documentation](https://www.postgresql.org/)

Then set up a test database add DB_USER and DB_PASS to your environment variable

```
export DB_USER=<your_username>
export DB_PASS=<your_password>
export coach_token=<generated_token>
export athlete_token=<generated_token>
```

or set your environment variables on windows.

In order to run tests navigate to the backend folder and run the following commands: 

```
dropdb goaltracker_test
createdb goaltracker_test
python test_goaltracker.py
```

The first time you run the tests, omit the dropdb command. Then run:

```
python test_goaltracker.py
```

All tests are kept in that file and should be maintained as updates are made to app functionality. 


To run the tests on the Heroku app, use the postman collection and run it with newman [newman documentation](https://www.npmjs.com/package/newman):

`newman run GoalTrackerAuth.postman_collection.json`

## API Reference

### Getting Started
- Base URL: The backend app is hosted on `https://goaltrackerhm.herokuapp.com/`
- It can be run locally on `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application requires authentication for some of the endpoints.

### Error Handling
Errors are returned as JSON objects in the following format:
```json
{
    "success": false, 
    "error": 400,
    "message": "Bad Request"
}
```
The API will return these error types when requests fail:
- 400: Bad request
- 404: Resource not found
- 405: Method not allowed
- 422: Request unprocessable
- 500: Internal Server Error

If the route requires authentification and the request fails, it will return:
- 401: "Message regarding the authorization header, or token"
- 400: "Invalid header"
- 403: "Permission not found"

### Roles and Permissions

There are currenly 2 roles: 

- Athlete : 
	- Can view objectives and objectives per athlete
- Coach : 
	- All permissions an Athlete has and…
	- View, create, edit and delete new objectives
	- Delete athlete from database

### Endpoints 


#### POST /objectives (Auth required)

- Add new objective

- Example of response for a request with following body: { "description": "Go to the gym twice a week for 30 min","athlete_id": 3,"start_date":"2020,1,1","end_date":"2020,12,12" } and the appropriate header:
```json
{
  "objective": {
    "completed": false,
    "description": "Go to the gym twice a week for 30 min",
    "end_date": "Sat, 12 Dec 2020 00:00:00 GMT",
    "id": 4,
    "participant": {
      "id": 3,
      "name": "Vanessa"
    },
    "start_date": "Wed, 01 Jan 2020 00:00:00 GMT"
  },
  "success": true
}
```

#### GET /objectives (Auth required)

- View all objectives

```json
{
  "objectives": [
    {
      "completed": false,
      "description": "Go to the gym twice a week for 30 min",
      "end_date": "Sat, 12 Dec 2020 00:00:00 GMT",
      "id": 3,
      "participant": {
        "id": 3,
        "name": "Vanessa"
      },
      "start_date": "Wed, 01 Jan 2020 00:00:00 GMT"
    }
  ],
  "success": true
}
```

#### PATCH /objective/<objective_id> (Auth required)

- Amend objective

- Example of response for a request with following body: {"description": "Test"} and the appropriate header:

```json
{
  "objective": {
    "completed": false,
    "description": "Test",
    "end_date": "Sat, 12 Dec 2020 00:00:00 GMT",
    "id": 2,
    "participant": {
      "id": 1,
      "name": "Andrea"
    },
    "start_date": "Wed, 01 Jan 2020 00:00:00 GMT"
  },
  "success": true
}
```

#### POST /athletes

- Add a new athlete
- Sample:`curl -X POST -H "Content-Type: application/json" -d "{\"name\":\"Vanessa\",\"goal\": \"Loose 5 kg\",\"weight\": \"40\",\"height\": \"170\",\"age\": \"30\"}"  http://127.0.0.1:5000/athletes`

```json
{
    "athlete": {
        "id": 4,
        "name": "Vanessa",
        "objectives": []
    },
    "success": true
}
```

#### GET /athletes/

- Get the list of all athletes
- Sample:`curl -X GET http://127.0.0.1:5000/athletes`

```json
{
    "athletes": [
        {
            "id": 1,
            "name": "Andrea",
            "objectives": [
                {
                    "completed": false,
                    "description": "Test",
                    "end_date": "Sat, 12 Dec 2020 00:00:00 GMT",
                    "id": 2,
                    "participant": {
                        "id": 1,
                        "name": "Andrea"
                    },
                    "start_date": "Wed, 01 Jan 2020 00:00:00 GMT"
                }
            ]
        },
        {
            "id": 3,
            "name": "Vanessa",
            "objectives": [
                {
                    "completed": false,
                    "description": "Walk twice a week for 20 min",
                    "end_date": "Sat, 12 Dec 2020 00:00:00 GMT",
                    "id": 3,
                    "participant": {
                        "id": 3,
                        "name": "Vanessa"
                    },
                    "start_date": "Wed, 01 Jan 2020 00:00:00 GMT"
                },
                {
                    "completed": false,
                    "description": "Go to the gym twice a week for 30 min",
                    "end_date": "Sat, 12 Dec 2020 00:00:00 GMT",
                    "id": 4,
                    "participant": {
                        "id": 3,
                        "name": "Vanessa"
                    },
                    "start_date": "Wed, 01 Jan 2020 00:00:00 GMT"
                }
            ]
        }
    ],
    "success": true
}
```

#### DELETE /athletes/<athlete_id> (Auth required)

- Delete athlete based on his id
- Sample of response for id = 4

```json
{
    "athlete_deleted": "4",
    "success": true
}
```

## Deployment N/A

## Authors
Helene Misonne

## Acknowledgements 
I want to thank Udacity for providing the framework and guidelines for this great project.
