
from datetime import datetime
from flask_wtf import FlaskForm
# from FlaskForm import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL, ValidationError, Length
from enums import State, Genre

choicesGenre=[
    ('Alternative', 'Alternative'),
    ('Blues', 'Blues'),
    ('Classical', 'Classical'),
    ('Country', 'Country'),
    ('Electronic', 'Electronic'),
    ('Folk', 'Folk'),
    ('Funk', 'Funk'),
    ('Hip-Hop', 'Hip-Hop'),
    ('Heavy Metal', 'Heavy Metal'),
    ('Instrumental', 'Instrumental'),
    ('Jazz', 'Jazz'),
    ('Musical Theatre', 'Musical Theatre'),
    ('Pop', 'Pop'),
    ('Punk', 'Punk'),
    ('R&B', 'R&B'),
    ('Reggae', 'Reggae'),
    ('Rock n Roll', 'Rock n Roll'),
    ('Soul', 'Soul'),
    ('Other', 'Other'),
]


class ShowForm(FlaskForm):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

def custom_validator(form, field):
    if (field.data[0],field.data[0]) not in choicesGenre:
    # # raise ValidationError('Valid enums are %s' % ([choice.value for choice in Genre]))
        raise ValidationError('Not Valid enums ')


class VenueForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired(), Length(-1,120)]
    )
    city = StringField(
        'city', validators=[DataRequired(), Length(-1,120)]
    )
    state = SelectField(
        'state', validators=[DataRequired(), AnyOf([choice.value for choice in State])],
        choices=State.choices()
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        # 'genres',
        'genres', validators=[DataRequired(), custom_validator],
        choices=Genre.choices()
    )
    facebook_link = StringField(
        # 'facebook_link'
        'facebook_link', validators=[URL()]

    )
    seeking_talent = BooleanField(
        # TODO implement enum restriction
        'seeking_talent'
    )
    seeking_description = StringField(
        # TODO implement enum restriction
        'seeking_description'
    ) 

class ArtistForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired(), Length(-1,120)]
    )
    city = StringField(
        'city', validators=[DataRequired(), Length(-1,120)]
    )
    state = SelectField(
        'state', validators=[DataRequired(), AnyOf([choice.value for choice in State])],
        choices=State.choices()
    )
    phone = StringField(
        # TODO implement validation logic for state
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired(), custom_validator],
        choices=Genre.choices()
    )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[URL()]
    )
    seeking_venue = BooleanField(
        # TODO implement enum restriction
        'seeking_venue'
    )
    seeking_description = StringField(
        # TODO implement enum restriction
        'seeking_description'
    ) 

# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM
