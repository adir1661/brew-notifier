from notifier.consts import ErrorMessages
import requests


def validate_company_url(company_url, error_class):
    try:
        resp = requests.get(company_url)
    except requests.exceptions.RequestException as e:
        raise error_class(ErrorMessages.COMPANY_URL_NOT_VALID)

    if not resp.ok:
        raise error_class(ErrorMessages.COMPANY_URL_NOT_VALID)
