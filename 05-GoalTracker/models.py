from sqlalchemy import Column, String, Integer, DateTime, Boolean, create_engine
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

class Athlete(db.Model):  
  __tablename__ = 'Athlete'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  goal = Column(String)
  weight = Column(Integer)
  height = Column(Integer)
  age = Column(Integer)
  objectives = db.relationship('Objective', backref='athlete', lazy=True, cascade="all, delete-orphan")
  # def __init__(self, name, catchphrase=""):
  #   self.name = name
  #   self.catchphrase = catchphrase
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
      'objectives': [objective.format() for objective in self.objectives]
      }
  def short_format(self):
    return {
      'id': self.id,
      'name': self.name
    }

class Objective(db.Model):

  __tablename__ = 'Objective'

  id = Column(Integer, primary_key=True)
  description = Column(String)
  start_date = Column(DateTime)
  end_date = Column(DateTime)
  completed = Column(Boolean, default=False)
  athlete_id = Column(Integer, db.ForeignKey('Athlete.id'),
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
        'start_date': self.start_date,
        'end_date': self.end_date,
        'description': self.description,
        'completed': self.completed,
        'participant': self.athlete.short_format()
      }

class Coach(db.Model):  
  __tablename__ = 'Coach'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  reviews = Column(Integer)
  specialty = Column(String)

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
      'specialty': self.specialty}