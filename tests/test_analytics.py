"""
File to handle testing business
"""
import os
import json
from werkzeug.datastructures import FileStorage

from tests.base import BaseTestCase
from fixtures.business import business
from fixtures.auth import register, login


class BAnalyticsTestCase(BaseTestCase):
    """
    Test Analytics Class
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

    def test_successful_file_upload(self):
        """Create Business the post CSV File"""
        access_token = self.get_token()
        self.client().post('/api/v1/business', headers=dict(Authorization=access_token),
                           data=json.dumps(business), content_type='application/json')
        my_csv = os.path.join("tests/text_file.csv")
        my_file = FileStorage(
            stream=open(my_csv, "rb"),
            filename="text_file.csv",
            content_type="text/csv",
        ),

        response = self.client().post("/api/v1/data-upload", headers=dict(Authorization=access_token),
                                      data={"file": my_file}, content_type="multipart/form-data"
                                      )
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_file_upload(self):
        """Create Business the post CSV File"""
        access_token = self.get_token()
        self.client().post('/api/v1/business', headers=dict(Authorization=access_token),
                           data=json.dumps(business), content_type='application/json')
        my_csv = os.path.join("tests/text_file.csv")
        my_file = FileStorage(
            stream=open(my_csv, "rb"),
            filename="text_file.csv",
            content_type="text/csv",
        ),

        response = self.client().post("/api/v1/data-upload", headers=dict(Authorization="asasafsgfvteyt4wu6t"),
                                      data={"file": my_file}, content_type="multipart/form-data"
                                      )
        self.assertEqual(response.status_code, 401)
