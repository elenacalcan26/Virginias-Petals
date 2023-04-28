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