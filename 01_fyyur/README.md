# Fyyur

## Introduction

This project is part of the Udacity Full Stack Developer Nano Degree. The goal of this project is to build the data models to power the API endpoints for the Fyyur site by connecting to a PostgreSQL database for storing, querying, and creating information about artists and venues on Fyyur.

[!Fyyur Demo](demo/demo.gif)

## App functionalities

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

## Getting started

### Pre-requisites and Local Development 
Developers using this project should already have Python3, pip and node installed on their local machines.


### Tech Stack

From the starter_code folder run `pip install requirements.txt`. All required packages are included in the requirements file. 

Before running the application, make sure you have postgres installed on your local machine. Then add add DB_USER and DB_PASS to your environment variable

```
export DB_USER=<your_username>
export DB_PASS=<your_password>
```

or replace the following fields on the 01_fyyur/models.py file

```
db_user = <your_username>
db_password = <your_password>
```

To run the application, run the following commands: 
```
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

## Deployment N/A

## Authors
Helene Misonne

## Acknowledgements 
I want to thank Udacity for providing the framework and guidelines for this great project.
