"""setup business resource blueprint."""


def business_bp(Api, Blueprint):
    from .models import Business, Country
    from .business import BusinessAPI

    business_bp_service = Blueprint('business_api', __name__)
    business_api = Api(business_bp_service)

    # user endpoints
    business_api.add_resource(
        BusinessAPI,
        '/business',
        '/business/',
        endpoint='business',
        resource_class_kwargs={
            'Business': Business,
            'Country': Country
        }
    )
    return business_bp_service
