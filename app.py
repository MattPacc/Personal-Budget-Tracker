# Citation for the following code:
# Date: 05/22/2024
# Adapted from:
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app?tab=readme-ov-file#step-0---quick-and-dirty-task-1-setup
# and
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app
from routes import create_app

app = create_app()

# Listener
if __name__ == "__main__":
    app.run(port=55308, debug=True)