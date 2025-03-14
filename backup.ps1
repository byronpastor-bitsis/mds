# Configuración
$Fecha = Get-Date -Format "yyyyMMdd_HHmmss"
$DBName = "odoo-database"
$BackupDir = "C:\Users\HP\Desktop\dev\odoo-local\backup"
$FilestoreDir = "C:\Users\HP\.local\share\Odoo\filestore\$DBName"

# Crear directorio de backup si no existe
if (-Not (Test-Path -Path $BackupDir)) {
    New-Item -ItemType Directory -Path $BackupDir
}

# Backup de PostgreSQL
$BackupFileSQL = "$BackupDir\${DBName}_${Fecha}.dump"
pg_dump -U postgres -F c -b -v -f $BackupFileSQL $DBName

# Verificar dump
if (-Not (Test-Path -Path $BackupFileSQL)) {
    Write-Error "Error al crear el backup de la base de datos"
    exit 1
}

# Verificar filestore
if (-Not (Test-Path -Path $FilestoreDir)) {
    Write-Error "El directorio filestore no existe: $FilestoreDir"
    exit 1
}

# Comprimir TODO en un solo archivo (usando 7-Zip para eficiencia)
$BackupFileFinal = "$BackupDir\${DBName}_backup_${Fecha}.7z"
& "C:\Program Files\7-Zip\7z.exe" a -t7z $BackupFileFinal $BackupFileSQL $FilestoreDir

# Eliminar temporal .dump
Remove-Item -Path $BackupFileSQL

# Eliminar backups antiguos (30 días)
Get-ChildItem -Path $BackupDir -Filter *.7z | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30) } | Remove-Item -Force

Write-Output "Backup completado: $BackupFileFinal"
