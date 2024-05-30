from flask import Blueprint

user_passwords_bp = Blueprint('user_passwords_bp', __name__, template_folder='../../templates')

from . import views