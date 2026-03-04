#!/bin/bash

# SmartCommerce Backend Setup Script

echo "🚀 SmartCommerce Backend Setup"
echo "================================"

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your configuration."
else
    echo "✅ .env file already exists"
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo ""
echo "🐳 Starting Docker services..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

echo ""
echo "🗄️  Running database migrations..."
docker-compose exec -T web python manage.py makemigrations
docker-compose exec -T web python manage.py migrate

echo ""
echo "👤 Creating superuser..."
echo "Please enter superuser details:"
docker-compose exec web python manage.py createsuperuser

echo ""
echo "✅ Setup complete!"
echo ""
echo "📍 Access points:"
echo "   - API: http://localhost:8000/api/"
echo "   - Admin: http://localhost:8000/admin/"
echo "   - WebSocket: ws://localhost:8000/ws/"
echo ""
echo "📚 Next steps:"
echo "   1. Login to admin panel and create some categories"
echo "   2. Create a vendor account"
echo "   3. Add some products"
echo "   4. Check API documentation in API_DOCUMENTATION.md"
echo ""
echo "🛠️  Useful commands:"
echo "   - View logs: docker-compose logs -f web"
echo "   - Stop services: docker-compose down"
echo "   - Restart: docker-compose restart"
echo ""
