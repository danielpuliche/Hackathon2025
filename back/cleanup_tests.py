#!/usr/bin/env python3
"""
Script para limpiar conversaciones de test de la base de datos
"""
import requests
import json
import os
import glob

BASE_URL = "http://localhost:8000"

def clean_mongodb_tests():
    """Limpiar conversaciones de test de MongoDB"""
    print("🧹 Limpiando conversaciones de test de MongoDB...")
    
    try:
        response = requests.delete(f"{BASE_URL}/conversations/cleanup-tests")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data.get('message')}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error conectando al servidor: {e}")

def clean_json_files():
    """Limpiar archivos JSON de test"""
    print("🧹 Limpiando archivos JSON de test...")
    
    test_patterns = [
        "chat_histories/chat_history_test_*.json",
        "chat_histories/chat_history_*test*.json"
    ]
    
    deleted_count = 0
    for pattern in test_patterns:
        files = glob.glob(pattern)
        for file in files:
            try:
                os.remove(file)
                print(f"   ✅ Eliminado: {os.path.basename(file)}")
                deleted_count += 1
            except Exception as e:
                print(f"   ❌ Error eliminando {file}: {e}")
    
    if deleted_count == 0:
        print("   ✅ No hay archivos de test para eliminar")
    else:
        print(f"   ✅ Eliminados {deleted_count} archivos de test")

def show_remaining_conversations():
    """Mostrar conversaciones restantes"""
    print("📊 Conversaciones restantes en la base de datos:")
    
    try:
        response = requests.get(f"{BASE_URL}/conversations")
        if response.status_code == 200:
            data = response.json()
            conversations = data.get('conversations', [])
            
            print(f"   Total: {len(conversations)} conversaciones")
            
            for i, conv in enumerate(conversations, 1):
                conv_id = conv.get('id_chat', 'N/A')
                history_count = len(conv.get('history', []))
                labels = conv.get('labels', [])
                created = conv.get('created_at', 'N/A')
                
                print(f"   {i}. ID: {conv_id[:30]}...")
                print(f"      Mensajes: {history_count}")
                print(f"      Etiquetas: {labels}")
                print(f"      Creado: {created}")
                print()
                
        else:
            print(f"   ❌ Error obteniendo conversaciones: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

def main():
    print("🚀 Limpieza de conversaciones de test")
    print("=" * 50)
    
    # Verificar que el servidor esté ejecutándose
    try:
        response = requests.get(f"{BASE_URL}/conversations", timeout=5)
        print("✅ Servidor conectado")
    except:
        print("❌ Servidor no disponible")
        print("💡 Ejecuta primero: python app.py")
        return
    
    # Ejecutar limpieza
    clean_mongodb_tests()
    clean_json_files()
    
    print("\n" + "=" * 50)
    show_remaining_conversations()
    
    print("=" * 50)
    print("🎉 Limpieza completada!")
    print("💡 Solo quedan conversaciones reales de usuarios")

if __name__ == "__main__":
    main()
