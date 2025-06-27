#!/bin/bash

# 🚀 Script maestro para Impulsa EDU-Tech Backend
# Universidad Cooperativa de Colombia - Campus Popayán
# Inicia: Backend Flask + Bot Telegram + Ngrok

set -e

echo "🚀 Iniciando Impulsa EDU-Tech - Sistema Completo"
echo "================================================"
echo "🏫 Campus: Popayán"
echo "⚙️  Servicios: Backend + Telegram Bot + Ngrok"
echo ""

# Verificar que estamos en el directorio correcto (raíz del proyecto)
if [ ! -d "back" ] || [ ! -f "back/app.py" ]; then
    echo "❌ Error: Ejecuta este script desde la raíz del proyecto Hackathon"
    echo "📁 Directorio actual: $(pwd)"
    echo "💡 Estructura esperada: ./back/app.py debe existir"
    exit 1
fi

# Cambiar al directorio backend
cd back

# Verificar que existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "❌ Error: No se encontró el entorno virtual 'venv' en ./back/"
    echo "💡 Ejecuta: cd back && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activar entorno virtual
echo "📦 Activando entorno virtual..."
source venv/bin/activate

# Verificar variables de entorno
echo "� Verificando configuración..."
if [ -z "$COHERE_API_KEY" ] && [ ! -f ".env" ]; then
    echo "⚠️  Advertencia: No se encontró COHERE_API_KEY ni archivo .env"
fi

if [ -z "$TELEGRAM_TOKEN" ] && [ ! -f ".env" ]; then
    echo "⚠️  Advertencia: No se encontró TELEGRAM_TOKEN. El bot de Telegram no funcionará."
fi

# Variables para control de procesos
BACKEND_PID=""
TELEGRAM_PID=""
NGROK_PID=""

# Función de limpieza al salir
cleanup() {
    echo ""
    echo "🛑 Deteniendo servicios..."
    
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
        echo "   ✅ Backend Flask detenido"
    fi
    
    if [ ! -z "$TELEGRAM_PID" ]; then
        kill $TELEGRAM_PID 2>/dev/null || true
        echo "   ✅ Bot Telegram detenido"
    fi
    
    if [ ! -z "$NGROK_PID" ]; then
        kill $NGROK_PID 2>/dev/null || true
        echo "   ✅ Ngrok detenido"
    fi
    
    echo "🏁 Todos los servicios han sido detenidos"
    exit 0
}

# Configurar trap para cleanup
trap cleanup SIGINT SIGTERM

# Verificar e instalar ngrok si no existe
check_ngrok() {
    if ! command -v ngrok &> /dev/null; then
        echo "🔧 Ngrok no encontrado. Intentando instalar..."
        
        if command -v snap &> /dev/null; then
            echo "   � Instalando via snap..."
            sudo snap install ngrok 2>/dev/null || {
                echo "   ❌ Error instalando ngrok via snap"
                echo "   💡 Instala manualmente desde: https://ngrok.com/download"
                return 1
            }
        else
            echo "   ❌ No se pudo instalar ngrok automáticamente"
            echo "   💡 Instala manualmente desde: https://ngrok.com/download"
            return 1
        fi
    fi
    return 0
}

# Iniciar ngrok
start_ngrok() {
    echo "🔗 Iniciando ngrok para exponer bot de Telegram..."
    
    if ! check_ngrok; then
        echo "⚠️  Continuando sin ngrok. El bot de Telegram no funcionará."
        return 1
    fi
    
    # Verificar si ngrok ya está corriendo
    if curl -s http://localhost:4040/api/tunnels &> /dev/null; then
        echo "   ✅ Ngrok ya está corriendo"
        return 0
    fi
    
    # Iniciar ngrok en background
    ngrok http 9000 --log=stdout > /tmp/ngrok.log 2>&1 &
    NGROK_PID=$!
    
    # Esperar a que ngrok esté listo
    echo "   ⏳ Esperando que ngrok esté listo..."
    for i in {1..10}; do
        if curl -s http://localhost:4040/api/tunnels &> /dev/null; then
            echo "   ✅ Ngrok está corriendo"
            return 0
        fi
        sleep 1
    done
    
    echo "   ⚠️  Ngrok tardó en iniciar, continuando..."
    return 0
}

# Obtener URL de ngrok
get_ngrok_url() {
    if curl -s http://localhost:4040/api/tunnels &> /dev/null; then
        curl -s http://localhost:4040/api/tunnels | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    tunnels = data.get('tunnels', [])
    for tunnel in tunnels:
        if tunnel.get('proto') == 'https':
            print(tunnel['public_url'])
            break
except:
    pass
" 2>/dev/null
    fi
}

# 1. Iniciar Backend Flask
echo "🔧 Iniciando Backend Flask (puerto 8000)..."
python app.py &
BACKEND_PID=$!

# Esperar a que el backend esté listo con reintentos
echo "   ⏳ Esperando que el backend esté listo..."
for i in {1..15}; do
    if curl -s http://localhost:8000/health &> /dev/null; then
        echo "   ✅ Backend Flask funcionando"
        break
    fi
    if [ $i -eq 15 ]; then
        echo "❌ Error: El backend no responde en puerto 8000 después de 15 segundos"
        echo "   💡 Revisa los logs del backend para más detalles"
        cleanup
        exit 1
    fi
    sleep 1
done

# 2. Iniciar ngrok (solo si hay token de Telegram)
if [ ! -z "$TELEGRAM_TOKEN" ] || grep -q "TELEGRAM_TOKEN" .env 2>/dev/null; then
    start_ngrok
    sleep 2
    
    # 3. Iniciar Bot de Telegram
    echo "🤖 Iniciando Bot de Telegram (puerto 9000)..."
    python src/services/telegram_bot.py &
    TELEGRAM_PID=$!
    sleep 3
    
    # Verificar que el bot esté corriendo
    if curl -s http://localhost:9000/health &> /dev/null; then
        echo "   ✅ Bot de Telegram funcionando"
        
        # 4. Configurar webhook automáticamente
        NGROK_URL=$(get_ngrok_url)
        if [ ! -z "$NGROK_URL" ]; then
            echo "🔗 Configurando webhook automáticamente..."
            echo "   📡 URL pública: $NGROK_URL"
            
            # Intentar configurar webhook
            python -c "
import os, sys
sys.path.insert(0, 'src')
from services.telegram_bot import TelegramBotService
from config.settings import config

try:
    app_config = config['default']()
    bot = TelegramBotService(app_config)
    success = bot.set_webhook('$NGROK_URL')
    print('   ✅ Webhook configurado exitosamente' if success else '   ⚠️  Error configurando webhook')
except Exception as e:
    print(f'   ⚠️  Error: {e}')
"
        else
            echo "   ⚠️  No se pudo obtener URL de ngrok"
        fi
    else
        echo "   ⚠️  Bot de Telegram no responde en puerto 9000"
    fi
else
    echo "⚠️  TELEGRAM_TOKEN no configurado. Saltando bot de Telegram."
fi

# Mostrar estado final
echo ""
echo "🎉 ¡Sistema Impulsa EDU-Tech iniciado!"
echo "=================================="
echo "🌐 Backend Flask: http://localhost:8000"
echo "📊 Dashboard: http://localhost:8000/health"

if [ ! -z "$TELEGRAM_PID" ]; then
    echo "🤖 Bot Telegram: http://localhost:9000"
    NGROK_URL=$(get_ngrok_url)
    if [ ! -z "$NGROK_URL" ]; then
        echo "📡 URL Pública: $NGROK_URL"
    fi
fi

echo ""
echo "💡 Para detener todos los servicios: Presiona Ctrl+C"
echo ""

# Mantener el script corriendo y monitorear procesos
while true; do
    # Verificar si los procesos siguen corriendo
    if [ ! -z "$BACKEND_PID" ] && ! kill -0 $BACKEND_PID 2>/dev/null; then
        echo "❌ El backend se detuvo inesperadamente"
        cleanup
        exit 1
    fi
    
    if [ ! -z "$TELEGRAM_PID" ] && ! kill -0 $TELEGRAM_PID 2>/dev/null; then
        echo "❌ El bot de Telegram se detuvo inesperadamente"
        # No salir, el backend puede seguir funcionando
    fi
    
    sleep 5
done
