from flask_restful import Resource
from flask import request

from api.utils.helpers import response_builder
from .marshmallow_schema import register_user_schema, login_user_schema
from api.endpoints.users.models import User
from api.services.helpers import generate_token

access_time = str(datetime.datetime.utcnow().time())


class RegisterUserAPI(Resource):
    """Register User Resources."""

    def __init__(self, **kwargs):
        """
        Inject dependencies for resource.
        """
        self.User = kwargs['User']

    def post(self):
        """Create a new User"""
        from manage import app
        payload = request.get_json(silent=True)
        if payload:
            try:
                register_user_schema.load(payload)
            except Exception as err:
                return response_builder(dict(err.messages), 400)

            new_user = self.User(
                first_name=payload['first_name'],
                last_name=payload['last_name'],
                email=payload['email'],
                password=payload['password']
            )

            new_user.save()
            token = generate_token(new_user.uuid)
            app.logger.info(
                'User {} SUCCESSFULLY CREATED. The log time is UTC {}'.format(new_user.email, access_time))

            return response_builder(dict(
                token=token.decode(),
                message='User successfully created, Welcome to PBP'
            ), 201)

        return response_builder(dict(
                                message="User data must be provided."),
                                400)


class LoginUserAPI(Resource):
    """Login User Resources."""

    def __init__(self, **kwargs):
        """
        Inject dependencies for resource.
        """
        self.User = kwargs['User']

    def post(self):
        """Log in User"""
        from manage import app
        payload = request.get_json()
        print(payload)
        if payload:
            try:
                login_user_schema.load(payload)
            except Exception as err:
                return response_builder(dict(err.messages), 400)

            user = User.query.filter_by(email=payload['email']).first()

            
            token = generate_token(user.uuid)
            app.logger.info(
                'LOGIN SUCCESSFUL. The log time is UTC {}'.format(access_time))

            return response_builder(dict(
                token=token.decode(),
                message='Successful Login, Welcome to PBP'
            ), 201)

        return response_builder(dict(
                                message="User data must be provided."),
                                400)
