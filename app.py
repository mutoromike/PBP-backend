""" app/__init__.py """
from flask import Flask, Blueprint, redirect
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from api.models.base import db
from api.endpoints.users import users_bp
from api.endpoints.business import business_bp
from config import app_config


def create_app(config_name):
    # Initialize app
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    cors = CORS(app)
    url_version_1 = '/api/v1'
    # register users blueprint
    app.register_blueprint(
        users_bp(Api, Blueprint),
        url_prefix=url_version_1
    )
    # register business blueprint
    app.register_blueprint(
        business_bp(Api, Blueprint),
        url_prefix=url_version_1
    )

    @app.route('/')
    def health_check_url():
        return redirect("https://documenter.getpostman.com/view/3425671/T1DiHghM", code=200)

    return app
