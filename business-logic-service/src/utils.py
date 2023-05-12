from http import HTTPStatus
import requests

auth_url = "http://auth-service:8081"
core_url = "http://core-service:7000"


def verify_request_body(body, fields):
    """
        Verifies the existence of a list of arguments in a request body.

        Returns True if the body contains only the parameters given. Otherwise, returns False.
    """

    if len(body) != len(fields):
        return False

    for field in fields:
        if not field in body:
            return False

    return True


def verify_authorization(authorization_header):
    if authorization_header is None:
        return {"status": HTTPStatus.FORBIDDEN}

    auth_headers = {
        "Authorization": authorization_header
    }

    auth_validation = requests.get(
        f"{auth_url}/api/current-user", headers=auth_headers)

    if auth_validation.status_code != HTTPStatus.OK:
        return {"status": HTTPStatus.FORBIDDEN}

    current_user = auth_validation.json()

    return {"status": HTTPStatus.OK, "user": current_user}
