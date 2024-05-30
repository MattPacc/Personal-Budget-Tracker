from flask import Blueprint

expenses_bp = Blueprint('expenses_bp', __name__, template_folder='../../templates')

from . import views