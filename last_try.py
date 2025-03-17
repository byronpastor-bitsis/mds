import requests
import datetime

url = 'http://localhost:8069/web/database/backup'
db_name = 'nombre_de_tu_base_de_datos'
backup_path = f'backup_{db_name}_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.zip'

# Enviar la petición POST a Odoo
response = requests.post(url, data={
    'master_pwd': 'tu_contraseña_de_odoo',  # Clave maestra (configurada en odoo.conf)
    'name': db_name,
    'backup_format': 'zip'
})

# Guardar el archivo si la respuesta es correcta
if response.status_code == 200:
    with open(backup_path, 'wb') as f:
        f.write(response.content)
    print(f'✅ Backup guardado como {backup_path}')
else:
    print(f'❌ Error en la petición: {response.status_code} - {response.text}')

