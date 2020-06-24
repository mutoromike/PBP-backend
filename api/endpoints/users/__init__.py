"""setup user resource blueprint."""


def users_bp(Api, Blueprint):
    from .models import User
    from .users import UserAPI, UsersAPI

    users_bp_service = Blueprint('users_api', __name__)
    users_api = Api(users_bp_service)

    # user endpoints
    users_api.add_resource(
        UserAPI,
        '/auth/register',
        '/auth/register/',
        endpoint='register',
        resource_class_kwargs={
            'User': User
        }
    )
    users_api.add_resource(
        UserAPI,
        '/auth/login',
        '/auth/login/',
        endpoint='login',
        resource_class_kwargs={
            'User': User
        }
    )
    users_api.add_resource(
        UsersAPI,
        '/users/profile',
        '/users/profile/',
        endpoint='users_info',
        resource_class_kwargs={
            'User': User
        }
    )
    return users_bp_service
