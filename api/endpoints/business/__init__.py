"""setup business resource blueprint."""


def business_bp(Api, Blueprint):
    from .models import Business, Country, Transaction
    from .business import BusinessAPI, ProcessCsvAPI

    business_bp_service = Blueprint('business_api', __name__)
    business_api = Api(business_bp_service)

    # user endpoints
    business_api.add_resource(
        BusinessAPI,
        '/business',
        '/business/',
        '/business/<string:business_id>',
        '/business/<string:business_id>/',
        endpoint='business',
        resource_class_kwargs={
            'Business': Business,
            'Country': Country
        }
    )

    business_api.add_resource(
        ProcessCsvAPI,
        '/data-upload',
        '/data-upload/',
        '/analytics',
        '/analytics/',
        endpoint='data_upload',
        resource_class_kwargs={
            "Transaction": Transaction,
            'Business': Business,
        }
    )
    return business_bp_service
