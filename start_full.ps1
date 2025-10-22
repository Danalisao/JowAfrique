# Script de démarrage complet JowAfrique
Write-Host "🚀 Démarrage de JowAfrique - Frontend + Backend" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Cyan

# Fonction pour vérifier si un port est utilisé
function Test-Port {
    param([int]$Port)
    try {
        $connection = New-Object System.Net.Sockets.TcpClient
        $connection.Connect("localhost", $Port)
        $connection.Close()
        return $true
    } catch {
        return $false
    }
}

# Vérifier les ports
if (Test-Port 5000) {
    Write-Host "⚠️  Port 5000 déjà utilisé (Backend)" -ForegroundColor Yellow
}

if (Test-Port 3000) {
    Write-Host "⚠️  Port 3000 déjà utilisé (Frontend)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📋 Instructions:" -ForegroundColor Cyan
Write-Host "1. Ouvrez un terminal pour le backend" -ForegroundColor White
Write-Host "2. Ouvrez un autre terminal pour le frontend" -ForegroundColor White
Write-Host "3. Ou utilisez les scripts individuels:" -ForegroundColor White
Write-Host "   - .\start_backend.ps1" -ForegroundColor Green
Write-Host "   - .\start_frontend.ps1" -ForegroundColor Green
Write-Host ""

# Demander à l'utilisateur ce qu'il veut faire
$choice = Read-Host "Voulez-vous démarrer le backend maintenant? (y/n)"
if ($choice -eq "y" -or $choice -eq "Y") {
    Write-Host "🔥 Démarrage du backend..." -ForegroundColor Cyan
    .\start_backend.ps1
} else {
    Write-Host "💡 Utilisez .\start_backend.ps1 pour démarrer le backend" -ForegroundColor Yellow
    Write-Host "💡 Utilisez .\start_frontend.ps1 pour démarrer le frontend" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🌐 URLs:" -ForegroundColor Cyan
Write-Host "Backend API: http://localhost:5000" -ForegroundColor Green
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Green
Write-Host "Health Check: http://localhost:5000/api/health" -ForegroundColor Green
