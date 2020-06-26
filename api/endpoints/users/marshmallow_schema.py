from datetime import date
from marshmallow import (ValidationError, fields, post_load, validate,
                         validates_schema)

from api.utils.marshmallow_schemas import BaseSchema

from .models import User


class RegisterSchema(BaseSchema):
    """Creates a validation schema for user registration."""

    first_name = fields.String(
        required=True,
        validate=validate.Length(min=3),
        error_messages={
            'required': {'message': 'User first name is required.'}
        })
    last_name = fields.String(
        required=True,
        validate=validate.Length(min=3),
        error_messages={
            'required': {'message': 'User last name is required.'}
        })
    email = fields.Email(
        required=True,
        error_messages={
            'required': {'message': 'User email is required.'}
        })
    password = fields.String(
        required=True,
        validate=validate.Length(min=3),
        error_messages={
            'required': {'message': 'User password is required.'}
        })

    @post_load
    def verify_user(self, data, **kwargs):
        """Extra validation for the Register User Schema."""
        user = User.query.filter_by(email=data['email']).first()

        if user:
            self.context = {'status_code': 409}
            raise ValidationError({'message': 'User with that email already exists!'})



register_user_schema = RegisterSchema()
