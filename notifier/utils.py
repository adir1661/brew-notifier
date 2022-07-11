from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

from notifier.consts import ErrorMessages
import requests


def validate_company_url(company_url, drf=False):
    try:
        resp = requests.get(company_url)
    except requests.exceptions.RequestException as e:
        if drf:
            raise DRFValidationError(ErrorMessages.COMPANY_URL_NOT_VALID)
        raise DjangoValidationError(ErrorMessages.COMPANY_URL_NOT_VALID)

    if not resp.ok:
        if drf:
            raise DRFValidationError(ErrorMessages.COMPANY_URL_NOT_VALID)
        raise DjangoValidationError(ErrorMessages.COMPANY_URL_NOT_VALID)
