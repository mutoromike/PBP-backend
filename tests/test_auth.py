"""
File to handle testing authentication
"""
import os
import json

from tests.base import BaseTestCase
from fixtures.auth import *


class AuthTestCase(BaseTestCase):
    """
    Test Auth Class
    """

    def test_register_user(self):
        """
        Test API can register user.
        """
        response = self.client().post('/api/v1/auth/register',
                                      data=json.dumps(register), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_error_register_user(self):
        """
        Test API cannot register user wrong data.
        """
        response = self.client().post('/api/v1/auth/register',
                                      data=json.dumps(bad_register), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_register_wrong_email(self):
        """
        Test API cannot register user wrong data.
        """
        response = self.client().post('/api/v1/auth/register',
                                      data=json.dumps(bad_email_register), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_login_user(self):
        """
        Test API can login user.
        """
        self.client().post('/api/v1/auth/register',
                           data=json.dumps(register), content_type='application/json')
        response = self.client().post('/api/v1/auth/login',
                                      data=json.dumps(login), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_login_non_existing_user(self):
        """
        Test API error login user.
        """
        response = self.client().post('/api/v1/auth/login',
                                      data=json.dumps(login), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_login_wrong_password(self):
        """
        Test API error login user.
        """
        self.client().post('/api/v1/auth/register',
                           data=json.dumps(register), content_type='application/json')
        response = self.client().post('/api/v1/auth/login',
                                      data=json.dumps(bad_login), content_type='application/json')
        self.assertEqual(response.status_code, 400)
