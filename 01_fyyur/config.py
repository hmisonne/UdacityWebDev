import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASS')

database_name = "fyyurapp"
SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}/{}".format(db_user, db_password,'localhost:5432', database_name)

# Command Line: psql -U postgres fyyurapp