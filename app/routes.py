

def add_resources():
    from app.resources import (
        healthCheck, sendMessage
    )
    from app import api

    api.add_resource(healthCheck.HealthCheck, '/')

    api.add_resource(sendMessage.SendMessage, '/send', '/send/')