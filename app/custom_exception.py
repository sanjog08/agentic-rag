import config
from datetime import datetime
from flask import request




def internal_server_error(errors='Something went wrong', status='fail', has_error=True, code=500, body=None,
                          message=None, module="", payload={}):
    # Sending detailed error alert to viasocket flow for immediate actions
    if module or payload:
        try:
            payload.update({"req_url": request.url, "req_method": request.method, "req_params": dict(request.args)})
        except Exception:
            pass
        data = {"error": str(message) or errors, "alertModule": module, "payload": payload}
        if hasattr(message, "code") and message.code in [400, 404]:
            return message.description, message.code

    try:
        message = "==>>" + request.url_rule.endpoint + "." + request.method + "." + \
                  datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": " + str(message)
    except Exception:
        pass
    response = {"status": status, "hasError": has_error, "data": body, "errors": errors}
    return response, code


def unauthorized_error(errors='Unauthorized', status='fail', has_error=True, code=401, body=None, web=None, clevertap=None):
    message = "==>>" + request.url_rule.endpoint + "." + request.method + "." + \
              datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": " + errors
    # send_error_event_on_space(message, config.ERROR_EXCEPT_500_CHANNEL_ID)
    response = {"status": status, "hasError": has_error, "data": body, "errors": errors}
    if web:
        response = {"status": "whatsapp_rejected", "statusCode": 2005, "message": "Authorization failure"}
    if clevertap:
        code = 200
        response = {"status": "failure",
                    "error": {
                        "code": 2000,
                        "message": "Invalid Credentials"
                    }
                    }
        return response, code
    return response, code
