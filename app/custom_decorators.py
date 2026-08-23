

def responsify(status='success', has_error=False, code=200, body=None, errors=None):

    response = {
        "status": status, 
        "hasError": has_error, 
        "data": body, 
        "errors": errors
    }

    if has_error:
        code = 400

    return response, code
