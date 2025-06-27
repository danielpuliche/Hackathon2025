# Backend Chatbot UCC - Con MongoDB

Backend del chatbot de la Universidad Cooperativa de Colombia usando Flask y MongoDB para almacenar el historial de conversaciones.

## 🚀 Características

- **API REST** con Flask
- **Almacenamiento en MongoDB** para historiales de chat
- **Clasificación automática** de conversaciones por etiquetas
- **Respaldo en archivos JSON** como fallback
- **Integración con Cohere** para respuestas de IA
- **CORS habilitado** para peticiones desde frontend

## 📁 Estructura del Proyecto

```
back/
├── app.py                 # Aplicación principal Flask
├── database.py           # Módulo de conexión a MongoDB
├── migrate_to_mongodb.py # Script para migrar datos existentes
├── setup_mongodb.sh      # Script de instalación de MongoDB
├── requirements.txt      # Dependencias Python
├── .env.example         # Ejemplo de configuración
└── chat_histories/      # Respaldo local (JSON)
```

## ⚙️ Configuración

### 1. Instalar Dependencias

```bash
# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# venv\Scripts\activate   # En Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno

Copia el archivo `.env.example` a `.env` y configura las variables:

```bash
cp .env.example .env
```

Edita el archivo `.env`:

```env
# Configuración de Cohere
COHERE_API_KEY=tu_clave_de_cohere_aqui

# Configuración de Flask
FLASK_SECRET_KEY=supersecretkey

# Configuración de MongoDB
# Opción 1: MongoDB local
MONGODB_URI=mongodb://localhost:27017/

# Opción 2: MongoDB Atlas (cloud)
# MONGODB_URI=mongodb+srv://usuario:password@cluster.mongodb.net/

# Nombre de la base de datos
DATABASE_NAME=chatbot_ucc
```

### 3. Configurar MongoDB

#### Opción A: MongoDB Local

Ejecuta el script de instalación (Ubuntu/Debian):

```bash
./setup_mongodb.sh
```

O instala manualmente siguiendo la [documentación oficial](https://docs.mongodb.com/manual/installation/).

#### Opción B: MongoDB Atlas (Cloud)

1. Crea una cuenta en [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Crea un cluster gratuito
3. Obtén la cadena de conexión
4. Actualiza `MONGODB_URI` en tu archivo `.env`

## 🔄 Migración de Datos Existentes

Si ya tienes historiales en archivos JSON, puedes migrarlos a MongoDB:

```bash
python migrate_to_mongodb.py
```

Este script:
- ✅ Crea un respaldo de tus archivos JSON
- ✅ Migra todos los historiales a MongoDB
- ✅ Verifica que la migración fue exitosa

## 🚀 Ejecutar el Servidor

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar servidor
python app.py
```

El servidor estará disponible en `http://localhost:8000`

## 📚 API Endpoints

### Chat

- **POST** `/ask` - Enviar pregunta al chatbot
- **GET** `/conversations` - Obtener todas las conversaciones
- **GET** `/conversations/<id>` - Obtener conversación específica
- **DELETE** `/conversations/<id>` - Eliminar conversación
- **GET** `/conversations/by-label/<label>` - Filtrar por etiqueta

### Ejemplo de uso:

```bash
# Enviar pregunta
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Cómo me matriculo?", "conversation_id": "opcional"}'

# Obtener conversaciones
curl http://localhost:8000/conversations

# Obtener conversaciones sobre matrículas
curl http://localhost:8000/conversations/by-label/Matrículas
```

## 🏷️ Etiquetas Automáticas

El sistema clasifica automáticamente las conversaciones con estas etiquetas:

- **Matrículas** - Inscripciones, matricular
- **Admisiones** - Proceso de admisión
- **Biblioteca** - Préstamos, libros
- **Pagos** - Cuotas, facturas
- **Programas** - Carreras, ingeniería
- **Becas** - Descuentos, financiamiento
- **Calendario** - Fechas, cronogramas
- **Soporte** - Ayuda, problemas

## 🧹 Limpieza de Datos de Test

Los scripts de prueba ahora eliminan automáticamente los datos de test para mantener la base de datos limpia:

### Scripts con Auto-limpieza
- ✅ `test_chatbot.py` - Elimina conversaciones de test automáticamente
- ✅ `setup_bot.py` - Limpia tests del bot de Telegram
- ✅ API endpoint `/conversations/cleanup-tests` - Limpieza manual

### Limpieza Manual
```bash
# Limpiar todas las conversaciones de test
python cleanup_tests.py

# O usar el endpoint API
curl -X DELETE http://localhost:8000/conversations/cleanup-tests
```

### Identificación de Tests
Las conversaciones de test se identifican por:
- ID que empieza con `test_`
- ID que contiene `temp_`
- Creadas por scripts de prueba

## 🔧 Troubleshooting

### Error de conexión a MongoDB

```
ERROR: No hay conexión a MongoDB
```

**Soluciones:**

1. **MongoDB local**: Verifica que esté ejecutándose
   ```bash
   sudo systemctl status mongod
   sudo systemctl start mongod
   ```

2. **MongoDB Atlas**: Verifica la cadena de conexión y credenciales

3. **Red**: Asegúrate de que no haya firewalls bloqueando

### Error de dependencias

```
ModuleNotFoundError: No module named 'pymongo'
```

**Solución:**
```bash
pip install -r requirements.txt
```

### Fallback a archivos JSON

Si MongoDB no está disponible, el sistema automáticamente usará archivos JSON como respaldo.

## 🌟 Características Avanzadas

### Respaldo Automático

- MongoDB como almacenamiento principal
- Archivos JSON como respaldo automático
- Sin pérdida de datos si MongoDB falla

### Escalabilidad

- Base de datos MongoDB optimizada para grandes volúmenes
- Índices automáticos para búsquedas rápidas
- Soporte para clustering y replicación

### Monitoreo

- Logs detallados de todas las operaciones
- Métricas de uso y rendimiento
- Alertas automáticas de errores

## 📞 Soporte

Para problemas o dudas:

1. Revisa los logs en la consola
2. Verifica la configuración en `.env`
3. Consulta la documentación de [MongoDB](https://docs.mongodb.com/)
4. Consulta la documentación de [Cohere](https://docs.cohere.ai/)

---

**¡Chatbot UCC listo para funcionar con MongoDB! 🎉**
