from rest_framework.exceptions import APIException
from rest_framework import status
import stripe
import logging


class StripeException(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE


class ErrorHandler:

    logger = logging.getLogger(__name__)

    def create_error(self, exception):
        self.logger.error(exception.json_body)
        if getattr(exception, "__module__") == stripe.error.__name__:
            raise StripeException()
        else:
            raise APIException()
