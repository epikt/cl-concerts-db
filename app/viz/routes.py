# -*- coding: utf-8 -*-
from app import db
#from app.main.forms import EditProfileForm, PostForm, SearchForm
from app.viz.forms import *
from app.models import *
#from app.translate import translate
from app.viz import bp
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
    
@bp.route('/event/<event_id>', methods = ['GET'])
def ViewEvent(event_id):
    event=Event.query.filter_by(id=event_id).first_or_404()
    return render_template('viz/event.html',event=event)