import random
import string

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_talisman import Talisman

# Initialize SQLAlchemy without an app context
db = SQLAlchemy()

def create_app():
    # Create and configure the Flask app
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the app with SQLAlchemy
    db.init_app(app)

    # Simplified CSP configuration without nonce
    csp = {
        'default-src': '\'self\'',
        'style-src': [
            '\'self\'',
            'https://cdn.jsdelivr.net'  # Allow styles from jsdelivr (for Tailwind CSS)
        ],
        'script-src': [
            '\'self\''
        ]
    }

    # Initialize Flask-Talisman with static CSP configuration
    talisman = Talisman(app, content_security_policy=csp)

    # Import models to register them with SQLAlchemy
    with app.app_context():
        from . import models

    # Register blueprints (if any)
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app