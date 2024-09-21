from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Initialize SQLAlchemy without an app context
db = SQLAlchemy()

def create_app():
    # Create and configure the Flask app
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the app with SQLAlchemy
    db.init_app(app)

    # Import models to register them with SQLAlchemy
    with app.app_context():
        from . import models

    # Register blueprints (if any)
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app