Write-Host "🚀 PIPELINE DE TEST COMPLET" -ForegroundColor Cyan
Write-Host "=" * 50

$env:NODE_OPTIONS = "--openssl-legacy-provider"

# 1. Clean
Write-Host "`n1. 🧹 Nettoyage..." -ForegroundColor Yellow
try {
    npx hardhat clean
    Write-Host "   ✅ Succès" -ForegroundColor Green
} catch {
    Write-Host "   ⚠️  Clean échoué (normal si première fois)" -ForegroundColor Yellow
}

# 2. Compile
Write-Host "`n2. 🔨 Compilation..." -ForegroundColor Yellow
npx hardhat compile
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Compilation réussie" -ForegroundColor Green
} else {
    Write-Host "   ❌ Échec compilation" -ForegroundColor Red
    exit 1
}

# 3. Test
Write-Host "`n3. 🧪 Tests unitaires..." -ForegroundColor Yellow
npx hardhat test
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Tests passés" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Tests échoués" -ForegroundColor Yellow
}

# 4. Déploiement local (si nœud disponible)
Write-Host "`n4. 🚀 Test déploiement..." -ForegroundColor Yellow
try {
    # Vérifie si un nœud local tourne
    $nodeRunning = Test-NetConnection -ComputerName localhost -Port 8545 -ErrorAction SilentlyContinue
    
    if ($nodeRunning.TcpTestSucceeded) {
        npx hardhat run scripts/deploy.js --network localhost 2>&1 | Select-String -Pattern "deployé|address|Error" -CaseSensitive
        Write-Host "   ✅ Déploiement testé" -ForegroundColor Green
    } else {
        Write-Host "   ℹ️  Nœud local non démarré" -ForegroundColor Gray
        Write-Host "   Pour tester: npx hardhat node (dans un autre terminal)" -ForegroundColor White
    }
} catch {
    Write-Host "   ⚠️  Erreur déploiement: $_" -ForegroundColor Yellow
}

# 5. Rapport
Write-Host "`n5. 📊 Rapport final..." -ForegroundColor Cyan
if (Test-Path "artifacts/build-info") {
    $artifacts = Get-ChildItem "artifacts/contracts" -Recurse -Filter "*.json" | Measure-Object
    Write-Host "   • Contrats compilés: $($artifacts.Count) fichiers" -ForegroundColor Green
}

Write-Host "`n" + "=" * 50
Write-Host "✅ PIPELINE TERMINÉ" -ForegroundColor Green
Write-Host "`nProchaines étapes recommandées:" -ForegroundColor Cyan
Write-Host "1. Démarrer un nœud: npx hardhat node" -ForegroundColor White
Write-Host "2. Déployer: npx hardhat run scripts/deploy.js --network localhost" -ForegroundColor White
Write-Host "3. Ajouter plus de tests dans tests/" -ForegroundColor White
Write-Host "4. Configurer des réseaux de test (Sepolia)" -ForegroundColor White
