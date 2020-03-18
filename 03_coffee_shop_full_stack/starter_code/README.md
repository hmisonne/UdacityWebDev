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

### Authentification : Auth0
This application is using Auth0. To setup a Auth0 account follow these [instructions](./backend/README.md)

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

## Deployment N/A

## Authors
Helene Misonne

## Acknowledgements 
I want to thank Udacity for providing the framework and guidelines for this great project.