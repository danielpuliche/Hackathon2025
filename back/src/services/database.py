import os
from pymongo import MongoClient
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatHistoryDB:
    def __init__(self):
        # Obtener URI de MongoDB desde variables de entorno
        self.mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        self.database_name = os.getenv("DATABASE_NAME", "chatbot_db")
        self.collection_name = "chat_histories"
        
        try:
            self.client = MongoClient(self.mongo_uri)
            self.db = self.client[self.database_name]
            self.collection = self.db[self.collection_name]
            
            # Verificar conexión
            self.client.admin.command('ping')
            logger.info(f"Conectado exitosamente a MongoDB: {self.database_name}")
            
        except Exception as e:
            logger.error(f"Error conectando a MongoDB: {e}")
            self.client = None
            self.db = None
            self.collection = None

    def is_connected(self):
        """Verificar si hay conexión a MongoDB"""
        return self.client is not None and self.db is not None

    def save_chat_history(self, conversation_id, history, labels, user_type=None):
        """Guardar o actualizar el historial de chat"""
        if not self.is_connected():
            logger.error("No hay conexión a MongoDB")
            return False
            
        try:
            chat_data = {
                "id_chat": conversation_id,
                "history": history,
                "labels": labels,
                "user_type": user_type,
                "updated_at": datetime.utcnow(),
                "created_at": datetime.utcnow()
            }
            
            # Usar upsert para actualizar si existe o crear si no existe
            update_data = {
                "history": history,
                "labels": labels,
                "updated_at": datetime.utcnow()
            }
            
            if user_type is not None:
                update_data["user_type"] = user_type
            
            result = self.collection.update_one(
                {"id_chat": conversation_id},
                {
                    "$set": update_data,
                    "$setOnInsert": {"created_at": datetime.utcnow()}
                },
                upsert=True
            )
            
            logger.info(f"Historial guardado para conversación {conversation_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error guardando historial: {e}")
            return False

    def load_chat_history(self, conversation_id):
        """Cargar historial de chat por ID de conversación"""
        if not self.is_connected():
            logger.error("No hay conexión a MongoDB")
            return None
            
        try:
            result = self.collection.find_one({"id_chat": conversation_id})
            if result:
                return {
                    "id_chat": result["id_chat"],
                    "history": result.get("history", []),
                    "labels": result.get("labels", []),
                    "user_type": result.get("user_type")
                }
            return None
            
        except Exception as e:
            logger.error(f"Error cargando historial: {e}")
            return None

    def get_all_conversations(self, limit=50):
        """Obtener todas las conversaciones (últimas 'limit')"""
        if not self.is_connected():
            logger.error("No hay conexión a MongoDB")
            return []
            
        try:
            conversations = self.collection.find({}, {
                "id_chat": 1,
                "labels": 1,
                "created_at": 1,
                "updated_at": 1,
                "history": {"$slice": -2}  # Solo últimos 2 mensajes para vista previa
            }).sort("updated_at", -1).limit(limit)
            
            return list(conversations)
            
        except Exception as e:
            logger.error(f"Error obteniendo conversaciones: {e}")
            return []

    def delete_conversation(self, conversation_id):
        """Eliminar una conversación"""
        if not self.is_connected():
            logger.error("No hay conexión a MongoDB")
            return False
            
        try:
            result = self.collection.delete_one({"id_chat": conversation_id})
            return result.deleted_count > 0
            
        except Exception as e:
            logger.error(f"Error eliminando conversación: {e}")
            return False

    def get_conversations_by_label(self, label):
        """Obtener conversaciones por etiqueta"""
        if not self.is_connected():
            logger.error("No hay conexión a MongoDB")
            return []
            
        try:
            conversations = self.collection.find(
                {"labels": label},
                {
                    "id_chat": 1,
                    "labels": 1,
                    "created_at": 1,
                    "updated_at": 1,
                    "history": {"$slice": -2}
                }
            ).sort("updated_at", -1)
            
            return list(conversations)
            
        except Exception as e:
            logger.error(f"Error obteniendo conversaciones por etiqueta: {e}")
            return []

    def close_connection(self):
        """Cerrar conexión a MongoDB"""
        if self.client:
            self.client.close()
            logger.info("Conexión a MongoDB cerrada")
