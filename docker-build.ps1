# Build and run ERFDoc with Docker (PowerShell)

Write-Host "🧠 Building ERFDoc Docker image..." -ForegroundColor Cyan
docker-compose build

Write-Host "🚀 Starting ERFDoc..." -ForegroundColor Cyan
docker-compose up -d

Write-Host "✅ ERFDoc is running!" -ForegroundColor Green
Write-Host "📍 Access the application at: http://localhost:8501"
Write-Host ""
Write-Host "📊 View logs with: docker-compose logs -f erfdoc" -ForegroundColor Gray
Write-Host "🛑 Stop with: docker-compose down" -ForegroundColor Gray
