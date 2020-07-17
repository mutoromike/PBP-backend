"""
File to handle testing business
"""
import os
import json

from tests.base import BaseTestCase
from fixtures.business import *
from fixtures.auth import register, login


class BusinessTestCase(BaseTestCase):
    """
    Test Business Class
    """

    def get_token(self):
        """register and login a user to get an access token"""
        self.client().post('/api/v1/auth/register',
                           data=json.dumps(register), content_type='application/json')
        response = self.client().post('/api/v1/auth/login',
                                      data=json.dumps(login), content_type='application/json')
        data = json.loads(response.data.decode())
        access_token = data['token']
        return access_token

    def test_create_business(self):
        """
        Test API can create business.
        """
        access_token = self.get_token()
        response = self.client().post('/api/v1/business', headers=dict(Authorization=access_token),
                                      data=json.dumps(business), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_create_business_wrong_data(self):
        """
        Test API error create business.
        """
        access_token = self.get_token()
        response = self.client().post('/api/v1/business', headers=dict(Authorization=access_token),
                                      data=json.dumps(bad_business), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_create_business_unauthorized(self):
        """
        Test API error create business.
        """
        response = self.client().post('/api/v1/business', headers=dict(Authorization="string"),
                                      data=json.dumps(business), content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_create_and_get_business(self):
        """
        Test API can create and get business.
        """
        access_token = self.get_token()
        self.client().post('/api/v1/business', headers=dict(Authorization=access_token),
                           data=json.dumps(business), content_type='application/json')
        response = self.client().get('/api/v1/business', headers=dict(Authorization=access_token),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_missing_business(self):
        """
        Test API cannot get missing business.
        """
        access_token = self.get_token()
        response = self.client().get('/api/v1/business', headers=dict(Authorization=access_token),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_update_business_details(self):
        """
        Test API can update business.
        """
        access_token = self.get_token()
        self.client().post('/api/v1/business', headers=dict(Authorization=access_token),
                           data=json.dumps(business), content_type='application/json')
        res = self.client().get('/api/v1/business', headers=dict(Authorization=access_token),
                                     content_type='application/json')
        data = json.loads(res.data.decode())
        uuid = data['business']['uuid']
        response = self.client().put('/api/v1/business/{}'.format(uuid), headers=dict(Authorization=access_token),
                                     data=json.dumps(update_business), content_type='application/json')
        self.assertEqual(response.status_code, 200)
