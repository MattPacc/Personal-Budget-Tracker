from routes import create_app

app = create_app()

# Listener
if __name__ == "__main__":
    app.run(port=55308, debug=True)