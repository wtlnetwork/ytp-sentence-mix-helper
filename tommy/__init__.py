from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_talisman import Talisman

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    csp = {
        'default-src': "'self'",
        'style-src': [
            "'self'"
        ],
        'script-src': [
            "'self'"
        ],
        'img-src': [
            "'self'"
        ],
        'manifest-src': [
            "'self'"
        ],
        'frame-ancestors': [
            "'none'"
        ],
        'form-action': [
            "'self'"
        ]
    }

    talisman = Talisman(app, content_security_policy=csp)

    with app.app_context():
        from . import models

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app