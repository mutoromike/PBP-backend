import datetime
import string
import operator

from flask_restful import Resource
from flask import request, g
from pandas import pandas as pd
from sqlalchemy import func

from api.endpoints.business.models import Business, Country, Transaction
from api.utils.helpers import response_builder, validate_file, format_date
from .marshmallow_schema import business_schema, transactions_schema
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
        self.Business = kwargs['Business']

    @token_required
    def post(self):
        payload = request.files['file']
        if payload.mimetype != "text/csv" or not payload:
            return response_builder(dict(
                message="Please upload a CSV file"
            ), 400)
        user = g.current_user.uuid
        existing = self.Business.query.filter_by(created_by_id=user).first()
        if existing:
            data = pd.read_csv(payload, header=None)
            fields = data.loc[27:]
            validate_file(data, fields)
            for i in range(len(fields)):
                payload = {
                    "transaction_type": fields.iloc[i, 0],
                    "transaction_id": int(fields.iloc[i, 1]),
                    "status": fields.iloc[i, 2],
                    "transaction_date": fields.iloc[i, 3],
                    "due_date": fields.iloc[i, 4],
                    "customer_or_supplier": fields.iloc[i, 5],
                    "item": fields.iloc[i, 6],
                    "quantity": int(fields.iloc[i, 7]),
                    "unit_amount": float(fields.iloc[i, 8]),
                    "transaction_amount": float(fields.iloc[i, 9])
                }
                try:
                    transactions_schema.load(payload)
                except Exception as err:
                    return response_builder(dict(err.messages), 400)

                transaction = transactions_schema.dump(payload)
                transaction["created_by_id"] = user
                transaction["business_id"] = existing.uuid
                new_transaction = Transaction(**transaction)
                new_transaction.save()

            return response_builder(dict(
                message="File successfully Uploaded and Processed"), 200)
        else:
            return response_builder(dict(
                message="Register a Business before uploading any files!"), 400)

    @token_required
    def get(self):
        """ Get Analytics for 30 days"""
        user = g.current_user.uuid
        start_date = datetime.datetime.now() - datetime.timedelta(60)
        start = format_date(str(start_date.date()))
        stop = format_date(str(datetime.datetime.now().date()))
        data = Transaction.query.filter(func.DATE(Transaction.due_date) <= stop).filter(
            func.DATE(Transaction.due_date) >= start).filter(Transaction.created_by_id == user)
        if data.count() > 0:
            business = Business.query.filter_by(
                created_by_id=data[0].created_by_id).first()
            """ Get first 5 items in terms of quantity """
            leading_quantity = {}
            for d in data:
                if d.transaction_type == "Order":
                    leading_quantity[d.item] = d.quantity
            ordered = dict(sorted(leading_quantity.items(),
                                  key=operator.itemgetter(1), reverse=True))
            ranked_quantity = {k: ordered[k] for k in list(ordered)[:5]}
            """ Get first 5 items in terms of value """
            leading_value = {}
            for d in data:
                if d.transaction_type == "Order":
                    leading_value[d.item] = d.quantity * d.unit_amount
            ordered_ = dict(sorted(leading_value.items(),
                                   key=operator.itemgetter(1), reverse=True))
            ranked_value = {k: ordered_[k] for k in list(ordered_)[:5]}
            """ Get incoming amount """
            orders = set()
            orders_payment = set()
            for d in data:
                if d.transaction_type == "Order":
                    orders.add(d.transaction_amount)
                if d.transaction_type == "Order Payment":
                    orders_payment.add(d.transaction_amount)
            incoming_amount = sum(orders) - sum(orders_payment)
            """ Get outgoing amount """
            bills = set()
            bills_payment = set()
            for d in data:
                if d.transaction_type == "Bill":
                    bills.add(d.transaction_amount)
                if d.transaction_type == "Bill Payment":
                    bills_payment.add(d.transaction_amount)
            outgoing_amount = sum(bills) - sum(bills_payment)

            data = {
                "leading_quantity": ranked_quantity,
                "leading_value": ranked_value,
                "incoming": incoming_amount,
                "outgoing": outgoing_amount,
                "user": string.capwords(g.current_user.first_name + " " + g.current_user.last_name),
                "business": string.capwords(business.name),
                "message": "Analitics pulled successfully"
            }
            return response_builder(data, 200)
        else:
            return response_builder(dict(
                message="No data for the specified period"
            ), 404)
