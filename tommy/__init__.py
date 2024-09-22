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

    # Function to generate a random nonce
    def generate_nonce(length=16):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    talisman = Talisman(app)

    @app.before_request
    def set_csp_nonce():
        # Generate a nonce for this request
        nonce = generate_nonce()
        request.csp_nonce = nonce

        # Define CSP with the generated nonce
        csp = {
            'default-src': '\'self\'',
            'style-src': [f'\'self\'', f'\'nonce-{nonce}\'', 'https://cdn.jsdelivr.net'],
            'script-src': [f'\'self\'', f'\'nonce-{nonce}\'']
        }

        # Apply the CSP dynamically to the current request
        talisman.content_security_policy = csp

    # Import models to register them with SQLAlchemy
    with app.app_context():
        from . import models

    # Register blueprints (if any)
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app