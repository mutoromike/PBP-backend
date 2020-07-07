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
                'Business {} SUCCESSFULLY CREATED. The log time is \
                    UTC {}'.format(new_business.name, access_time))

            return response_builder(dict(
                message='Business successfully created!'
            ), 201)

        return response_builder(dict(
                                message="Business data must be provided."),
                                400)

    @token_required
    def get(self, business_id=None):
        """ Get created business """
        business = self.Business.query.filter_by(uuid=business_id).first()
        countries = self.Country.query.filter_by(business_id=business_id).all()
        if business:
            data = business_schema.dump(business)
            if countries:
                country_data = []
                for country in countries:
                    country_data.append(country.name)

                data["countries"] = country_data

            return response_builder(dict(business=data), 200)
        return response_builder(dict(
                                message="Business with that ID not found"),
                                404)

    @token_required
    def put(self, business_id=None):
        """ Update specific business """
        print(g.current_user.email)
        business = self.Business.query.filter_by(uuid=business_id).first()
        if business:
            # refactor this later
            print(business)
            payload = request.get_json(silent=True)
            if payload:
                try:
                    business_schema.load(payload)
                except Exception as err:
                    return response_builder(dict(err.messages), 400)

                business.name = payload['name'],
                business.name_abbr = payload['abbreviated_name'],
                business.address = payload['address'],
                business.country = payload['country'],
                business.entity = payload['entity'],
                business.revenue = payload['revenue'],
                business.acc_sftw = payload['accounting_software']

                business.save()
                country_s = self.Country.query.filter_by(business_id=business.uuid).all()
                if country_s:
                    for country in country_s:
                        country.delete()
                countries = payload['countries'].split(",")
                for country in countries:
                    new_country = self.Country(
                        name=country.lower(),
                        business_id=business.uuid
                    )
                    new_country.save()

                return response_builder(dict(
                    message='Business successfully updated!'
                ), 200)
        return response_builder(dict(
            message="Business not found!"
        ), 404)


class ProcessCsvAPI(Resource):

    def post(self):
        payload = request.files['file']
        data = pd.read_csv(payload)
        print(data)
        return