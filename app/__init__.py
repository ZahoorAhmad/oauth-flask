from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .models import OAuthToken
from .oauth import OAuthIntegration

#
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
#
# db = SQLAlchemy()
# migrate = Migrate()
#
# def create_app():
#     app = Flask(__name__)
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://oauthUser:oauthPassword123@db:5432/oauthdb'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     app.secret_key = 'your_secret_key'
#
#     # Initialize extensions
#     db.init_app(app)
#     migrate.init_app(app, db)
#
#     # Import routes and models after initializing extensions
#     from . import models
#     from . import routes
#
#     return app
