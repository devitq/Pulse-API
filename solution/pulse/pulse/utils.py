from rest_framework.views import exception_handler


def wrap_error_into_reason(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        custom_response = {"reason": str(response.data)}
        response.data = custom_response

    return response
