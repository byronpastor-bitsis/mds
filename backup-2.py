#!/usr/bin/env python
import sys
import datetime
import os
import shutil
import argparse
import subprocess

# Configuración personalizada
DEFAULT_DB_NAME = 'nombre_bd'
POSTGRES_PASSWORD = 'tu_contraseña_postgres'  # Contraseña de PostgreSQL
POSTGRES_USER = 'odoo'  # Usuario de PostgreSQL (normalmente 'odoo' o 'postgres')
POSTGRES_HOST = 'localhost'
POSTGRES_PORT = '5432'
BACKUP_DIR = r'C:\odoo_backups'  # Usar ruta absoluta estilo Windows
FILESTORE_SOURCE = r'C:\Users\{usuario}\AppData\Local\Odoo\filestore\{db}'

def crear_backup_windows(db_name=None):
    try:
        # Usar el nombre de BD proporcionado o el predeterminado
        db_name = db_name or DEFAULT_DB_NAME
        
        # Crear directorio de backups si no existe
        os.makedirs(BACKUP_DIR, exist_ok=True)
        
        # Generar nombre de archivo con timestamp
        fecha = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(BACKUP_DIR, f'backup_{db_name}_{fecha}.sql')
        
        # Crear backup usando pg_dump
        pg_env = os.environ.copy()
        pg_env['PGPASSWORD'] = POSTGRES_PASSWORD
        
        pg_dump_cmd = [
            'pg_dump',
            '-h', POSTGRES_HOST,
            '-p', POSTGRES_PORT,
            '-U', POSTGRES_USER,
            '-F', 'c',  # Custom format (compressed)
            '-f', backup_file,
            db_name
        ]
        
        result = subprocess.run(pg_dump_cmd, env=pg_env, 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
        
        if result.returncode != 0:
            raise Exception(f"pg_dump error: {result.stderr.decode()}")
        
        # Copiar filestore si existe
        filestore_path = FILESTORE_SOURCE.format(
            usuario=os.environ.get('USERNAME', 'tu_usuario_windows'),
            db=db_name
        )
        
        if os.path.exists(filestore_path):
            filestore_backup_dir = os.path.join(BACKUP_DIR, f'filestore_{db_name}_{fecha}')
            shutil.copytree(filestore_path, filestore_backup_dir)
            print(f"[SUCCESS] Filestore copiado a: {filestore_backup_dir}")
        else:
            print(f"[WARNING] Filestore no encontrado en: {filestore_path}")
        
        print(f"[SUCCESS] Backup creado: {backup_file}")
        return True

    except Exception as e:
        print(f"[ERROR] Fallo en backup: {str(e)}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Crear backup de base de datos Odoo')
    parser.add_argument('--db', help='Nombre de la base de datos (opcional)')
    args = parser.parse_args()
    
    if crear_backup_windows(args.db):
        sys.exit(0)
    else:
        sys.exit(1)
