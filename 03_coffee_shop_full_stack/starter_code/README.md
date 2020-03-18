# Coffee Shop Full Stack

## Full Stack Nano - IAM Final Project

This project is part of the Udacity Full Stack Developer Nano Degree. The goal of this project is to implement a restful API for a Digital Cafe App. This project is using Auth0 as a third-party authentication system to allow roles-based access control (RBAC).


## App functionalities

1) Display graphics representing the ratios of ingredients in each drink.
2) Allow public users to view drink names and graphics.
3) Allow the shop baristas to see the recipe information.
4) Allow the shop managers to create new drinks and edit existing drinks.

## Getting started

### Pre-requisites and Local Development 
Developers using this project should already have Python3, pip, Ionic and node installed on their local machines.

Starter code available on this [project repository](https://github.com/udacity/FSND/tree/master/projects/03_coffee_shop_full_stack/starter_code)

## About the Stack

### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file. 

To run the application run the following commands from within the `./src` directory: 
```
export FLASK_APP=api.py;
flask run --reload
```
If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

[View the README.md within ./backend for more details.](./backend/README.md)


### Frontend

From the frontend folder, run the following commands to start the client: 
```
npm install // only once to install dependencies
ionic serve
```

By default, the frontend will run on `localhost:3000`. 


[View the README.md within ./frontend for more details.](./frontend/README.md)

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require API keys but does require an authentication through Auth0. To setup a Auth0 account follow these [instructions](./backend/README.md)

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "Bad Request"
}
```
The API will return three error types when requests fail:
- 400: Bad request
- 404: Resource not found
- 422: Request unprocessable
- 500: Internal Server Error

### API permissions

2 roles are currently defined:
- Barista
    - can `get:drinks-detail`
- Manager
    - can perform all actions

### Endpoints 

#### Prerequisites

To visualize the results of the following endpoints, import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json` 

Navigate to the authorization tab, and update the type to Bearer Token and paste the JWT in the token field.

#### GET /drinks
- General:
	- Fetches a dictionary of questions in which the keys are the id and recipe.
	- Request Arguments: None
	- Returns: A list of drinks with short description of th recipe

```
{
  "drinks": [
    {
      "id": 3,
      "recipe": [
        {
          "color": "Black",
          "parts": 5
        },
        {
          "color": "red",
          "parts": 1
        }
      ],
      "title": "Coke"
    },
    {
      "id": 4,
      "recipe": [
        {
          "color": "Blue",
          "parts": 1
        },
        {
          "color": "yellow",
          "parts": 2
        }
      ],
      "title": "Curacao"
    }
  ],
  "success": true
}
```

#### GET /drinks-detail
- General:
	- Fetches a dictionary of questions in which the keys are the id and recipe.
	- Request Arguments: None
	- Returns: A list of drinks with complete description of recipe

```
{
  "drinks": [
    {
      "id": 2,
      "recipe": {
        "color": "pink",
        "name": "Water",
        "parts": 1
      },
      "title": "Water"
    },
    {
      "id": 3,
      "recipe": [
        {
          "color": "Black",
          "name": "",
          "parts": 5
        },
        {
          "color": "red",
          "name": "",
          "parts": 1
        }
      ],
      "title": "Coke"
    }
  ],
  "success": true
}
```

#### POST /drinks
- General:
    - Creates a new drink. Returns the detail of the created drink, success value.
    - Request Arguments: title, recipe
```
{
  "drinks": [
    {
      "id": 2,
      "recipe": {
        "color": "pink",
        "name": "Water",
        "parts": 1
      },
      "title": "Water5"
    }
  ],
  "success": true
}
```

#### PATCH /drinks/<drink_id>
- General:
    - Modify a drink. Returns the detail of the created drink, success value.
    - Request Arguments: title and/or recipe
```
{
  "drinks": {
    "id": 1,
    "recipe": {
      "color": "blue",
      "name": "Water",
      "parts": 1
    },
    "title": "Water50"
  },
  "success": true
}
```

#### DELETE /drinks/<drink_id>
- General:
    - Deletes the drink of the given ID if it exists. Returns the id of the deleted drink, success value


```
{
  "delete": "1",
  "success": true
}
```

## Deployment N/A

## Authors
Helene Misonne

## Acknowledgements 
I want to thank Udacity for providing the framework and guidelines for this great project.