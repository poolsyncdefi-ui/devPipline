Write-Host "=== VERSIONS INSTALLÉES ===" -ForegroundColor Cyan
Write-Host "`n📦 Node.js & npm:" -ForegroundColor Yellow
node --version
npm --version

Write-Host "`n⚡ Hardhat:" -ForegroundColor Yellow
try {
    npx hardhat --version
} catch {
    Write-Host "Hardhat non disponible" -ForegroundColor Red
}

Write-Host "`n📁 Dépendances principales:" -ForegroundColor Yellow
@("hardhat", "@nomicfoundation/hardhat-toolbox", "@openzeppelin/contracts", "ethers", "dotenv") | ForEach-Object {
    $pkg = $_
    try {
        $version = npm list $_ --depth=0 2>$null | Select-String -Pattern $_
        if ($version) {
            Write-Host "$pkg : $($version.ToString().Split('@')[-1])" -ForegroundColor Green
        } else {
            Write-Host "$pkg : Non installé" -ForegroundColor Gray
        }
    } catch {
        Write-Host "$pkg : Erreur" -ForegroundColor Red
    }
}

Write-Host "`n📊 Toutes les dépendances:" -ForegroundColor Yellow
npm list --depth=0 2>$null | Where-Object { $_ -match "@" } | ForEach-Object {
    $line = $_.ToString().Trim()
    if ($line -notmatch "^\s") {
        Write-Host "  $line" -ForegroundColor White
    }
}