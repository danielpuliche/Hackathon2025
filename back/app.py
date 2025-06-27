"""
Aplicación principal Flask - Impulsa EDU-Tech Chatbot
Universidad Cooperativa de Colombia - Campus Popayán
"""
import sys
import os

# Agregar el directorio src al path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from flask import Flask
from flask_cors import CORS

from src.config import config
from src.services import ChatbotService, ChatHistoryDB
from src.routes import create_chatbot_routes, create_conversation_routes

def create_app(config_name: str = 'default') -> Flask:
    """Factory function para crear la aplicación Flask"""
    
    # Crear instancia de Flask
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object(config[config_name])
    
    # Configurar CORS
    CORS(app)
    
    # Inicializar servicios
    app_config = config[config_name]()
    chatbot_service = ChatbotService(app_config)
    chat_db = ChatHistoryDB()
    
    # Crear directorio de historial de chat
    os.makedirs(app_config.CHAT_HISTORY_DIR, exist_ok=True)
    
    # Registrar blueprints
    app.register_blueprint(create_chatbot_routes(chatbot_service))
    app.register_blueprint(create_conversation_routes(chat_db))
    
    # Importar configuración de colores para endpoint
    from src.config.colors import get_theme_config
    
    # Endpoint para configuración de tema
    @app.route('/theme', methods=['GET'])
    def get_theme():
        """Endpoint para obtener configuración de tema y colores"""
        return {
            "theme": get_theme_config(),
            "version": "2.0.0",
            "university": "Universidad Cooperativa de Colombia - Campus Popayán"
        }
    
    # Ruta de salud
    @app.route('/health', methods=['GET'])
    def health_check():
        """Endpoint de verificación de salud"""
        return {
            "status": "healthy",
            "service": "Impulsa EDU-Tech Chatbot",
            "campus": "Popayán",
            "mongodb_connected": chat_db.is_connected(),
            "cohere_configured": bool(app_config.COHERE_API_KEY)
        }
    
    # Ruta raíz
    @app.route('/', methods=['GET'])
    def root():
        """Endpoint raíz con información del servicio"""
        return {
            "message": "Impulsa EDU-Tech Chatbot API",
            "description": "Asistente virtual para la Universidad Cooperativa de Colombia - Campus Popayán",
            "version": "2.0",
            "endpoints": {
                "health": "/health",
                "theme": "/theme (GET)",
                "ask": "/ask (POST)",
                "conversations": "/conversations (GET)",
                "conversation_detail": "/conversations/{id} (GET, DELETE)",
                "conversations_by_label": "/conversations/by-label/{label} (GET)"
            }
        }
    
    return app

def main():
    """Función principal para ejecutar la aplicación"""
    # Determinar configuración basada en variable de entorno
    config_name = os.getenv('FLASK_ENV', 'development')
    if config_name not in config:
        config_name = 'default'
    
    # Crear aplicación
    app = create_app(config_name)
    app_config = config[config_name]()
    
    # Ejecutar aplicación
    print(f"🚀 Iniciando Impulsa EDU-Tech Chatbot")
    print(f"🏫 Campus: Popayán")
    print(f"🌐 Servidor: http://{app_config.HOST}:{app_config.PORT}")
    print(f"⚙️  Configuración: {config_name}")
    
    app.run(
        host=app_config.HOST,
        port=app_config.PORT,
        debug=app_config.DEBUG
    )

if __name__ == '__main__':
    main()
