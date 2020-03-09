#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_wtf.csrf import CsrfProtect
from datetime import datetime
from sqlalchemy import func, desc
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
CsrfProtect(app)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Venue, Artist, Show

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  areas = Venue.query.distinct('city','state').all()
  data = []
  for area in areas:
    venues = Venue.query.filter(Venue.city == area.city, Venue.state == area.state).all()
    record = {
      "city":area.city,
      "state":area.state,
      "venues": [venue.get_venue() for venue in venues]
    }
    data.append(record)
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST','GET'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  search_term = request.args.get('search_term')
  venues = Venue.query.filter(func.lower(Venue.name).contains(search_term.lower())).all()
  data = []
  for venue in venues:
    new_data = {
    "id": venue.id,
    "name": venue.name,
    "num_upcoming_shows": venue.get_venue_history()['upcoming_shows_count'],
    }
    data.append(new_data)

  response = {
  "count": len(data),
  "data": data
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.args.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  venue = Venue.query.get(venue_id)
  data = venue.get_venue_history()
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  form = VenueForm()
  
  result = Venue.query.filter_by(name=form.name.data).first()
  if result != None:
    flash('Venue ' + request.form['name'] + ' already exists, please choose a different name.')
  elif form.validate_on_submit(): 
    newVenue = Venue(name=form.name.data,
      genres=form.genres.data,
      address =form.address.data,
      city = form.city.data,
      state = form.state.data,
      phone = form.phone.data,
      facebook_link = form.facebook_link.data,
      )
    db.session.add(newVenue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
    
# TODO: on unsuccessful db insert, flash an error instead.
  else:
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.', 'error')
    flash(form.errors)

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = Artist.query.order_by(desc(Artist.id)).limit(10)

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST', 'GET'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  name_search = request.args.get('search_term')
  artists = Artist.query.filter(func.lower(Artist.name).contains(name_search.lower())).all()
  
  data = []
  for artist in artists:
    new_data = {
    "id": artist.id,
    "name": artist.name,
    "num_upcoming_shows": artist.get_show_history()['upcoming_shows_count'],
    }
    data.append(new_data)

  response = {
  "count": len(data),
  "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.args.get('search_term', ''))

@app.route('/artists/search_bylocation', methods=['POST', 'GET'])
def search_artists_bylocation():
  location_search = request.args.get('search_term_location')
  artists = Artist.query.filter(func.lower(Artist.city).contains(location_search.lower())).all()
  
  data = []
  for artist in artists:
    new_data = {
    "id": artist.id,
    "name": artist.name,
    "num_upcoming_shows": artist.get_show_history()['upcoming_shows_count'],
    }
    data.append(new_data)

  response = {
  "count": len(data),
  "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.args.get('search_term_location', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  artist = Artist.query.get(artist_id)
  data = artist.get_show_history()
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  artist.name = form.name.data.capitalize()
  artist.genres = form.genres.data
  artist.city = form.city.data
  artist.state = form.state.data
  artist.phone = form.phone.data
  artist.image_link = form.image_link.data
  artist.facebook_link = form.facebook_link.data
  artist.seeking_venue = form.seeking_venue.data
  artist.seeking_description = form.seeking_description.data

  db.session.commit()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm()
  result = Artist.query.filter_by(name=form.name.data.capitalize()).first()
    # Check for duplicates
  if result != None:
    flash('Artist ' + request.form['name'] + ' already exists, please choose a different name.')
  elif form.validate_on_submit():
    newArtist = Artist(name=form.name.data.capitalize(),
      genres=form.genres.data,
      city = form.city.data,
      state = form.state.data,
      phone = form.phone.data,
      image_link = form.image_link.data,
      facebook_link = form.facebook_link.data,
      )
    db.session.add(newArtist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  else:
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.', 'error')
    flash(form.errors)
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  # shows = Show.query.all()
  shows = Show.query.order_by(desc(Show.id)).limit(10)
  data = [show.get_show() for show in shows]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form = ShowForm()
  if form.validate_on_submit():
    newShow = Show(
      artist_id=form.artist_id.data,
      venue_id = form.venue_id.data,
      start_time = form.start_time.data,
      )
    db.session.add(newShow)
    db.session.commit()
    flash('Show was successfully listed!')
  else:
    flash('An error occurred. Show could not be listed.', 'error')
    flash(form.errors)

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
