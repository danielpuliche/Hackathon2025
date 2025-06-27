#!/bin/bash

# Script para iniciar el bot de Telegram automáticamente
# Uso: ./start_bot.sh

echo "🚀 Iniciando bot de Telegram..."
echo "================================"

# Verificar que estamos en el directorio correcto
if [ ! -f "app.py" ] || [ ! -f "telegram_bot.py" ]; then
    echo "❌ Error: Ejecuta este script desde el directorio /back"
    exit 1
fi

# Activar entorno virtual
echo "📦 Activando entorno virtual..."
source venv/bin/activate

# Función para limpiar procesos al salir
cleanup() {
    echo ""
    echo "🛑 Deteniendo servicios..."
    kill $BACKEND_PID $BOT_PID 2>/dev/null
    wait $BACKEND_PID $BOT_PID 2>/dev/null
    echo "✅ Servicios detenidos"
    exit 0
}

# Configurar trap para cleanup
trap cleanup SIGINT SIGTERM

# Iniciar backend
echo "🔧 Iniciando backend (puerto 8000)..."
python app.py &
BACKEND_PID=$!
sleep 3

# Iniciar bot de Telegram
echo "🤖 Iniciando bot de Telegram (puerto 9000)..."
python telegram_bot.py &
BOT_PID=$!
sleep 3

# Verificar que ngrok esté corriendo
echo "🔗 Verificando ngrok..."
if ! curl -s http://localhost:4040/api/tunnels > /dev/null; then
    echo "⚠️  Ngrok no está corriendo. Iniciándolo..."
    echo "   Ejecuta en otra terminal: ngrok http 9000"
    echo "   Presiona Enter cuando ngrok esté funcionando..."
    read
fi

# Configurar webhook automáticamente
echo "⚙️  Configurando webhook automáticamente..."
python setup_bot.py

echo ""
echo "🎉 ¡Bot configurado y funcionando!"
echo "📱 Puedes enviar mensajes a tu bot de Telegram"
echo ""
echo "Para detener: Presiona Ctrl+C"
echo ""

# Mantener el script corriendo
wait $BACKEND_PID $BOT_PID
