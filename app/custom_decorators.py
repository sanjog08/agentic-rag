from functools import wraps
from flask import request
from datetime import  timedelta, datetime
import jwt
import json
import config
from app.custom_exception import *
from app.exceptions.Exceptions import InvalidRequestError, InternalServerError
import logging

logger = logging.getLogger(__name__)


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



def authenticate():
    """Returns user_id for the conversation thread"""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            """Checks & verifies the user token and remaining session time"""
            # get the token
            jwt_token = request.headers.get('jwt')
            url = request.path
            datetime_deco = datetime.now()
            datetime_req = int(datetime_deco.timestamp())

            if not jwt_token:
                return responsify(has_error=True, errors="JWT token is missing in request.")

            # decode the token
            payload = jwt.decode(jwt_token, config.JWT_SECRET, algorithms=['HS256'])
            user_name = payload.get('name')
            user_email = user_id = payload.get('email')
            session_valid_till = payload.get('token_validity')

            if datetime_req > session_valid_till:
                return responsify(has_error=True, errors="session expire login to continue")

            kwargs['user_name'] = user_name
            kwargs['user_email'] = user_email
            kwargs['user_id'] = user_id

            response = f(*args, **kwargs)
            return response

        return decorated_function

    return decorator


def exception_handler():
    """Decorator for Exception Handling on API Endpoints."""

    def decorator(f):

        @wraps(f)
        def decorated_function(*args, **kwargs):
            module = "Unhandled Error"
            start_time = datetime.now()
            try:
                module = f"Unhandled Error in {args[0].__class__.__name__}.{f.__name__} API"
                request_data = {"path": request.path, "body": request.get_json(silent=True), "form": request.form.to_dict()}
            except Exception as E:
                request_data = str(E)
                logger.error(f"Exception occurred in exception_handler decorator - {str(E)}")

            try:
                _return = f(*args, **kwargs)
                return _return
            except KeyError as E:
                payload = {"args": args, "kwargs": kwargs, "request": request_data, "api_time": datetime.now() - start_time}
                return internal_server_error(message=E, errors=str(E.args[0]) + " Key is missing", code=400, module=module, payload=payload)
            except InvalidRequestError as E:
                payload = {"args": args, "kwargs": kwargs, "request": request_data, "api_time": datetime.now() - start_time}
                return internal_server_error(message=E, errors=E.message, code=400, module=module, payload=payload)
            except Exception as E:
                logger.error(E)
                payload = {"args": args, "kwargs": kwargs, "request": request_data, "api_time": datetime.now() - start_time}
                return internal_server_error(message=E, module=module, payload=payload)

        return decorated_function

    return decorator
