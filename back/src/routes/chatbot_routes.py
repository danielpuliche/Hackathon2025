"""
Rutas para el chatbot
"""
from flask import Blueprint, request, jsonify
from src.services.chatbot_service import ChatbotService

def create_chatbot_routes(chatbot_service: ChatbotService) -> Blueprint:
    """Crear blueprint con las rutas del chatbot"""
    
    chatbot_bp = Blueprint('chatbot', __name__)
    
    @chatbot_bp.route('/ask', methods=['POST'])
    def ask():
        """Endpoint principal para hacer preguntas al chatbot"""
        data = request.get_json()
        question = data.get("question", "")
        conv_id = data.get("conversation_id")
        
        response = chatbot_service.generate_response(question, conv_id)
        return jsonify(response)
    
    return chatbot_bp
