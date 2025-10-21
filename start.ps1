# Script de démarrage simplifié pour Windows PowerShell
# Lance le backend Flask et le frontend Next.js en parallèle

Write-Host "Démarrage de JowAfrique en mode développement" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Green

# Démarrer le backend
Write-Host "Démarrage du backend Flask..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; python api_endpoints.py"

# Attendre un peu
Start-Sleep -Seconds 3

# Démarrer le frontend
Write-Host "Démarrage du frontend Next.js..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host "`nServices démarrés:" -ForegroundColor Green
Write-Host "   Backend API: http://localhost:5000" -ForegroundColor Cyan
Write-Host "   Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "`nLes services s'exécutent dans des fenêtres séparées" -ForegroundColor Yellow
Write-Host "Fermez les fenêtres pour arrêter les services" -ForegroundColor Yellow
