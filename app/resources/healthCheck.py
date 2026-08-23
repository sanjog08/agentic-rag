from app.resources import *

class HealthCheck(Resource):

    def get(self):
        return jsonify({"message": "ChatBot running!!!"})
