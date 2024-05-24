from flask import Blueprint

categories_bp = Blueprint('categories_bp', __name__, template_folder='../../templates')

from . import views