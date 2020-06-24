#!/usr/bin/env python

"""Entry point for app, contain commands to configure and run the app."""

import os
import sys
import logging

from flask_migrate import Migrate
from flask.cli import FlaskGroup

from api.models.base import db

from app import create_app
from run_tests import test

config_name = os.getenv("FLASK_ENV")
app = create_app(config_name)
cli = FlaskGroup(app)

if __name__ == "__main__":
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


@cli.command()
def drop():
    """Drop database tables."""
    try:
        db.drop_all()
        print("Dropped all tables successfully.")
    except Exception:
            print("Failed, make sure your database server is running!")


@cli.command()
def create():
    """Create database tables from sqlalchemy models."""
    try:
        db.create_all()
        print("Created tables successfully.")
    except Exception:
        db.session.rollback()
        print("Failed, make sure your database server is running!")


@cli.command()
def tests():
    """Run the tests."""
    test()


migrate = Migrate(app, db)

if __name__ == "__main__":
    cli()
