# Citation for the following code:
# Date: 05/22/2024
# Adapted from:
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app
# Exploration - Developing in Flask: https://canvas.oregonstate.edu/courses/1958399/pages/exploration-developing-in-flask?module_item_id=24181857
from flask import Flask, render_template
from flask_mysqldb import MySQL

# Initialize the MySQL extension
mysql = MySQL()

def create_app():
    app = Flask(__name__, static_url_path='/static', static_folder='../static')
    app.secret_key = 'super_secret_key'  # Needed for flashing messages

    # Replace placeholder credentials with your MySQL configuration
    app.config['MYSQL_HOST'] = 'localhost'  # or any placeholder
    app.config['MYSQL_USER'] = 'username'   # or any placeholder
    app.config['MYSQL_PASSWORD'] = 'password'  # or any placeholder
    app.config['MYSQL_DB'] = 'database'  # or any placeholder
    app.config['MYSQL_CURSORCLASS'] = "DictCursor"

      # Initialize MySQL
    mysql = MySQL(app)
    
    # Store the MySQL instance in the app context
    app.extensions = {'mysql': mysql}

    # Import and register Blueprints
    from routes.categories import categories_bp
    app.register_blueprint(categories_bp, url_prefix='/categories')

    from routes.expenses import expenses_bp
    app.register_blueprint(expenses_bp, url_prefix='/expenses')

    from routes.income_sources import income_sources_bp
    app.register_blueprint(income_sources_bp, url_prefix='/income')

    from routes.users import users_bp
    app.register_blueprint(users_bp, url_prefix='/users')

    from routes.user_passwords import user_passwords_bp
    app.register_blueprint(user_passwords_bp, url_prefix='/passwords')
    
    from routes.accounts import accounts_bp
    app.register_blueprint(accounts_bp, url_prefix='/accounts')

    @app.route("/")
    def home():
        return render_template("index.html")

    return app
