"""
Custom exception handler and response utilities
"""
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException


def custom_exception_handler(exc, context):
    """
    Custom exception handler for API responses.
    Returns standardized response format.
    """
    if isinstance(exc, APIException):
        detail = exc.detail
        status_code = exc.status_code
    else:
        detail = str(exc)
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    response_data = {
        'status': 'error',
        'message': detail if isinstance(detail, str) else str(detail),
        'data': None
    }

    return Response(response_data, status=status_code)


class StandardResponse:
    """Standard response formatter."""

    @staticmethod
    def success(message='Success', data=None, status_code=status.HTTP_200_OK):
        """Return success response."""
        return Response(
            {
                'status': 'success',
                'message': message,
                'data': data
            },
            status=status_code
        )

    @staticmethod
    def error(message='Error', status_code=status.HTTP_400_BAD_REQUEST):
        """Return error response."""
        return Response(
            {
                'status': 'error',
                'message': message,
                'data': None
            },
            status=status_code
        )
