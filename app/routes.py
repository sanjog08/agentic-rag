

def add_resources():
    from app.resources import (
        healthCheck, sendMessage, loginSignup, userConversations, conversationHistory
    )
    from app import api

    api.add_resource(healthCheck.DefaultRoute, '/')

    api.add_resource(healthCheck.HealthCheck, '/health-check')

    api.add_resource(loginSignup.UserRegister, '/register')

    api.add_resource(loginSignup.UserLogin, '/login')

    api.add_resource(sendMessage.SendMessage, '/send', '/send/')

    api.add_resource(userConversations.UserConversations, '/user-threads', '/user-threads/')

    api.add_resource(conversationHistory.ConversationHistory, '/conversation-history', '/conversation-history/')