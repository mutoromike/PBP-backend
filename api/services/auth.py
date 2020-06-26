"""
Authorisation Module.

This module contains the authorisation required by the client to
communicate with the API.
"""
import os
import base64
from functools import wraps
import datetime

from flask import current_app, g, request
from jose import ExpiredSignatureError, JWTError, jwt

from .helpers import store_user_details
from api.models import User
from api.utils.helpers import response_builder

access_time = str(datetime.datetime.utcnow().time())

def verify_token(authorization_token, secret_key):
    """Validate token."""
    from manage import app
    try:
        payload = jwt.decode(
            authorization_token,
            secret_key,
            algorithms=['RS256'],
            options={
                'verify_signature': True,
                'verify_exp': True
            })
    except JWTError:
        payload = jwt.decode(
            authorization_token,
            secret_key,
            algorithms=['RS256'],
            options={
                'verify_signature': True,
                'verify_exp': True
            })
    app.logger.info('Token SUCCESSFULLY validated: The ACCESS time is UTC {}'.format(access_time)) # Noqa E501
    return payload


# authorization decorator
def token_required(f):
    """Authenticate that a valid Token is present."""
    @wraps(f)
    def decorated(*args, **kwargs):
        from manage import app
        # check that the Authorization header is set
        authorization_token = request.headers.get('Authorization')
        if not authorization_token:
            return response_builder(dict(
                                    message="Bad request. Header does"
                                    "not contain authorization token"), 400)

        unauthorized_message = "Unauthorized. The authorization token " \
                               "supplied is invalid"

        try:
            # decode token
            secret_key = os.get_env("SECRET_KEY")
            payload = verify_token(authorization_token,
                                   secret_key)
        except ExpiredSignatureError:
            expired_response = "The authorization token supplied is expired"
            app.logger.warning('Token HAS EXPIRED!')
            return response_builder(dict(message=expired_response), 401)
        except JWTError:
            app.logger.info('Token Authentication FAILED!: The ACCESS time is UTC {}'.format(access_time)) # Noqa E501
            return response_builder(dict(message=unauthorized_message), 401)

        # confirm that payload and UserInfo has required keys
        if ("UserInfo" and "exp") not in payload.keys():
            return response_builder(dict(message=unauthorized_message), 401)
        elif not payload["UserInfo"].get("id"):
            return response_builder(dict(message="malformed token"), 401)
        else:
            user = User.query.get(payload["UserInfo"]["id"])  #TODO check if user id exists
            # user id returns the name of the user
            if not user:
                user = store_user_details(payload, authorization_token)
            g.current_user = user
            g.current_user_token = authorization_token

            app.logger.info('Token Authentication SUCCESSFUL! The CURRENT USER is {}'.format(user))
        return f(*args, **kwargs)
    return decorated
