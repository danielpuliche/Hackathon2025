#!/usr/bin/env python3
"""
Script para automatizar la configuración del bot de Telegram
Obtiene la URL de ngrok automáticamente y configura el webhook
"""

import os
import requests
import json
import time
import subprocess
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

def get_ngrok_url():
    """Obtener la URL pública de ngrok"""
    try:
        response = requests.get("http://localhost:4040/api/tunnels")
        if response.status_code == 200:
            data = response.json()
            for tunnel in data.get('tunnels', []):
                if tunnel.get('proto') == 'https':
                    return tunnel.get('public_url')
        return None
    except requests.exceptions.ConnectionError:
        return None

def set_telegram_webhook(webhook_url):
    """Configurar el webhook de Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook"
    data = {"url": webhook_url}
    
    try:
        response = requests.post(url, data=data)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_webhook_info():
    """Obtener información del webhook actual"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getWebhookInfo"
    
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def delete_webhook():
    """Eliminar el webhook actual"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/deleteWebhook"
    
    try:
        response = requests.post(url)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def check_servers():
    """Verificar si los servidores están funcionando"""
    print("🔍 Verificando servidores...")
    
    # Verificar backend (puerto 8000)
    try:
        response = requests.get("http://localhost:8000", timeout=5)
        print("✅ Backend (puerto 8000): Funcionando")
        backend_ok = True
    except:
        print("❌ Backend (puerto 8000): No responde")
        backend_ok = False
    
    # Verificar bot (puerto 9000)
    try:
        response = requests.get("http://localhost:9000", timeout=5)
        print("✅ Bot (puerto 9000): Funcionando")
        bot_ok = True
    except:
        print("❌ Bot (puerto 9000): No responde")
        bot_ok = False
    
    return backend_ok, bot_ok

def test_bot():
    """Probar el bot enviando una solicitud al backend"""
    try:
        # Usar un ID de conversación especial para tests que será eliminado después
        test_conversation_id = "test_setup_temp_" + str(int(time.time()))
        
        payload = {
            "question": "Test de conexión",
            "conversation_id": test_conversation_id
        }
        response = requests.post(
            "http://localhost:8000/ask",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Test del backend exitoso")
            print(f"   Respuesta: {data.get('answer', '')[:50]}...")
            
            # Eliminar la conversación de test de la base de datos
            cleanup_test_conversation(test_conversation_id)
            return True
        else:
            print(f"❌ Test del backend falló - Código: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Test del backend falló - Error: {e}")
        return False

def cleanup_test_conversation(conversation_id):
    """Eliminar conversación de test de la base de datos"""
    try:
        # Intentar eliminar via API
        response = requests.delete(f"http://localhost:8000/conversations/{conversation_id}", timeout=5)
        if response.status_code == 200:
            print("🧹 Conversación de test eliminada de la DB")
        else:
            print("ℹ️  Conversación de test guardada en archivo local (MongoDB no disponible)")
    except Exception as e:
        print("ℹ️  No se pudo eliminar conversación de test (sin problema)")

def cleanup_all_test_conversations():
    """Limpiar todas las conversaciones de test existentes"""
    try:
        # Obtener todas las conversaciones
        response = requests.get("http://localhost:8000/conversations", timeout=5)
        if response.status_code == 200:
            data = response.json()
            conversations = data.get('conversations', [])
            
            # Buscar conversaciones de test
            test_conversations = [
                conv for conv in conversations 
                if conv.get('id_chat', '').startswith('test_setup') or 
                   conv.get('id_chat', '').startswith('test_')
            ]
            
            if test_conversations:
                print(f"🧹 Encontradas {len(test_conversations)} conversaciones de test para limpiar...")
                
                for conv in test_conversations:
                    conv_id = conv.get('id_chat')
                    delete_response = requests.delete(f"http://localhost:8000/conversations/{conv_id}", timeout=5)
                    if delete_response.status_code == 200:
                        print(f"   ✅ Eliminada: {conv_id[:20]}...")
                    else:
                        print(f"   ⚠️  No se pudo eliminar: {conv_id[:20]}...")
                
                print("✅ Limpieza de conversaciones de test completada")
            else:
                print("✅ No hay conversaciones de test para limpiar")
                
    except Exception as e:
        print("ℹ️  No se pudo acceder a la lista de conversaciones para limpieza")

def main():
    print("🤖 Configurador automático del bot de Telegram")
    print("=" * 50)
    
    if not TELEGRAM_TOKEN:
        print("❌ Error: TELEGRAM_TOKEN no encontrado en .env")
        return
    
    # Limpiar conversaciones de test anteriores
    print("🧹 Limpiando conversaciones de test anteriores...")
    cleanup_all_test_conversations()
    
    # Verificar servidores
    backend_ok, bot_ok = check_servers()
    
    if not backend_ok:
        print("\n⚠️  El backend no está funcionando.")
        print("   Ejecuta: python app.py")
        return
    
    if not bot_ok:
        print("\n⚠️  El bot no está funcionando.")
        print("   Ejecuta: python telegram_bot.py")
        return
    
    # Verificar ngrok
    print("\n🔗 Obteniendo URL de ngrok...")
    ngrok_url = get_ngrok_url()
    
    if not ngrok_url:
        print("❌ No se pudo obtener la URL de ngrok")
        print("   Asegúrate de que ngrok esté funcionando en puerto 9000:")
        print("   ngrok http 9000")
        return
    
    print(f"✅ URL de ngrok encontrada: {ngrok_url}")
    
    # Configurar webhook
    webhook_url = f"{ngrok_url}/webhook/{TELEGRAM_TOKEN}"
    print(f"\n⚙️  Configurando webhook...")
    print(f"   URL: {webhook_url}")
    
    result = set_telegram_webhook(webhook_url)
    
    if result.get("ok"):
        print("✅ Webhook configurado exitosamente")
    else:
        print(f"❌ Error configurando webhook: {result}")
        return
    
    # Verificar webhook
    print("\n🔍 Verificando webhook...")
    webhook_info = get_webhook_info()
    
    if webhook_info.get("ok"):
        info = webhook_info.get("result", {})
        print(f"✅ Webhook activo: {info.get('url', 'N/A')}")
        print(f"   Actualizaciones pendientes: {info.get('pending_update_count', 0)}")
    else:
        print(f"❌ Error verificando webhook: {webhook_info}")
    
    # Test del backend
    print("\n🧪 Probando backend...")
    if test_bot():
        print("\n🎉 ¡Todo configurado correctamente!")
        print("\n📱 Ahora puedes enviar mensajes a tu bot de Telegram")
        print("   El bot debería responder automáticamente")
    else:
        print("\n⚠️  Hay un problema con el backend")
    
    print("\n" + "=" * 50)
    print("📊 Resumen:")
    print(f"   Backend: http://localhost:8000")
    print(f"   Bot: http://localhost:9000")
    print(f"   Ngrok: {ngrok_url}")
    print(f"   Webhook: {webhook_url}")

if __name__ == "__main__":
    main()
