from flask import Flask, request, jsonify, session
from flask_cors import CORS
import os
from dotenv import load_dotenv
import cohere
import uuid
import json
import unicodedata
import re

load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecretkey")  # Necesario para sesiones

# Diccionario simple de temas y palabras clave
TOPIC_KEYWORDS = [
    {"label": "Matrículas", "keywords": ["matricula", "matrícula", "matricular", "inscripción", "inscribir"]},
    {"label": "Admisiones", "keywords": ["admisión", "admisiones", "admitido", "inscripción", "inscribir"]},
    {"label": "Biblioteca", "keywords": ["biblioteca", "libro", "préstamo", "prestamo", "devolver"]},
    {"label": "Pagos", "keywords": ["pago", "pagos", "cuota", "factura", "recibo"]},
    {"label": "Programas", "keywords": ["programa", "carrera", "ingeniería", "derecho", "medicina"]},
    {"label": "Becas", "keywords": ["beca", "becas", "descuento", "financiamiento"]},
    {"label": "Calendario", "keywords": ["calendario", "fechas", "cronograma"]},
    {"label": "Soporte", "keywords": ["soporte", "ayuda", "problema", "error", "contacto"]},
]

CHAT_HISTORY_DIR = "chat_histories"
os.makedirs(CHAT_HISTORY_DIR, exist_ok=True)

def normalize(text):
    # Quita tildes y pasa a minúsculas
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore').decode('utf-8')
    return text.lower()

def detect_labels(text):
    found = []
    norm_text = normalize(text)
    for topic in TOPIC_KEYWORDS:
        for k in topic["keywords"]:
            norm_k = normalize(k)
            # Buscar palabra completa o raíz (por ejemplo, "matricula" detecta "matriculas", "matricular")
            if re.search(rf"\b{re.escape(norm_k)}[a-z]*\b", norm_text):
                found.append(topic["label"])
                break
    return found

@app.route('/ask', methods=['POST'])
def ask():
    if not COHERE_API_KEY:
        return jsonify({"answer": "No se encontró la clave API de Cohere. Configúrala en el archivo .env como COHERE_API_KEY."})

    data = request.get_json()
    question = data.get("question", "")
    conv_id = data.get("conversation_id")

    # Cargar historial desde archivo si existe, si no, crear uno nuevo
    chat_file = os.path.join(CHAT_HISTORY_DIR, f"chat_history_{conv_id}.json") if conv_id else None
    labels = []
    if chat_file and os.path.exists(chat_file):
        with open(chat_file, "r", encoding="utf-8") as f:
            chat_data = json.load(f)
        chat_history = chat_data.get("history", [])
        conv_id = chat_data.get("id_chat", conv_id)
        labels = chat_data.get("labels", [])
    else:
        if not conv_id:
            conv_id = str(uuid.uuid4())
        chat_history = []
        labels = []

    # Agregar la pregunta al historial
    if question.strip():
        chat_history.append({"role": "User", "message": question})
        # Detectar etiquetas y agregarlas si no existen
        found_labels = detect_labels(question)
        for label in found_labels:
            if label not in labels:
                labels.append(label)

    enlaces_info = {
        "programas": "https://www.ucc.edu.co/programas",
        "credito": "https://www.comuna.com.co/sscgucc.php",
        "inscripciones": "https://www.ucc.edu.co/inscripciones",
        "admisiones": "https://www.ucc.edu.co/estudiante/admisiones-registro-cad/Paginas/admisiones-registro-cad.aspx",
        "biblioteca": "https://www.ucc.edu.co/biblioteca",
        "contacto": "https://www.ucc.edu.co/Paginas/Contacto.aspx",
        "virtual": "https://www.ucc.edu.co/programas/educacion-virtual/Paginas/pregrados-virtuales.aspx",
        "campus": "https://campusvirtual.ucc.edu.co/d2l/loginh/",
        # ...agrega más temas y enlaces según necesidad...
    }
    # Buscar enlace relevante usando normalización robusta
    pregunta_norm = normalize(question)
    enlace = "https://www.ucc.edu.co/campus-popayan"
    for tema, url in enlaces_info.items():
        if normalize(tema) in pregunta_norm:
            enlace = url
            break

    co = cohere.Client(COHERE_API_KEY)
    try:
        # Quitar punto final solo si el enlace está al final del mensaje
        enlace_final = enlace.rstrip('.')
        prompt = (
            f"Eres un asistente virtual para la Universidad Cooperativa de Colombia, específicamente en el campus de Popayán. Responde en máximo 60 palabras. Al final, cuando se haya realizado una pregunta agrega este enlace para más información: {enlace_final} No lo agregues en cualquier otro caso.\n\n"
            f"Pregunta: {question}"
        )
        response = co.chat(
            model="command-r-plus",
            message=prompt,
            chat_history=chat_history,
            temperature=0.2,
            max_tokens=300
        )
        answer = response.text
        # Guardar respuesta solo si no es error
        if answer and not answer.startswith("Error"):
            chat_history.append({"role": "Chatbot", "message": answer})
        # Guardar historial en archivo local con formato solicitado
        chat_data = {"id_chat": conv_id, "history": chat_history, "labels": labels}
        with open(os.path.join(CHAT_HISTORY_DIR, f"chat_history_{conv_id}.json"), "w", encoding="utf-8") as f:
            json.dump(chat_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        answer = f"Error al consultar Cohere: {e}"
    return jsonify({"answer": answer, "conversation_id": conv_id, "history": chat_history, "labels": labels})

if __name__ == '__main__':
    app.run(debug=True, port=8000)
