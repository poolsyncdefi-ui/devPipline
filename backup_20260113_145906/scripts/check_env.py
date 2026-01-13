#!/usr/bin/env python3
"""
Script de vérification de l'environnement
"""
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_check(icon, text, details=""):
    print(f"{icon} {text:40} {details}")

def check_python():
    """Vérifie l'environnement Python"""
    print_header("PYTHON ENVIRONNEMENT")
    
    # Version Python
    version = sys.version.split()[0]
    print_check("🐍", f"Python {version}")
    
    # Environnement virtuel
    venv_path = os.environ.get('VIRTUAL_ENV', 'Non activé')
    if venv_path != 'Non activé':
        print_check("✅", "Virtual Environment", Path(venv_path).name)
    else:
        print_check("⚠️", "Virtual Environment", "Non activé")
    
    # Pip
    try:
        import pip
        print_check("📦", f"Pip {pip.__version__}")
    except:
        print_check("❌", "Pip", "Non disponible")

def check_node():
    """Vérifie l'environnement Node.js"""
    print_header("NODE.JS & HARHAT")
    
    try:
        # Version Node.js
        result = subprocess.run(["node", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print_check("⬢", f"Node.js {result.stdout.strip()}")
        else:
            print_check("❌", "Node.js", "Non disponible")
    except:
        print_check("❌", "Node.js", "Non installé")
    
    try:
        # Version npm
        result = subprocess.run(["npm", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print_check("📦", f"npm {result.stdout.strip()}")
    except:
        print_check("❌", "npm", "Non disponible")
    
    # Hardhat
    hardhat_config = Path("hardhat.config.js")
    if hardhat_config.exists():
        print_check("🛠️", "Hardhat", "Configuré")
        
        # Vérifier la compilation
        try:
            result = subprocess.run(["npx", "hardhat", "--version"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.split()[1]
                print_check("✅", f"Hardhat CLI", f"v{version}")
        except:
            print_check("⚠️", "Hardhat CLI", "Erreur d'exécution")
    else:
        print_check("❌", "Hardhat", "Config manquante")

def check_python_packages():
    """Vérifie les packages Python installés"""
    print_header("PYTHON PACKAGES")
    
    required_packages = [
        ("web3", "Blockchain"),
        ("openai", "IA - OpenAI"),
        ("anthropic", "IA - Claude"),
        ("langchain", "IA - Framework"),
        ("eth_account", "Wallets"),
        ("py_solc_x", "Compilation Solidity"),
        ("watchdog", "Surveillance fichiers"),
        ("pydantic", "Validation données")
    ]
    
    for package, description in required_packages:
        try:
            module = __import__(package.replace("-", "_"))
            version = getattr(module, "__version__", "✓")
            print_check("✅", f"{description}", f"{version}")
        except ImportError:
            print_check("❌", f"{description}", "Manquant")

def check_api_keys():
    """Vérifie les clés API configurées"""
    print_header("CLÉS API")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    api_keys = [
        ("OPENAI_API_KEY", "OpenAI", "sk-"),
        ("ANTHROPIC_API_KEY", "Anthropic", "sk-ant-"),
        ("INFURA_API_KEY", "Infura", "32 chars"),
        ("ETHERSCAN_API_KEY", "Etherscan", "Verified")
    ]
    
    for env_var, service, expected_format in api_keys:
        value = os.getenv(env_var, "")
        
        if not value:
            print_check("❌", f"{service}", "Non configuré")
        elif expected_format and expected_format in value:
            print_check("✅", f"{service}", "Configuré")
        else:
            print_check("⚠️", f"{service}", "Format suspect")

def check_project_structure():
    """Vérifie la structure du projet"""
    print_header("STRUCTURE PROJET")
    
    required_dirs = [
        ("contracts/", "Smart Contracts"),
        ("tests/", "Tests"),
        ("scripts/", "Scripts"),
        ("agents/", "Agents IA"),
        ("pipeline/", "Pipeline"),
        ("logs/", "Logs")
    ]
    
    for dir_path, description in required_dirs:
        if Path(dir_path).exists():
            items = list(Path(dir_path).iterdir())
            count = len([i for i in items if i.is_file()])
            print_check("📁", f"{description}", f"{count} fichiers")
        else:
            print_check("❌", f"{description}", "Manquant")

def check_smart_contracts():
    """Vérifie les smart contracts"""
    print_header("SMART CONTRACTS")
    
    contracts_dir = Path("contracts")
    if contracts_dir.exists():
        sol_files = list(contracts_dir.glob("**/*.sol"))
        
        if sol_files:
            print_check("📄", "Contrats Solidity", f"{len(sol_files)} fichier(s)")
            
            for sol_file in sol_files[:3]:  # Afficher les 3 premiers
                size = sol_file.stat().st_size
                print_check("   ", f"  {sol_file.name}", f"{size:,} bytes")
            
            if len(sol_files) > 3:
                print(f"     ... et {len(sol_files) - 3} autres")
        else:
            print_check("⚠️", "Contrats Solidity", "Aucun fichier .sol")
    else:
        print_check("❌", "Dossier contracts", "Manquant")

def main():
    """Fonction principale"""
    print("\n" + "="*60)
    print("           VÉRIFICATION ENVIRONNEMENT WEB3 AI")
    print("="*60)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Projet: {Path.cwd().name}")
    print("="*60)
    
    try:
        check_python()
        check_node()
        check_python_packages()
        check_api_keys()
        check_project_structure()
        check_smart_contracts()
        
        print_header("🎯 RÉSUMÉ & RECOMMANDATIONS")
        
        print("\nCommandes disponibles:")
        print("  • npx hardhat compile     # Compiler les contrats")
        print("  • npx hardhat test        # Exécuter les tests")
        print("  • python pipeline/orchestrator.py --mode watch")
        print("  • python agents/blockchain/contract_generator.py")
        
        print("\nProchaines étapes:")
        print("  1. Configurez les clés API manquantes dans .env")
        print("  2. Lancez le pipeline: python pipeline/orchestrator.py")
        print("  3. Testez avec: npx hardhat test")
        
        print("\n" + "="*60)
        print("✅ Vérification terminée!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Erreur pendant la vérification: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())