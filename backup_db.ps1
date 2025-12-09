# Database Backup Script
$Date = Get-Date -Format "yyyy-MM-dd_HH-mm"
$BackupFile = "./backups/db_backup_$Date.sql"

# Create backups directory if not exists
New-Item -ItemType Directory -Force -Path "./backups" | Out-Null

# Run Docker Backup (Postgres)
Write-Host "Backing up database to $BackupFile..."
docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U postgres postgres > $BackupFile

if ($?) {
    Write-Host "Backup Successful: $BackupFile" -ForegroundColor Green
}
else {
    Write-Host "Backup Failed!" -ForegroundColor Red
}
