#!/bin/bash
# Build and run ERFDoc with Docker

echo "🧠 Building ERFDoc Docker image..."
docker-compose build

echo "🚀 Starting ERFDoc..."
docker-compose up -d

echo "✅ ERFDoc is running!"
echo "📍 Access the application at: http://localhost:8501"
echo ""
echo "📊 View logs with: docker-compose logs -f erfdoc"
echo "🛑 Stop with: docker-compose down"
