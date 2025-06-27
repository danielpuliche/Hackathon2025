"""
Constantes y configuración del chatbot
"""
from src.models.chat_models import TopicKeywords
from .colors import COLORS, CHAT_THEME, STATUS_COLORS

# Palabras clave para detección de temas
TOPIC_KEYWORDS = [
    TopicKeywords("Matrículas", ["matricula", "matrícula", "matricular", "inscripción", "inscribir"]),
    TopicKeywords("Admisiones", ["admisión", "admisiones", "admitido", "inscripción", "inscribir"]),
    TopicKeywords("Biblioteca", ["biblioteca", "libro", "préstamo", "prestamo", "devolver"]),
    TopicKeywords("Pagos", ["pago", "pagos", "cuota", "factura", "recibo"]),
    TopicKeywords("Programas", ["programa", "carrera", "ingeniería", "derecho", "medicina"]),
    TopicKeywords("Becas", ["beca", "becas", "descuento", "financiamiento"]),
    TopicKeywords("Calendario", ["calendario", "fechas", "cronograma"]),
    TopicKeywords("Soporte", ["soporte", "ayuda", "problema", "error", "contacto"]),
]

# Enlaces informativos por tema
ENLACES_INFO = {
    "programas": "https://www.ucc.edu.co/programas",
    "credito": "https://www.comuna.com.co/sscgucc.php",
    "inscripciones": "https://www.ucc.edu.co/inscripciones",
    "admisiones": "https://www.ucc.edu.co/estudiante/admisiones-registro-cad/Paginas/admisiones-registro-cad.aspx",
    "biblioteca": "https://www.ucc.edu.co/biblioteca",
    "contacto": "https://www.ucc.edu.co/Paginas/Contacto.aspx",
    "virtual": "https://www.ucc.edu.co/programas/educacion-virtual/Paginas/pregrados-virtuales.aspx",
    "campus": "https://campusvirtual.ucc.edu.co/d2l/loginh/",
}

# Enlace por defecto
DEFAULT_LINK = "https://www.ucc.edu.co/campus-popayan"
