"""
Custom exception handler and response utilities
"""
import traceback
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException
from .logging_config import get_logger

logger = get_logger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler for API responses.
    Returns standardized response format and logs the full traceback so
    every unhandled exception is visible in Railway deployment logs.
    """
    view = context.get('view')
    view_name = type(view).__name__ if view else 'unknown view'

    if isinstance(exc, APIException):
        detail = exc.detail
        status_code = exc.status_code
        # Log 5xx errors as ERROR, 4xx as WARNING
        if status_code >= 500:
            logger.error(
                'APIException in %s [HTTP %s]: %s\n%s',
                view_name, status_code, detail,
                traceback.format_exc(),
            )
        else:
            logger.warning(
                'APIException in %s [HTTP %s]: %s',
                view_name, status_code, detail,
            )
    else:
        detail = str(exc)
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        logger.error(
            'Unhandled exception in %s: %s\n%s',
            view_name, detail,
            traceback.format_exc(),
        )

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
