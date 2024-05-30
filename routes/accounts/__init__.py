from flask import Blueprint

accounts_bp = Blueprint('accounts_bp', __name__, template_folder='../../templates')

from . import views