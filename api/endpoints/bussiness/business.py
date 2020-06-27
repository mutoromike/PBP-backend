from flask_restful import Resource
from flask import request

from api.endpoints.bussiness.models import Bussiness
from api.utils.helpers import response_builder
from .marshmallow_schema import create_business_schema
from api.services.auth import token_required


class BusinessAPI(Resource):
    """Handle Business Features"""

    def __init__(self, **kwargs):
        """
        Inject resource dependencies
        """

        self.Business = kwargs['Business']

    @token_required
    def post(self):
        """Create new business"""
        payload = request.get_json(silent=True)
        if payload:
            try:
                business_schema.load(payload)
            except Exception as err:
                return response_builder(dict(err.messages), 400)

            new_business = self.User(
                first_name=payload['first_name'],
                last_name=payload['last_name'],
                email=payload['email'],
                password=payload['password']
            )
