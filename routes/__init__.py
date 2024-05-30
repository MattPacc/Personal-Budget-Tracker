# Citation for the following code:
# Date: 05/22/2024
# Adapted from:
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app?tab=readme-ov-file#step-0---quick-and-dirty-task-1-setup
# and
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app
from flask import Flask, render_template
from flask_mysqldb import MySQL

# Initialize the MySQL extension
mysql = MySQL()

def create_app():
    app = Flask(__name__, static_url_path='/static', static_folder='../static')
    app.secret_key = 'super_secret_key'  # Needed for flashing messages

    app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
    app.config['MYSQL_USER'] = 'cs340_paccionm'
    app.config['MYSQL_PASSWORD'] = '1546'  # last 4 of onid
    app.config['MYSQL_DB'] = 'cs340_paccionm'
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

    @app.route("/")
    def home():
        return render_template("index.html")

    return app
