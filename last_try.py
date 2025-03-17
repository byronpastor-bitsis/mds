import xmlrpc.client
import datetime

# Configurar la conexión con Odoo
url = 'http://localhost:8069'  # Cambia según tu configuración
db = 'nombre_de_tu_base_de_datos'
username = 'admin'
password = 'tu_contraseña'

# Conectar con Odoo
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

if uid:
    # Crear la conexión al modelo 'db.backup' en Odoo
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

    # Generar el backup
    backup_name = f'backup_{db}_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.zip'
    backup = models.execute_kw(db, uid, password, 'db.backup', 'backup', [db])

    # Guardar el backup en un archivo
    with open(backup_name, 'wb') as f:
        f.write(backup)
    print(f'Backup guardado como {backup_name}')
else:
    print('Error al autenticar con Odoo')
