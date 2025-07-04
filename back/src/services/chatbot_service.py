"""
Servicio principal del chatbot
"""
import cohere
import uuid
import re
import unicodedata
from typing import List, Tuple, Optional

from src.config.settings import Config
from src.config.constants import TOPIC_KEYWORDS, ENLACES_INFO, DEFAULT_LINK
from src.services.database import ChatHistoryDB
from src.models.chat_models import ChatMessage, ChatConversation

class ChatbotService:
    """Servicio principal para manejo del chatbot"""
    
    def __init__(self, config: Config):
        self.config = config
        self.cohere_client = cohere.Client(config.COHERE_API_KEY) if config.COHERE_API_KEY else None
        self.chat_db = ChatHistoryDB()
    
    def normalize_text(self, text: str) -> str:
        """Normalizar texto removiendo tildes y convirtiendo a minúsculas"""
        text = unicodedata.normalize('NFD', text)
        text = text.encode('ascii', 'ignore').decode('utf-8')
        return text.lower()
    
    def detect_labels(self, text: str) -> List[str]:
        """Detectar etiquetas/temas en el texto"""
        found = []
        norm_text = self.normalize_text(text)
        
        for topic in TOPIC_KEYWORDS:
            for keyword in topic.keywords:
                norm_keyword = self.normalize_text(keyword)
                # Buscar palabra completa o raíz
                if re.search(rf"\b{re.escape(norm_keyword)}[a-z]*\b", norm_text):
                    found.append(topic.label)
                    break
        
        return found
    
    def find_relevant_link(self, question: str) -> str:
        """Encontrar enlace relevante basado en la pregunta"""
        question_norm = self.normalize_text(question)
        
        for tema, url in ENLACES_INFO.items():
            if self.normalize_text(tema) in question_norm:
                return url
        
        return DEFAULT_LINK
    
    def load_or_create_conversation(self, conv_id: Optional[str] = None) -> Tuple[str, List[dict], List[str], Optional[str]]:
        """Cargar conversación existente o crear una nueva"""
        labels = []
        user_type = None
        
        if conv_id and self.chat_db.is_connected():
            # Intentar cargar desde MongoDB
            chat_data = self.chat_db.load_chat_history(conv_id)
            if chat_data:
                return (
                    chat_data.get("id_chat", conv_id), 
                    chat_data.get("history", []), 
                    chat_data.get("labels", []),
                    chat_data.get("user_type")
                )
        
        # Crear nueva conversación
        if not conv_id:
            conv_id = str(uuid.uuid4())
        
        return conv_id, [], [], None
    
    def save_conversation(self, conv_id: str, history: List[dict], labels: List[str], user_type: Optional[str] = None) -> bool:
        """Guardar conversación en la base de datos"""
        if self.chat_db.is_connected():
            return self.chat_db.save_chat_history(conv_id, history, labels, user_type)
        return False
    
    def generate_response(self, question: str, conv_id: Optional[str] = None, user_type: Optional[str] = None) -> dict:
        """Generar respuesta del chatbot"""
        if not self.cohere_client:
            return {
                "answer": "No se encontró la clave API de Cohere. Configúrala en el archivo .env como COHERE_API_KEY.",
                "conversation_id": conv_id or str(uuid.uuid4()),
                "history": [],
                "labels": [],
                "user_type": None,
                "needs_user_type": False
            }
        
        # Cargar o crear conversación
        conv_id, chat_history, labels, existing_user_type = self.load_or_create_conversation(conv_id)
        
        # Si se proporciona user_type, actualizarlo
        if user_type:
            existing_user_type = user_type
        
        # Si es una nueva conversación o no hay tipo de usuario, pedirlo
        if not existing_user_type and not user_type:
            # Es la primera interacción y necesitamos el tipo de usuario
            if not chat_history:  # Primera interacción
                return {
                    "answer": "¡Hola! Soy tu asistente virtual de Impulsa EDU-Tech para la Universidad Cooperativa de Colombia. Para brindarte la mejor atención, por favor selecciona tu tipo de usuario:",
                    "conversation_id": conv_id,
                    "history": [],
                    "labels": [],
                    "user_type": None,
                    "needs_user_type": True,
                    "user_options": ["Estudiante", "Docente", "Administrativo", "Externo"]
                }
            
            # Si ya hay historial pero no hay tipo de usuario (caso raro)
            if question.lower() not in ['estudiante', 'docente', 'administrativo', 'externo']:
                return {
                    "answer": "Para continuar, necesito que selecciones tu tipo de usuario: Estudiante, Docente, Administrativo o Externo.",
                    "conversation_id": conv_id,
                    "history": chat_history,
                    "labels": labels,
                    "user_type": None,
                    "needs_user_type": True,
                    "user_options": ["Estudiante", "Docente", "Administrativo", "Externo"]
                }
        
        # Agregar pregunta al historial
        if question.strip():
            chat_history.append({"role": "User", "message": question})
            
            # Detectar nuevas etiquetas
            found_labels = self.detect_labels(question)
            for label in found_labels:
                if label not in labels:
                    labels.append(label)
        
        # Si es selección de tipo de usuario
        question_lower = question.lower()
        if question_lower in ['estudiante', 'docente', 'administrativo', 'externo'] and not existing_user_type:
            existing_user_type = question.capitalize()
            
            welcome_message = f"¡Perfecto! Te doy la bienvenida como {existing_user_type}. ¿En qué puedo ayudarte hoy?"
            
            chat_history.append({"role": "Chatbot", "message": welcome_message})
            
            # Guardar conversación con tipo de usuario
            self.save_conversation(conv_id, chat_history, labels, existing_user_type)
            
            return {
                "answer": welcome_message,
                "conversation_id": conv_id,
                "history": chat_history,
                "labels": labels,
                "user_type": existing_user_type,
                "needs_user_type": False
            }
        
        # Encontrar enlace relevante
        enlace = self.find_relevant_link(question)
        enlace_final = enlace.rstrip('.')
        
        try:
            # Generar prompt para Cohere incluyendo el tipo de usuario
            user_context = f"El usuario es un {existing_user_type.lower()} de la universidad." if existing_user_type else ""
            
            prompt = (
                f"Eres un asistente virtual para la Universidad Cooperativa de Colombia, "
                f"específicamente en el campus de Popayán. {user_context} "
                f"Responde en máximo {self.config.MAX_WORDS} palabras. "
                f"Al final, cuando se haya realizado una pregunta agrega este enlace para más información: {enlace_final} "
                f"No lo agregues en cualquier otro caso.\n\n"
                f"Pregunta: {question}"
            )
            
            # Llamar a Cohere
            response = self.cohere_client.chat(
                model="command-r-plus",
                message=prompt,
                chat_history=chat_history,
                temperature=self.config.TEMPERATURE,
                max_tokens=self.config.MAX_TOKENS
            )
            
            answer = response.text
            
            # Guardar respuesta si no es error
            if answer and not answer.startswith("Error"):
                chat_history.append({"role": "Chatbot", "message": answer})
            
            # Guardar conversación
            self.save_conversation(conv_id, chat_history, labels, existing_user_type)
            
        except Exception as e:
            answer = f"Error al consultar Cohere: {e}"
        
        return {
            "answer": answer,
            "conversation_id": conv_id,
            "history": chat_history,
            "labels": labels,
            "user_type": existing_user_type,
            "needs_user_type": False
        }
