from sqlalchemy import Column, String, DateTime, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import os 


database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

class User(db.Model):  
	__tablename__ = 'User'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	objectives = db.relationship('Objective', backref='user', lazy=True, cascade="all, delete-orphan")
	# def __init__(self, name, catchphrase=""):
	#   self.name = name
	#   self.catchphrase = catchphrase

	def format(self):
	  return {
	    'id': self.id,
	    'name': self.name,
	    'objectives': self.objectives}

class Objective(db.Model):

	__tablename__ = 'Objective'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	start_date = Column(DateTime)
	end_date = Column(DateTime)
	completed = Column(Boolean)
	history = Column(String)
	frequency = Column(String)
	user_id = Column(Integer, db.ForeignKey('User.id'),
	    	nullable=False)

	def insert(self):
	    db.session.add(self)
	    db.session.commit()
  
	def update(self):
    	db.session.commit()
	
	def delete(self):
	    db.session.delete(self)
	    db.session.commit()

	def format(self):
	    return {
	      'id': self.id,
	      'name': self.name,
	      'completed': self.completed,
	      'participant': self.user,
	      'difficulty': self.difficulty
	    }