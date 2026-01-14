#!/bin/bash
# full_pipeline_execution.sh

echo "🚀 Lancement du Pipeline Multi-Agents"

# Phase 1: Analyse initiale
echo "🔍 Phase 1: Analyse avec Agents Spécialisés"
python agents/blockchain_specific_agent.py \
  --project "project_specs.json" \
  --output "analysis/blockchain_analysis.json"

python agents/crypto_compliance_agent.py \
  --jurisdiction "EU,US" \
  --output "analysis/compliance_report.json"

python agents/web_architecture_agent.py \
  --project "project_specs.json" \
  --output "analysis/web_architecture.json"

# Phase 2: Développement assisté
echo "⚙️ Phase 2: Développement avec Best Practices"
python agents/solidity_best_practices_agent.py \
  --generate \
  --template "erc20_advanced" \
  --output "contracts/ERC20Advanced.sol"

python agents/web3_frontend_agent.py \
  --generate \
  --framework "nextjs" \
  --features "wallet_connect, nft_gallery, swap_interface" \
  --output "frontend/"

# Phase 3: Audit multi-couche
echo "🛡️ Phase 3: Audit Sécurité Complet"
python agents/smart_contract_security_agent.py \
  --audit "contracts/" \
  --tools "slither,mythril,manual" \
  --output "audit/security_report.json"

python agents/crypto_security_agent.py \
  --audit "project_specs.json" \
  --output "audit/crypto_security.json"

python agents/web_security_agent.py \
  --audit "frontend/" \
  --owasp-level 2 \
  --output "audit/web_security.json"

# Phase 4: Performance et optimisation
echo "⚡ Phase 4: Tests Performance"
python agents/blockchain_performance_agent.py \
  --benchmark "contracts/" \
  --network "sepolia" \
  --iterations 100 \
  --output "performance/blockchain_benchmarks.json"

python agents/web_performance_agent.py \
  --audit "frontend/" \
  --lighthouse \
  --web-vitals \
  --output "performance/web_metrics.json"

python agents/gas_optimization_agent.py \
  --optimize "contracts/" \
  --target-reduction 20 \
  --output "optimization/gas_report.json"

# Phase 5: Validation et reporting
echo "📊 Phase 5: Validation et Rapport Final"
python validation/multi_agent_validator.py \
  --reports "analysis/,audit/,performance/" \
  --generate-dashboard \
  --output "reports/final_dashboard.html"

# Lancement du dashboard
echo "🌐 Lancement du Dashboard..."
python dashboard/server.py \
  --port 8080 \
  --reports "reports/" \
  --auto-refresh

echo "✅ Pipeline terminé avec succès!"
echo "📊 Dashboard disponible: http://localhost:8080"