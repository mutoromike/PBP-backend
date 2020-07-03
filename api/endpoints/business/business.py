import datetime

from flask_restful import Resource
from flask import request, g
from pandas import pandas as pd

from api.endpoints.business.models import Business, Country
from api.utils.helpers import response_builder
from .marshmallow_schema import business_schema
from api.services.auth import token_required

access_time = str(datetime.datetime.utcnow().time())

class BusinessAPI(Resource):
    """Handle Business Features"""

    def __init__(self, **kwargs):
        """
        Inject resource dependencies
        """

        self.Business = kwargs['Business']
        self.Country = kwargs['Country']

    @token_required
    def post(self):
        """Create new business"""
        from manage import app
        payload = request.get_json(silent=True)
        if payload:
            try:
                business_schema.load(payload)
            except Exception as err:
                return response_builder(dict(err.messages), 400)

            created_by = g.current_user.uuid
            new_business = self.Business(
                name=payload['name'],
                name_abbr=payload['abbreviated_name'],
                address=payload['address'],
                country=payload['country'],
                entity=payload['entity'],
                revenue=payload['revenue'],
                acc_sftw=payload['accounting_software'],
                created_by_id=created_by
            )

            new_business.save()
            countries = payload['countries'].split(",")
            for country in countries:
                new_country = self.Country(
                    name=country.lower(),
                    business_id=new_business.uuid
                )
                new_country.save()
            app.logger.info(
                'Business {} SUCCESSFULLY CREATED. The log time is UTC {}'.format(new_business.name, access_time))

            return response_builder(dict(
                message='Business successfully created!'
            ), 201)

        return response_builder(dict(
                                message="Business data must be provided."),
                                400)


class ProcessCsvAPI(Resource):

    def post(self):
        payload = request.files['file']
        print(payload)
        return