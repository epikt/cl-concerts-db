# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectMultipleField, SelectField, IntegerField, DateField
from wtforms.validators import ValidationError, DataRequired, Length, Optional, NumberRange
from flask_babel import _, lazy_gettext as _l
from app.models import  Instrument, InstrumentType, Person,\
                        Location, Organization, EventType, Event, MusicalPiece,\
                        Activity
