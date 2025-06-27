#!/bin/bash

# Script para configurar MongoDB en Ubuntu/Debian
# Este script es opcional - también puedes usar MongoDB Atlas (cloud)

echo "🚀 Configurando MongoDB para el chatbot..."

# Verificar si ya está instalado
if command -v mongod &> /dev/null; then
    echo "✅ MongoDB ya está instalado"
    sudo systemctl status mongod
    exit 0
fi

echo "📦 Instalando MongoDB Community Edition..."

# Actualizar paquetes
sudo apt update

# Instalar gnupg y curl si no están instalados
sudo apt install -y gnupg curl

# Importar la clave pública de MongoDB
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
   --dearmor

# Crear archivo de lista para MongoDB
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Actualizar base de datos de paquetes
sudo apt update

# Instalar MongoDB
sudo apt install -y mongodb-org

# Habilitar e iniciar MongoDB
sudo systemctl enable mongod
sudo systemctl start mongod

# Verificar estado
echo "🔍 Verificando instalación..."
sudo systemctl status mongod

echo ""
echo "✅ MongoDB instalado exitosamente!"
echo ""
echo "📝 Comandos útiles:"
echo "   Iniciar MongoDB:    sudo systemctl start mongod"
echo "   Detener MongoDB:    sudo systemctl stop mongod"
echo "   Reiniciar MongoDB:  sudo systemctl restart mongod"
echo "   Estado de MongoDB:  sudo systemctl status mongod"
echo "   Cliente MongoDB:    mongosh"
echo ""
echo "🌐 Para usar MongoDB Atlas (cloud) en su lugar:"
echo "   1. Crea una cuenta en https://www.mongodb.com/atlas"
echo "   2. Crea un cluster gratuito"
echo "   3. Obtén la cadena de conexión"
echo "   4. Actualiza MONGODB_URI en tu archivo .env"
