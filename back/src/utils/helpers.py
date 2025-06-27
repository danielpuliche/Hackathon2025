"""
Utilidades generales para el proyecto
"""
import os
import json
import unicodedata
from typing import Dict, List, Any

def normalize_text(text: str) -> str:
    """Normalizar texto removiendo tildes y convirtiendo a minúsculas"""
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore').decode('utf-8')
    return text.lower()

def ensure_directory_exists(directory: str) -> None:
    """Crear directorio si no existe"""
    os.makedirs(directory, exist_ok=True)

def save_json_file(data: Dict[str, Any], filepath: str) -> bool:
    """Guardar datos en archivo JSON"""
    try:
        ensure_directory_exists(os.path.dirname(filepath))
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error guardando archivo JSON {filepath}: {e}")
        return False

def load_json_file(filepath: str) -> Dict[str, Any]:
    """Cargar datos desde archivo JSON"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error cargando archivo JSON {filepath}: {e}")
        return {}

def validate_conversation_id(conv_id: str) -> bool:
    """Validar formato del ID de conversación"""
    if not conv_id or not isinstance(conv_id, str):
        return False
    
    # UUID format: 8-4-4-4-12 characters
    import re
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    return bool(re.match(uuid_pattern, conv_id.lower()))

def sanitize_user_input(text: str, max_length: int = 1000) -> str:
    """Sanitizar entrada del usuario"""
    if not text or not isinstance(text, str):
        return ""
    
    # Truncar si es muy largo
    text = text[:max_length]
    
    # Remover caracteres peligrosos básicos
    text = text.replace('<', '&lt;').replace('>', '&gt;')
    
    return text.strip()
