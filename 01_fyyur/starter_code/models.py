from app import db
from datetime import datetime

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    city = db.Column(db.String(120), nullable = False)
    state = db.Column(db.String(120), nullable = False)
    address = db.Column(db.String(120), nullable = False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)
    website = db.Column(db.String(500))
    shows = db.relationship('Show', backref='venue', lazy=True)
    genres = db.Column(db.String(120), nullable = False)

    def get_venue(self):
      return {"id": self.id, "name": self.name, "num_upcoming_shows": 0}

    def get_venue_history(self):
      past_shows = []
      upcoming_shows = []

      for show in self.shows:
        if show.start_time < datetime.now():
          past_shows.append(show.get_show_per_venue())
        else:
          upcoming_shows.append(show.get_show_per_venue())

      venue_show_history = {"id": self.id, 
        "name": self.name, 
        "genres": self.genres,
        "address": self.address,
        "city": self.city,
        "state": self.state,
        "phone": self.phone,
        "website": self.website,
        "facebook_link": self.facebook_link,
        "seeking_talent": self.seeking_talent,
        "seeking_description": self.seeking_description,
        "image_link": self.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows)}
      return venue_show_history

    def __repr__(self):
      return f'<Venue {self.id} {self.name}>'


class Artist(db.Model):
    __tablename__ = 'Artist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    city = db.Column(db.String(120), nullable = False)
    state = db.Column(db.String(120), nullable = False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120), nullable = False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)
    website = db.Column(db.String(500))
    shows = db.relationship('Show', backref='artist', lazy=True)

    def get_show_history(self):
      past_shows = []
      upcoming_shows = []

      for show in self.shows:
        if show.start_time < datetime.now():
          past_shows.append(show.get_show_per_artist())
        else:
          upcoming_shows.append(show.get_show_per_artist())

      artist_show_history = {"id": self.id, 
      "name": self.name, 
      "genres": self.genres,
      "city": self.city,
      "state": self.state,
      "phone": self.phone,
      "seeking_venue": self.seeking_venue,
      "seeking_description": self.seeking_description,
      "image_link": self.image_link,
      "facebook_link": self.facebook_link,
      "website": self.website,
      "past_shows": past_shows,
      "upcoming_shows": upcoming_shows,
      "past_shows_count": len(past_shows),
      "upcoming_shows_count": len(upcoming_shows)}
      return artist_show_history

class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    start_time = db.Column(db.DateTime)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'),
        nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'),
        nullable=False)
    def get_show(self):
      return {"venue_id": self.venue_id, 
          "venue_name": Venue.query.get(self.venue_id).name,
          "artist_id": self.artist_id,
          "artist_name": Artist.query.get(self.artist_id).name,
          "artist_image_link": Artist.query.get(self.artist_id).image_link,
          "start_time": str(self.start_time)
          }

    def get_show_per_artist(self):
      return {
        "venue_id": self.venue_id,
        "venue_name": Venue.query.get(self.venue_id).name,
        "venue_image_link": Venue.query.get(self.venue_id).image_link,
        "start_time": str(self.start_time)
        }
    def get_show_per_venue(self):
      return {
        "artist_id": self.artist_id,
        "artist_name": Artist.query.get(self.artist_id).name,
        "artist_image_link": Artist.query.get(self.artist_id).image_link,
        "start_time": str(self.start_time)
      }


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#
# show_identifier = db.Table('show_identifier',
#     db.Column('show_id', db.Integer, db.ForeignKey('Show.id'), primary_key=True),
#     db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
# )
# new_venue=Venue(name='W',genres='rock',address='test',city='LA',state='CA',website='test')

