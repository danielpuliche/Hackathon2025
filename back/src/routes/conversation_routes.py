"""
Rutas para gestión de conversaciones
"""
from flask import Blueprint, request, jsonify
from src.services.database import ChatHistoryDB

def create_conversation_routes(chat_db: ChatHistoryDB) -> Blueprint:
    """Crear blueprint con las rutas de gestión de conversaciones"""
    
    conversation_bp = Blueprint('conversations', __name__)
    
    @conversation_bp.route('/conversations', methods=['GET'])
    def get_conversations():
        """Obtener todas las conversaciones"""
        if not chat_db.is_connected():
            return jsonify({"error": "MongoDB no está disponible"}), 500
        
        limit = request.args.get('limit', 50, type=int)
        conversations = chat_db.get_all_conversations(limit)
        
        # Convertir ObjectId a string para JSON serialization
        for conv in conversations:
            if '_id' in conv:
                conv['_id'] = str(conv['_id'])
        
        return jsonify({"conversations": conversations})
    
    @conversation_bp.route('/conversations/<conversation_id>', methods=['GET'])
    def get_conversation(conversation_id):
        """Obtener una conversación específica"""
        if not chat_db.is_connected():
            return jsonify({"error": "MongoDB no está disponible"}), 500
        
        conversation = chat_db.load_chat_history(conversation_id)
        if conversation:
            return jsonify(conversation)
        else:
            return jsonify({"error": "Conversación no encontrada"}), 404
    
    @conversation_bp.route('/conversations/<conversation_id>', methods=['DELETE'])
    def delete_conversation(conversation_id):
        """Eliminar una conversación"""
        if not chat_db.is_connected():
            return jsonify({"error": "MongoDB no está disponible"}), 500
        
        success = chat_db.delete_conversation(conversation_id)
        if success:
            return jsonify({"message": "Conversación eliminada exitosamente"})
        else:
            return jsonify({"error": "No se pudo eliminar la conversación"}), 404
    
    @conversation_bp.route('/conversations/by-label/<label>', methods=['GET'])
    def get_conversations_by_label(label):
        """Obtener conversaciones por etiqueta"""
        if not chat_db.is_connected():
            return jsonify({"error": "MongoDB no está disponible"}), 500
        
        conversations = chat_db.get_conversations_by_label(label)
        
        # Convertir ObjectId a string para JSON serialization
        for conv in conversations:
            if '_id' in conv:
                conv['_id'] = str(conv['_id'])
        
        return jsonify({"conversations": conversations, "label": label})
    
    @conversation_bp.route('/conversations/cleanup-tests', methods=['DELETE'])
    def cleanup_test_conversations():
        """Eliminar todas las conversaciones de test"""
        if not chat_db.is_connected():
            return jsonify({"error": "MongoDB no está disponible"}), 500
        
        try:
            # Limpiar de MongoDB
            result = chat_db.collection.delete_many({
                "id_chat": {"$regex": "^test_"}
            })
            
            return jsonify({
                "message": f"Eliminadas {result.deleted_count} conversaciones de test",
                "method": "mongodb_cleanup"
            })
            
        except Exception as e:
            return jsonify({"error": f"Error limpiando conversaciones de test: {e}"}), 500
    
    return conversation_bp
