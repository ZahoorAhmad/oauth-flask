# app.py
import os

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate

from . import db  # Import db from the app package

load_dotenv()

app = Flask(__name__)

# Set up the database URL for PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL",
                                                  "postgresql://oauthUser:oauthPassword123@db:5432/oauthdb")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")

# Initialize the database
db.init_app(app)
migrate = Migrate(app, db)

# Import the models and OAuth integration after db initialization to avoid circular import

# Create tables
with app.app_context():
    db.create_all()
