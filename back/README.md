# 🚀 Impulsa EDU-Tech Backend

**Asistente virtual con IA para la Universidad Cooperativa de Colombia - Campus Popayán**

## 📋 Descripción

Backend moderno desarrollado en **Flask** que proporciona un chatbot inteligente alimentado por **Cohere AI**. Incluye integración con **Telegram Bot** y almacenamiento en **MongoDB** para historiales de conversación.

## 🏗️ Estructura del Proyecto

```
back/
├── app.py                    # Aplicación principal Flask
├── requirements.txt          # Dependencias de Python
├── .env                     # Variables de entorno (no versionado)
├── .env.example             # Plantilla de variables de entorno
│
├── src/                     # Código fuente organizado
│   ├── config/              # Configuración de la aplicación
│   │   ├── settings.py      # Configuraciones por ambiente
│   │   └── constants.py     # Constantes globales
│   │
│   ├── models/              # Modelos de datos
│   │   └── chat_models.py   # Modelos para chat y conversaciones
│   │
│   ├── routes/              # Rutas de la API REST
│   │   ├── chatbot_routes.py      # Endpoints del chatbot
│   │   └── conversation_routes.py # Endpoints de conversaciones
│   │
│   ├── services/            # Lógica de negocio
│   │   ├── chatbot_service.py     # Servicio principal del chatbot
│   │   ├── database.py            # Conexión y operaciones de BD
│   │   └── telegram_bot.py        # Bot de Telegram integrado
│   │
│   └── utils/               # Utilidades y helpers
│       ├── helpers.py             # Funciones auxiliares
│       └── migrate_to_mongodb.py  # Script de migración de datos
│
├── tests/                   # Pruebas unitarias
├── docs/                    # Documentación adicional
├── chat_histories/          # Archivos locales de chat (respaldo)
└── venv/                    # Entorno virtual de Python
```

## 🚀 Inicio Rápido

### 1. Desde la raíz del proyecto (recomendado):

```bash
# Ejecutar todo el sistema con un solo comando
./start_backend.sh
```

Este script automatiza:
- ✅ Activación del entorno virtual
- ✅ Inicio del backend Flask (puerto 8000)
- ✅ Inicio del bot de Telegram (puerto 9000)
- ✅ Configuración automática de ngrok
- ✅ Configuración del webhook de Telegram
- ✅ Monitoreo de todos los procesos

### 2. Inicio manual (desarrollo):

```bash
# 1. Activar entorno virtual
cd back
source venv/bin/activate

# 2. Instalar dependencias (primera vez)
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# 4. Iniciar solo el backend
python app.py

# 5. En otra terminal, iniciar bot de Telegram (opcional)
python src/services/telegram_bot.py
```

## 🔧 Configuración

### Variables de Entorno Requeridas

Crea un archivo `.env` basado en `.env.example`:

```bash
# API Keys
COHERE_API_KEY=tu_api_key_de_cohere

# Telegram Bot (opcional)
TELEGRAM_TOKEN=tu_token_del_bot_telegram

# Base de datos MongoDB (opcional)
MONGODB_URI=mongodb://localhost:27017/impulsa_edutech
MONGODB_DB_NAME=impulsa_edutech

# Configuración del servidor
FLASK_ENV=development
HOST=0.0.0.0
PORT=8000
DEBUG=true
```

### Obtener API Keys

1. **Cohere AI**: Registrarse en [cohere.ai](https://cohere.ai) y obtener API key
2. **Telegram Bot**: Crear bot con [@BotFather](https://t.me/botfather) en Telegram
3. **MongoDB**: Usar MongoDB local o servicio como MongoDB Atlas

## 📡 API Endpoints

### Chatbot
- `POST /ask` - Enviar pregunta al chatbot
- `GET /health` - Estado del sistema

### Conversaciones
- `GET /conversations` - Listar todas las conversaciones
- `GET /conversations/{id}` - Obtener conversación específica
- `DELETE /conversations/{id}` - Eliminar conversación
- `GET /conversations/by-label/{label}` - Buscar por etiqueta

### Ejemplos de uso

```bash
# Preguntar al chatbot
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Qué carreras ofrece la universidad?", "conversation_id": "opcional"}'

# Ver estado del sistema
curl http://localhost:8000/health
```

## 🤖 Bot de Telegram

El bot de Telegram se integra automáticamente con el backend y permite:

- ✅ Conversaciones naturales con el chatbot
- ✅ Historial de conversaciones por usuario
- ✅ Respuestas contextuales
- ✅ Configuración automática de webhook con ngrok

## 🗄️ Base de Datos

### MongoDB (Recomendado)
- Almacenamiento robusto y escalable
- Búsquedas eficientes
- Respaldo automático

### Archivos JSON (Respaldo)
- Sistema de respaldo local en `chat_histories/`
- Se activa automáticamente si MongoDB no está disponible

## 🧪 Testing

```bash
# Ejecutar pruebas
cd back
python -m pytest tests/

# Ejecutar con coverage
python -m pytest tests/ --cov=src/
```

## 📦 Dependencias Principales

- **Flask**: Framework web minimalista
- **Cohere**: API de inteligencia artificial
- **PyMongo**: Cliente de MongoDB
- **Flask-CORS**: Manejo de CORS para frontend
- **python-telegram-bot**: SDK de Telegram
- **python-dotenv**: Manejo de variables de entorno

## 🔒 Seguridad

- ✅ Variables de entorno para credenciales
- ✅ Validación de entrada de usuarios
- ✅ Sanitización de datos
- ✅ CORS configurado correctamente

## 📈 Monitoreo

El sistema incluye:
- ✅ Logs detallados en consola
- ✅ Endpoint de salud `/health`
- ✅ Monitoreo automático de procesos
- ✅ Limpieza automática al detener servicios

## 🚫 Detener Servicios

Para detener todos los servicios iniciados con `start_backend.sh`:
- Presiona `Ctrl+C` en la terminal donde se ejecuta el script
- Todos los procesos se detendrán automáticamente

## 🆘 Solución de Problemas

### El backend no inicia
```bash
# Verificar puerto ocupado
lsof -i :8000

# Verificar dependencias
pip list | grep flask
```

### El bot de Telegram no funciona
```bash
# Verificar token
echo $TELEGRAM_TOKEN

# Verificar ngrok
curl http://localhost:4040/api/tunnels
```

### MongoDB no conecta
```bash
# Verificar servicio local
sudo systemctl status mongod

# O usar MongoDB Atlas (recomendado)
```

## 📞 Soporte

**Universidad Cooperativa de Colombia - Campus Popayán**

Para soporte técnico, consulta la documentación en el directorio `docs/` o contacta al equipo de desarrollo.

---

*Desarrollado con ❤️ para la comunidad educativa UCC Popayán*
