from flask import Blueprint

bp = Blueprint('shift', __name__)

from app.shift import views
