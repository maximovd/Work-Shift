from flask import Blueprint

bp = Blueprint('control_panel', __name__)

from app.control_panel import views
