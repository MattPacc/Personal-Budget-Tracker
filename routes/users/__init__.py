from flask import Blueprint

users_bp = Blueprint('users_bp', __name__, template_folder='../../templates')

from . import views