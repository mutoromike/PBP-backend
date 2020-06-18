""" app/__init__.py """
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from api.models.base import BaseModel, db
from config import app_config



def create_app(config_name):
	# Initialize app
	app = Flask(__name__)
	app.config.from_object(app_config[config_name])
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)
	cors = CORS(app)


	return app