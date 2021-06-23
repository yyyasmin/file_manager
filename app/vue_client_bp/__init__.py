#FROM https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure
from flask import Blueprint

#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from app import db   # pragma: no cover
from app import vue_client_bp, models


vue_bp = Blueprint('vue_client_bp', __name__, template_folder='templates')

from . import vue_client_bp