from flask import Blueprint

income_sources_bp = Blueprint('income_sources_bp', __name__, template_folder='../../templates')

from . import views