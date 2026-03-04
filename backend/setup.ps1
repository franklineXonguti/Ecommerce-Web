# SmartCommerce Backend Setup Script (PowerShell)

Write-Host "🚀 SmartCommerce Backend Setup" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Check if .env exists
if (-not (Test-Path .env)) {
    Write-Host "📝 Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "✅ .env file created. Please edit it with your configuration." -ForegroundColor Green
} else {
    Write-Host "✅ .env file already exists" -ForegroundColor Green
}

# Check if Docker is running
try {
    docker info | Out-Null
} catch {
    Write-Host "❌ Docker is not running. Please start Docker and try again." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🐳 Starting Docker services..." -ForegroundColor Cyan
docker-compose up -d

Write-Host ""
Write-Host "⏳ Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host ""
Write-Host "🗄️  Running database migrations..." -ForegroundColor Cyan
docker-compose exec -T web python manage.py makemigrations
docker-compose exec -T web python manage.py migrate

Write-Host ""
Write-Host "👤 Creating superuser..." -ForegroundColor Cyan
Write-Host "Please enter superuser details:" -ForegroundColor Yellow
docker-compose exec web python manage.py createsuperuser

Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Access points:" -ForegroundColor Cyan
Write-Host "   - API: http://localhost:8000/api/"
Write-Host "   - Admin: http://localhost:8000/admin/"
Write-Host "   - WebSocket: ws://localhost:8000/ws/"
Write-Host ""
Write-Host "📚 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Login to admin panel and create some categories"
Write-Host "   2. Create a vendor account"
Write-Host "   3. Add some products"
Write-Host "   4. Check API documentation in API_DOCUMENTATION.md"
Write-Host ""
Write-Host "🛠️  Useful commands:" -ForegroundColor Cyan
Write-Host "   - View logs: docker-compose logs -f web"
Write-Host "   - Stop services: docker-compose down"
Write-Host "   - Restart: docker-compose restart"
Write-Host ""
