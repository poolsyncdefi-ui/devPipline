#!/usr/bin/env pwsh

Write-Host "🚀 PIPELINE DE DÉVELOPPEMENT COMPLET" -ForegroundColor Cyan
Write-Host "=" * 60

# Configuration
$env:NODE_OPTIONS = "--openssl-legacy-provider"
$network = "localhost"

function Step($number, $message, $action) {
    Write-Host "`n$number. $message..." -ForegroundColor Yellow
    try {
        & $action
        Write-Host "   ✅ Succès" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "   ❌ Échec : $_" -ForegroundColor Red
        return $false
    }
}

# 1. Nettoyage
Step 1 "🧹 Nettoyage" { npx hardhat clean 2>$null }

# 2. Compilation
$compileSuccess = Step 2 "🔨 Compilation" { npx hardhat compile }
if (-not $compileSuccess) { exit 1 }

# 3. Tests unitaires
$testSuccess = Step 3 "🧪 Tests unitaires" { npx hardhat test }
if (-not $testSuccess) {
    Write-Host "   ⚠️  Tests échoués, poursuite du pipeline..." -ForegroundColor Yellow
}

# 4. Déploiement local (si nœud disponible)
Write-Host "`n4. 🚀 Test de déploiement..." -ForegroundColor Yellow
try {
    # Vérifier si un nœud local tourne
    $nodeTest = Test-NetConnection -ComputerName localhost -Port 8545 -ErrorAction SilentlyContinue
    
    if ($nodeTest.TcpTestSucceeded) {
        $deployOutput = npx hardhat run scripts/deploy.mjs --network $network 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "   ✅ Déploiement réussi" -ForegroundColor Green
            # Extraire l'adresse
            if ($deployOutput -match "0x[0-9a-fA-F]{40}") {
                $contractAddress = $matches[0]
                Write-Host "   📍 Adresse : $contractAddress" -ForegroundColor Cyan
                $contractAddress | Out-File -FilePath ".deployed_address" -Encoding UTF8
            }
        } else {
            Write-Host "   ℹ️  Déploiement échoué (nœud peut être occupé)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "   ℹ️  Nœud local non démarré" -ForegroundColor Gray
        Write-Host "   Pour tester : démarrer avec: npx hardhat node" -ForegroundColor White
    }
} catch {
    Write-Host "   ⚠️  Erreur déploiement : $_" -ForegroundColor Yellow
}

# 5. Rapport final
Write-Host "`n" + "=" * 60
Write-Host "📊 RAPPORT FINAL" -ForegroundColor Cyan

if (Test-Path "artifacts/build-info") {
    $artifacts = (Get-ChildItem "artifacts/contracts" -Recurse -Filter "*.json" -ErrorAction SilentlyContinue).Count
    Write-Host " • Contrats compilés : $artifacts artefacts" -ForegroundColor Green
}

if (Test-Path ".deployed_address") {
    $addr = Get-Content ".deployed_address"
    Write-Host " • Contrat déployé : $addr" -ForegroundColor Green
}

Write-Host "`n🎉 PIPELINE TERMINÉ" -ForegroundColor Green
Write-Host "`nProchaines étapes recommandées :" -ForegroundColor White
Write-Host "1. Démarrer un nœud local : npx hardhat node" -ForegroundColor Gray
Write-Host "2. Déployer : npx hardhat run scripts/deploy.mjs --network localhost" -ForegroundColor Gray
Write-Host "3. Tester sur réseau de test (Sepolia) : configurer hardhat.config.mjs" -ForegroundColor Gray
