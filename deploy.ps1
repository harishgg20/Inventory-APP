# Deployment Script
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Docker is not found in your PATH." -ForegroundColor Red
    Write-Host "Please install Docker Desktop from https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    Write-Host "If already installed, try restarting your terminal or computer." -ForegroundColor Yellow
    exit 1
}

Write-Host "Starting Production Deployment..." -ForegroundColor Green

# 1. Build and Run (Using 'docker compose' v2)
docker compose -f docker-compose.prod.yml up -d --build

# 2. Status Check
Write-Host "Waiting for services..."
Start-Sleep -Seconds 10
docker compose -f docker-compose.prod.yml ps

# 3. Collect Static Files (Important for Nginx)
Write-Host "Collecting Static Files..."
docker compose -f docker-compose.prod.yml exec -T web python manage.py collectstatic --noinput

Write-Host "Deployment Complete! Web accessible at http://localhost" -ForegroundColor Cyan
