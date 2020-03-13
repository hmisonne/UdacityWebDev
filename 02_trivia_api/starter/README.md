# Full Stack API Final Project

## Full Stack Trivia

This project is part of the Udacity Full Stack Developer Nano Degree. The goal of this project is structure plan, implement, and test an API of a Trivia app.

## App functionalities

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

## Getting started

### Pre-requisites and Local Development 
Developers using this project should already have Python3, pip and node installed on their local machines.

[Fork](https://help.github.com/en/articles/fork-a-repo) the [project repository]()

## About the Stack

We started the full stack application for you. It is desiged with some key functional areas:

### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file. 

To run the application run the following commands: 
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend


From the frontend folder, run the following commands to start the client: 
```
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on localhost:3000. 

[View the README.md within ./frontend for more details.](./frontend/README.md)

### Tests
In order to run tests navigate to the backend folder and run the following commands: 

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command. 

All tests are kept in that file and should be maintained as updates are made to app functionality. 

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

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

### Endpoints 
Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}


#### GET /categories
- General:
	- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
	- Request Arguments: None
	- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs and a success value.
- Sample: `curl http://127.0.0.1:5000/categories`
```{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

#### GET /questions
- General:
	- Fetches a dictionary of questions in which the keys are the id, question, answer, category, difficulty.
	- Request Arguments: page number
    - Returns a list of question objects, categories object, current_category, success value, and total number of questions
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 

- Sample: `curl http://127.0.0.1:5000/books` or `curl http://127.0.0.1:5000/books?page=1`

``` {
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    ...
  ],
  "success": true,
  "total_questions": 29
}
```

#### POST /questions
- General:
    - Searches questions that contains a specific term if a search term is provided. Returns the list of questions, success value.
    	- Request Arguments: search_term
    - Creates a new question. Returns the id of the created question, success value.
    	- Request Arguments: question, answer, category and difficulty

-`curl -X POST -H "Content-Type: application/json" -d "{\"question\":\"What is the number of continents on Earth?\",\"answer\":\"5\",\"difficulty\":1,\"category\":3}"  http://127.0.0.1:5000/questions`

```
{
  "created": 43,
  "success": true
}
```

- `curl -X POST -H "Content-Type: application/json" -d "{\"search_term\":\"title\"}"  http://127.0.0.1:5000/questions`

```

```

#### DELETE /questions/{question_id}
- General:
    - Deletes the question of the given ID if it exists. Returns the id of the deleted question, success value
- `curl -X DELETE http://127.0.0.1:5000/questions/2`

```

```


## Deployment N/A

## Authors
Helene Misonne

## Acknowledgements 
Thank you Udacity for providing the framework and guidelines for this great project.
