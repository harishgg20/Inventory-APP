$ErrorActionPreference = "Stop"

Write-Host "Installing requirements..."
pip install -r requirements.txt

Write-Host "Applying migrations..."
python manage.py makemigrations
python manage.py migrate

Write-Host "Creating superuser (admin/admin)..."
$env:DJANGO_SUPERUSER_PASSWORD = 'admin'
$env:DJANGO_SUPERUSER_USERNAME = 'admin'
$env:DJANGO_SUPERUSER_EMAIL = 'admin@example.com'
python manage.py createsuperuser --noinput 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Superuser might already exist, skipping."
}

Write-Host "Setup complete!"
Write-Host "Run 'python manage.py runserver' to start the application."
