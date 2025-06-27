"""
Modelos de datos para el chatbot
"""
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

@dataclass
class ChatMessage:
    """Modelo para un mensaje individual del chat"""
    role: str  # "User" o "Chatbot"
    message: str
    timestamp: Optional[datetime] = None
    
    def to_dict(self) -> Dict:
        """Convertir a diccionario para JSON"""
        return asdict(self)

@dataclass
class ChatConversation:
    """Modelo para una conversación completa"""
    id_chat: str
    history: List[Dict]
    labels: List[str]
    created_at: datetime
    updated_at: datetime
    
    def to_dict(self) -> Dict:
        """Convertir a diccionario para JSON"""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat() if self.created_at else None
        data['updated_at'] = self.updated_at.isoformat() if self.updated_at else None
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ChatConversation':
        """Crear instancia desde diccionario"""
        return cls(
            id_chat=data.get('id_chat', ''),
            history=data.get('history', []),
            labels=data.get('labels', []),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )

@dataclass
class TopicKeywords:
    """Modelo para las palabras clave de temas"""
    label: str
    keywords: List[str]
    
    def to_dict(self) -> Dict:
        """Convertir a diccionario"""
        return asdict(self)
