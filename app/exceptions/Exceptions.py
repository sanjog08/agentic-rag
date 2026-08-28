class AppError(Exception):
    status_code = 500
    status = "Failure"

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status'] = self.status
        return rv


class InvalidRequestError(AppError):
    def __init__(self, message="Invalid Request", status_code=400, payload=None):
        AppError.__init__(self, message, status_code, payload)


class InternalServerError(AppError):
    def __init__(self, message="Something went wrong.", status_code=500, payload=None):
        AppError.__init__(self, message, status_code, payload)