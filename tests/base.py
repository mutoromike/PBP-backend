""" tests base case """
import os
import datetime
from contextlib import contextmanager
from unittest import TestCase
import json
from app import db, create_app

class BaseTestCase(TestCase):

    TESTING = True
    def setUp(self):
        """Set up test variables."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.app.config.from_object(self)
        self.assertTrue(self.app.testing)
        self.ctx = self.app.test_request_context()
        self.ctx.push()

        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def tearDown(self):
        db.session.close()
        db.drop_all()
        self.ctx.pop()
