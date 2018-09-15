# -*- coding: utf-8 -*-
from flask import Blueprint

bp = Blueprint('viz', __name__)

from app.viz import routes
