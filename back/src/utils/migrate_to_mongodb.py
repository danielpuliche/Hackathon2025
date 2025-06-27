#!/usr/bin/env python3
"""
Script para migrar historiales de chat desde archivos JSON a MongoDB
"""
import os
import json
import glob
from database import ChatHistoryDB
from datetime import datetime

def migrate_json_to_mongodb():
    """Migrar todos los archivos JSON de chat_histories a MongoDB"""
    
    # Inicializar conexión a MongoDB
    chat_db = ChatHistoryDB()
    
    if not chat_db.is_connected():
        print("❌ Error: No se pudo conectar a MongoDB")
        print("Verifica que MongoDB esté ejecutándose y que las credenciales sean correctas")
        return False
    
    # Buscar todos los archivos JSON en el directorio chat_histories
    json_files = glob.glob("chat_histories/chat_history_*.json")
    
    if not json_files:
        print("📁 No se encontraron archivos JSON para migrar")
        return True
    
    print(f"🔍 Encontrados {len(json_files)} archivos para migrar")
    
    migrated_count = 0
    error_count = 0
    
    for json_file in json_files:
        try:
            print(f"📝 Procesando: {json_file}")
            
            # Leer el archivo JSON
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extraer datos
            conversation_id = data.get('id_chat')
            history = data.get('history', [])
            labels = data.get('labels', [])
            
            if not conversation_id:
                print(f"⚠️  Archivo {json_file} no tiene id_chat válido, saltando...")
                continue
            
            # Verificar si ya existe en MongoDB
            existing = chat_db.load_chat_history(conversation_id)
            if existing:
                print(f"ℹ️  Conversación {conversation_id} ya existe en MongoDB")
                # Opcionalmente, podrías actualizar aquí si quieres sobrescribir
                continue
            
            # Guardar en MongoDB
            success = chat_db.save_chat_history(conversation_id, history, labels)
            
            if success:
                print(f"✅ Migrado exitosamente: {conversation_id}")
                migrated_count += 1
            else:
                print(f"❌ Error migrando: {conversation_id}")
                error_count += 1
                
        except Exception as e:
            print(f"❌ Error procesando {json_file}: {e}")
            error_count += 1
    
    print(f"\n📊 Resumen de migración:")
    print(f"✅ Exitosos: {migrated_count}")
    print(f"❌ Errores: {error_count}")
    print(f"📁 Total archivos: {len(json_files)}")
    
    # Cerrar conexión
    chat_db.close_connection()
    
    return error_count == 0

def backup_json_files():
    """Crear respaldo de archivos JSON antes de migrar"""
    import shutil
    
    if os.path.exists("chat_histories"):
        backup_dir = f"chat_histories_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copytree("chat_histories", backup_dir)
        print(f"📦 Respaldo creado en: {backup_dir}")
        return backup_dir
    return None

def verify_migration():
    """Verificar que la migración fue exitosa"""
    chat_db = ChatHistoryDB()
    
    if not chat_db.is_connected():
        print("❌ No se pudo conectar a MongoDB para verificación")
        return False
    
    # Contar conversaciones en MongoDB
    conversations = chat_db.get_all_conversations(limit=1000)
    mongo_count = len(conversations)
    
    # Contar archivos JSON
    json_files = glob.glob("chat_histories/chat_history_*.json")
    json_count = len(json_files)
    
    print(f"\n🔍 Verificación:")
    print(f"📁 Archivos JSON: {json_count}")
    print(f"🗄️  Conversaciones en MongoDB: {mongo_count}")
    
    chat_db.close_connection()
    
    if mongo_count >= json_count:
        print("✅ La migración parece exitosa")
        return True
    else:
        print("⚠️  Posible problema en la migración")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando migración de archivos JSON a MongoDB")
    print("=" * 50)
    
    # Crear respaldo
    backup_dir = backup_json_files()
    
    # Ejecutar migración
    success = migrate_json_to_mongodb()
    
    if success:
        # Verificar migración
        verify_migration()
        print("\n🎉 Migración completada exitosamente!")
        
        if backup_dir:
            print(f"💡 Los archivos originales están respaldados en: {backup_dir}")
            print("💡 Puedes eliminar la carpeta 'chat_histories' si todo funciona correctamente")
    else:
        print("\n❌ La migración tuvo errores. Revisa los logs anteriores.")
