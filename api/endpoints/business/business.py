import datetime
import string

from flask_restful import Resource
from flask import request, g
from pandas import pandas as pd

from api.endpoints.business.models import Business, Country, Transaction
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
        user = g.current_user.uuid
        existing = self.Business.query.filter_by(created_by_id=user).all()
        if existing:
            return response_builder(dict(
                message="You already have an existing business"
            ), 400)
        payload = request.get_json(silent=True)
        if payload:
            try:
                business_schema.load(payload)
            except Exception as err:
                return response_builder(dict(err.messages), 400)

            created_by = user
            new_business = self.Business(
                name=payload['name'],
                abbreviated_name=payload['abbreviated_name'],
                address=payload['address'],
                country=payload['country'],
                entity=payload['entity'],
                revenue=payload['revenue'],
                accounting_software=payload['accounting_software'],
                created_by_id=created_by
            )

            new_business.save()
            countries = payload['countries'].split(",")
            for country in countries:
                new_country = self.Country(
                    name=string.capwords(country),
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
    def get(self):
        """ Get created business """
        user = g.current_user.uuid
        business = self.Business.query.filter_by(created_by_id=user).first()
        if business:
            countries = self.Country.query.filter_by(business_id=business.uuid).all()

            data = business_schema.dump(business)
            if countries:
                country_data = []
                for country in countries:
                    country_data.append(country.name)

                data["countries"] = country_data

            return response_builder(dict(business=data), 200)
        return response_builder(dict(
                                message="You have no Business Account"),
                                404)

    @token_required
    def delete(self, business_id):
        """ Delete Business """
        business = self.Business.query.filter_by(uuid=business_id).first()
        if business:
            deleted = business.delete()
            if deleted:
                return response_builder(dict(message="Business Successfully DELETED!"), 200)
            else:
                return response_builder(dict(message="An Error Occurred, Please Try again."), 400)
        return response_builder(dict(
                                message="A Business With That ID doesn't exist!"),
                                404)

    @token_required
    def put(self, business_id=None):
        """ Update specific business """
        business = self.Business.query.filter_by(uuid=business_id).first()
        if business:
            # refactor this later
            user = g.current_user.uuid
            if business.created_by_id != user:
                return response_builder(dict(
                    message="You can only edit your own business"
                ), 401)
            payload = request.get_json(silent=True)
            if payload:
                try:
                    business_schema.load(payload)
                except Exception as err:
                    return response_builder(dict(err.messages), 400)

                business.name = payload['name'],
                business.abbreviated_name = payload['abbreviated_name'],
                business.address = payload['address'],
                business.country = payload['country'],
                business.entity = payload['entity'],
                business.revenue = payload['revenue'],
                business.accounting_software = payload['accounting_software']

                business.save()
                country_s = self.Country.query.filter_by(business_id=business.uuid).all()
                if country_s:
                    for country in country_s:
                        country.delete()
                countries = payload['countries'].split(",")
                for country in countries:
                    new_country = self.Country(
                        name=string.capwords(country),
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

    def __init__(self, **kwargs):
        """
        Inject resource dependencies
        """

        self.Transaction = kwargs['Transaction']

    def post(self):
        payload = request.files['file']
        data = pd.read_csv(payload, header=None)
        """ Check for random headers"""
        if data.iloc[0, 0] != "Do not change the headers" or data.iloc[10, 1] != "Required" \
                or data.iloc[21, 0] != "Order Payment" or data.iloc[25, 2] != "Status":
            return response_builder(dict(message="The file headers are corrupted, \
                kindly upload file with correct headers"), 400)
        if data.iloc[25, 0] != "Transaction" or data.iloc[25, 1] != "ID" or data.iloc[25, 2] != "Status"\
                or data.iloc[25, 3] != "Transaction Date" or data.iloc[25, 4] != "Due Date" or data.iloc[25, 5] != \
                "Customer or Supplier" or data.iloc[25, 6] != "Item" or data.iloc[25, 7] != "Quantity":
            return response_builder(dict(message="The file headers are corrupted, \
                kindly upload file with correct headers"), 400)

        fields = data.loc[27:]
        if fields.isnull().values.any():
            return response_builder(dict(message="Some of the required fields \
                are missing"), 400)
        for i in range(len(fields)):
            print(fields.iloc[i, 0], type(fields.iloc[i, 1])) 

        return
