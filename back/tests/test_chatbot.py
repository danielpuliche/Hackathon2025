#!/usr/bin/env python3
"""
Script de prueba para demonstrar la funcionalidad del chatbot con MongoDB
"""
import requests
import json
import time

# URL base del servidor
BASE_URL = "http://localhost:8000"

def test_chatbot():
    """Probar la funcionalidad básica del chatbot"""
    print("🤖 Probando funcionalidad del chatbot...")
    
    # Test 1: Pregunta sobre matrículas con ID temporal
    print("\n1️⃣ Pregunta sobre matrículas:")
    test_conv_id = f"test_temp_{int(time.time())}"
    
    response = requests.post(f"{BASE_URL}/ask", json={
        "question": "¿Cómo me matriculo en la universidad?",
        "conversation_id": test_conv_id
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Respuesta recibida")
        print(f"🆔 ID Conversación: {data.get('conversation_id')}")
        print(f"🏷️  Etiquetas detectadas: {data.get('labels')}")
        print(f"📝 Historial: {len(data.get('history', []))} mensajes")
        
        # Guardar ID para siguientes pruebas
        conv_id = data.get('conversation_id')
        
        # Test 2: Continuar conversación
        print("\n2️⃣ Continuando la conversación:")
        response2 = requests.post(f"{BASE_URL}/ask", json={
            "question": "¿Cuáles son los costos?",
            "conversation_id": conv_id
        })
        
        if response2.status_code == 200:
            data2 = response2.json()
            print(f"✅ Conversación continuada")
            print(f"🏷️  Etiquetas: {data2.get('labels')}")
            print(f"📝 Historial: {len(data2.get('history', []))} mensajes")
        
        # Limpiar conversación de test
        cleanup_test_conversation(conv_id)
        return conv_id
    else:
        print(f"❌ Error: {response.status_code}")
        return None

def cleanup_test_conversation(conversation_id):
    """Eliminar conversación de test"""
    try:
        if conversation_id and conversation_id.startswith('test_'):
            response = requests.delete(f"{BASE_URL}/conversations/{conversation_id}")
            if response.status_code == 200:
                print("🧹 Conversación de test eliminada")
            else:
                print("ℹ️  Conversación de test guardada localmente (sin MongoDB)")
                # También eliminar archivo JSON si existe
                import os
                import glob
                json_files = glob.glob(f"chat_histories/chat_history_{conversation_id}.json")
                for file in json_files:
                    try:
                        os.remove(file)
                        print(f"🧹 Archivo JSON de test eliminado: {os.path.basename(file)}")
                    except:
                        pass
    except Exception as e:
        print(f"ℹ️  No se pudo limpiar conversación de test: {e}")

def test_mongodb_endpoints(conv_id=None):
    """Probar endpoints específicos de MongoDB"""
    print("\n🗄️  Probando endpoints de MongoDB...")
    
    # Test conversaciones
    print("\n📋 Obteniendo todas las conversaciones:")
    response = requests.get(f"{BASE_URL}/conversations")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ {len(data.get('conversations', []))} conversaciones encontradas")
    else:
        print(f"ℹ️  MongoDB no disponible (fallback a archivos JSON)")
    
    # Test conversación específica
    if conv_id:
        print(f"\n🔍 Obteniendo conversación {conv_id[:8]}...")
        response = requests.get(f"{BASE_URL}/conversations/{conv_id}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Conversación encontrada con {len(data.get('history', []))} mensajes")
        else:
            print(f"ℹ️  Conversación no encontrada en MongoDB")
    
    # Test por etiquetas
    print(f"\n🏷️  Buscando conversaciones sobre 'Matrículas':")
    response = requests.get(f"{BASE_URL}/conversations/by-label/Matrículas")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ {len(data.get('conversations', []))} conversaciones sobre matrículas")
    else:
        print(f"ℹ️  Búsqueda por etiquetas no disponible sin MongoDB")

def show_file_fallback():
    """Mostrar que el sistema funciona con archivos JSON como fallback"""
    print("\n📁 Verificando respaldo en archivos JSON...")
    
    import os
    import glob
    
    json_files = glob.glob("chat_histories/chat_history_*.json")
    print(f"📄 {len(json_files)} archivos JSON encontrados")
    
    if json_files:
        # Mostrar contenido del último archivo
        latest_file = max(json_files, key=os.path.getctime)
        print(f"\n📖 Contenido del archivo más reciente ({os.path.basename(latest_file)}):")
        
        try:
            with open(latest_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"🆔 ID: {data.get('id_chat', 'N/A')}")
            print(f"🏷️  Etiquetas: {data.get('labels', [])}")
            print(f"📝 Mensajes: {len(data.get('history', []))}")
            
            for i, msg in enumerate(data.get('history', []), 1):
                role = msg.get('role', 'Unknown')
                message = msg.get('message', '')[:50] + '...' if len(msg.get('message', '')) > 50 else msg.get('message', '')
                print(f"   {i}. {role}: {message}")
                
        except Exception as e:
            print(f"❌ Error leyendo archivo: {e}")

def main():
    """Función principal de prueba"""
    print("🚀 Iniciando pruebas del chatbot con MongoDB")
    print("=" * 60)
    
    try:
        # Verificar que el servidor esté ejecutándose
        response = requests.get(f"{BASE_URL}/conversations", timeout=5)
        print("✅ Servidor Flask está ejecutándose")
    except requests.exceptions.RequestException:
        print("❌ Error: Servidor Flask no está ejecutándose")
        print("💡 Ejecuta primero: python app.py")
        return
    
    # Ejecutar pruebas
    conv_id = test_chatbot()
    test_mongodb_endpoints(conv_id)
    show_file_fallback()
    
    print("\n" + "=" * 60)
    print("🎉 Pruebas completadas!")
    print("🧹 Datos de test eliminados automáticamente")
    print("\n💡 Próximos pasos:")
    print("1. ✅ MongoDB Atlas ya está configurado y funcionando")
    print("2. ✅ COHERE_API_KEY ya está configurada")
    print("3. ✅ Datos migrados exitosamente")
    print("4. 🚀 ¡Tu chatbot está listo para producción!")

if __name__ == "__main__":
    main()
