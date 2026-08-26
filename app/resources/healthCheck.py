from app.resources import *


class DefaultRoute(Resource):

    def get(self):
        return jsonify({"message": "Service available! 24X7!"})

class HealthCheck(Resource):

    def get(self):
        return jsonify({"message": "ChatBot running!!!"})
