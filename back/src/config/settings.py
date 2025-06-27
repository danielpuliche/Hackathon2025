"""
Configuración principal de la aplicación Flask
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración base"""
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "supersecretkey")
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "chatbot_db")
    
    # Configuración de Telegram
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/ask")
    
    # Configuración de Flask
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    HOST = os.getenv("FLASK_HOST", "0.0.0.0")
    PORT = int(os.getenv("FLASK_PORT", "8000"))
    TELEGRAM_PORT = int(os.getenv("TELEGRAM_PORT", "9000"))
    
    # Configuración del chatbot
    CHAT_HISTORY_DIR = "chat_histories"
    MAX_TOKENS = 300
    TEMPERATURE = 0.2
    MAX_WORDS = 100

class DevelopmentConfig(Config):
    """Configuración de desarrollo"""
    DEBUG = True

class ProductionConfig(Config):
    """Configuración de producción"""
    DEBUG = False

# Configuración por defecto
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
