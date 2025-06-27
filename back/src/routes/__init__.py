"""
Rutas de la API REST
"""
from .chatbot_routes import create_chatbot_routes
from .conversation_routes import create_conversation_routes

__all__ = [
    'create_chatbot_routes',
    'create_conversation_routes'
]

