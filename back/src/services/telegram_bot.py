"""
Servicio de Bot de Telegram para Impulsa EDU-Tech
Universidad Cooperativa de Colombia - Campus Popayán
"""
import os
import sys
import requests
from flask import Flask, request
from flask_cors import CORS

# Agregar el directorio padre al path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.config.settings import Config

class TelegramBotService:
    """Servicio para manejo del bot de Telegram"""
    
    def __init__(self, config: Config):
        self.config = config
        self.token = config.TELEGRAM_TOKEN if hasattr(config, 'TELEGRAM_TOKEN') else os.getenv("TELEGRAM_TOKEN")
        self.backend_url = os.getenv("BACKEND_URL", "http://localhost:8000/ask")
        self.api_url = f"https://api.telegram.org/bot{self.token}"
        
        # Crear app Flask para el webhook
        self.app = Flask(__name__)
        CORS(self.app)
        
        # Registrar rutas
        self._register_routes()
    
    def _register_routes(self):
        """Registrar rutas del webhook"""
        
        @self.app.route(f"/webhook/{self.token}", methods=["POST"])
        def telegram_webhook():
            data = request.get_json()
            if "message" in data:
                chat_id = data["message"]["chat"]["id"]
                text = data["message"].get("text", "")
                
                # Usar el chat_id como conversation_id para mantener contexto
                payload = {
                    "question": text, 
                    "conversation_id": f"telegram_{chat_id}"
                }
                
                try:
                    response = requests.post(
                        self.backend_url, 
                        json=payload, 
                        timeout=10,
                        headers={'Content-Type': 'application/json'}
                    )
                    
                    if response.status_code == 200:
                        answer = response.json().get("answer", "Lo siento, hubo un error.")
                    else:
                        answer = "Lo siento, hubo un error en el servidor."
                        
                except requests.exceptions.RequestException as e:
                    answer = f"Lo siento, no pude conectar con el servidor. Error: {str(e)}"
                except Exception as e:
                    answer = f"Lo siento, hubo un error inesperado: {str(e)}"
                
                self.send_message(chat_id, answer)
            
            return {"status": "ok"}
        
        @self.app.route("/health", methods=["GET"])
        def health():
            """Endpoint de salud del bot"""
            return {
                "status": "healthy",
                "service": "Telegram Bot - Impulsa EDU-Tech",
                "token_configured": bool(self.token),
                "backend_url": self.backend_url
            }
    
    def send_message(self, chat_id: str, text: str):
        """Enviar mensaje a Telegram"""
        url = f"{self.api_url}/sendMessage"
        payload = {
            "chat_id": chat_id, 
            "text": text, 
            "parse_mode": "HTML"
        }
        
        try:
            response = requests.post(url, json=payload, timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"Error enviando mensaje: {e}")
            return False
    
    def set_webhook(self, webhook_url: str):
        """Configurar webhook de Telegram"""
        url = f"{self.api_url}/setWebhook"
        payload = {"url": f"{webhook_url}/webhook/{self.token}"}
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"Error configurando webhook: {e}")
            return False
    
    def run(self, host="0.0.0.0", port=9000, debug=False):
        """Ejecutar el servicio del bot"""
        print(f"🤖 Iniciando Telegram Bot en {host}:{port}")
        self.app.run(host=host, port=port, debug=debug)

def create_telegram_app():
    """Factory function para crear la app de Telegram"""
    from src.config.settings import config
    app_config = config['default']()
    bot_service = TelegramBotService(app_config)
    return bot_service.app

if __name__ == "__main__":
    from src.config.settings import config
    
    # Crear servicio
    app_config = config['default']()
    bot_service = TelegramBotService(app_config)
    
    # Ejecutar
    bot_service.run(debug=True)
