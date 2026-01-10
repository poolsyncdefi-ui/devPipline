"""
Agent IA pour générer des smart contracts Solidity
"""
import os
import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ContractGeneratorAgent:
    """Agent IA pour génération et analyse de smart contracts"""
    
    def __init__(self, ai_provider: str = "openai"):
        """
        Initialise l'agent avec le provider IA spécifié
        
        Args:
            ai_provider: "openai", "anthropic", ou "google"
        """
        self.ai_provider = ai_provider
        self.project_root = Path(__file__).parent.parent.parent
        self.setup_ai_client()
        
    def setup_ai_client(self):
        """Configure le client IA selon le provider"""
        try:
            if self.ai_provider == "openai":
                import openai
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key or api_key == "sk-xxx":
                    raise ValueError("OPENAI_API_KEY non configuré dans .env. Remplace 'sk-xxx' par ta vraie clé.")
                
                # Configuration pour OpenAI v1.0+
                from openai import OpenAI
                self.client = OpenAI(api_key=api_key)
                self.model = "gpt-4"  # ou "gpt-3.5-turbo"
                
            elif self.ai_provider == "anthropic":
                from anthropic import Anthropic
                api_key = os.getenv("ANTHROPIC_API_KEY")
                if not api_key:
                    raise ValueError("ANTHROPIC_API_KEY non configuré dans .env")
                self.client = Anthropic(api_key=api_key)
                self.model = "claude-3-5-sonnet-20241022"
                
            elif self.ai_provider == "google":
                import google.generativeai as genai
                api_key = os.getenv("GOOGLE_AI_API_KEY")
                if not api_key:
                    raise ValueError("GOOGLE_AI_API_KEY non configuré dans .env")
                genai.configure(api_key=api_key)
                self.client = genai
                self.model = "gemini-pro"
                
            else:
                raise ValueError(f"Provider IA non supporté: {self.ai_provider}")
                
            logger.info(f"✅ Agent IA configuré avec {self.ai_provider}")
            
        except ImportError as e:
            logger.error(f"❌ Package manquant: {e}. Installe avec: pip install {self.ai_provider}")
            raise
        except Exception as e:
            logger.error(f"❌ Erreur configuration IA: {e}")
            raise
    
    def generate_contract(self, requirements: str, contract_type: str = "custom") -> Dict[str, Any]:
        """
        Génère un smart contract complet basé sur des exigences
        
        Args:
            requirements: Description textuelle des exigences
            contract_type: Type de contrat (erc20, erc721, erc1155, custom)
            
        Returns:
            Dict avec code, analyse et métadonnées
        """
        logger.info(f"Génération d'un contrat {contract_type}...")
        
        # Prompt optimisé pour Solidity
        prompt = self._build_generation_prompt(requirements, contract_type)
        
        try:
            # Appel au modèle IA
            if self.ai_provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system", 
                            "content": self._get_system_prompt()
                        },
                        {
                            "role": "user", 
                            "content": prompt
                        }
                    ],
                    temperature=0.1,
                    max_tokens=4000
                )
                generated_code = response.choices[0].message.content.strip()
                
            elif self.ai_provider == "anthropic":
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=4000,
                    temperature=0.1,
                    system=self._get_system_prompt(),
                    messages=[{"role": "user", "content": prompt}]
                )
                generated_code = response.content[0].text
                
            elif self.ai_provider == "google":
                import google.generativeai as genai
                model = genai.GenerativeModel(self.model)
                response = model.generate_content(
                    prompt,
                    generation_config=genai.GenerationConfig(
                        temperature=0.1,
                        max_output_tokens=4000,
                    )
                )
                generated_code = response.text
            
            else:
                raise ValueError(f"Provider {self.ai_provider} non implémenté")
            
            # Analyse et validation du code généré
            analysis = self._analyze_generated_code(generated_code, contract_type)
            
            # Préparation du résultat
            result = {
                "timestamp": datetime.now().isoformat(),
                "contract_type": contract_type,
                "requirements": requirements,
                "ai_provider": self.ai_provider,
                "model": self.model,
                "code": generated_code,
                "analysis": analysis,
                "file_name": self._generate_filename(contract_type),
                "status": "success" if analysis["is_valid"] else "needs_review"
            }
            
            logger.info(f"✅ Contrat généré: {analysis['summary']}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Erreur génération: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "status": "error",
                "error": str(e),
                "code": "",
                "analysis": {}
            }
    
    def _build_generation_prompt(self, requirements: str, contract_type: str) -> str:
        """Construit le prompt pour la génération"""
        
        type_specific_rules = {
            "erc20": """
            - Implémenter toutes les fonctions ERC20 standard
            - Inclure les événements Transfer et Approval
            - Ajouter les extensions: mintable, burnable si demandé
            """,
            "erc721": """
            - Implémenter toutes les fonctions ERC721 standard
            - Gérer les tokenURI correctement
            - Considérer ERC721Enumerable et ERC721URIStorage
            """,
            "erc1155": """
            - Implémenter le multi-token standard
            - Gérer les balances par type de token
            - Inclure les événements TransferSingle et TransferBatch
            """,
            "custom": """
            - Analyser les exigences pour déterminer le meilleur standard
            - Prioriser la sécurité et la gas efficiency
            """
        }
        
        return f"""
        TU ES UN EXPERT SOLIDITY ET SÉCURITÉ WEB3.
        
        # MISSION
        Génère un smart contract Solidity SÉCURISÉ et OPTIMISÉ basé sur:
        
        TYPE: {contract_type.upper()}
        EXIGENCES: {requirements}
        
        # RÈGLES STRICTES
        1. Solidity ^0.8.20 avec pragma strict
        2. Utiliser OpenZeppelin imports quand possible
        3. Implémenter les standards ERC complètement
        4. AJOUTER DES COMMENTAIRES NATSPEC POUR TOUTES LES FONCTIONS
        5. Inclure les modificateurs: onlyOwner, nonReentrant si nécessaire
        6. Gérer les erreurs avec require et messages clairs
        7. Optimiser le gas usage
        8. Prévenir les vulnérabilités: reentrancy, overflow, access control
        
        # RÈGLES SPÉCIFIQUES
        {type_specific_rules.get(contract_type, type_specific_rules['custom'])}
        
        # FORMAT DE SORTIE
        Retourne UNIQUEMENT le code Solidity complet et valide.
        Commence directement par "// SPDX-License-Identifier:".
        Pas d'explications, pas de markdown, juste le code.
        
        # EXEMPLE DE STRUCTURE:
        // SPDX-License-Identifier: MIT
        pragma solidity ^0.8.20;
        
        import "@openzeppelin/contracts/...";
        
        /**
         * @title NomDuContrat
         * @dev Description détaillée
         */
        contract NomDuContrat {{ ... }}
        """
    
    def _get_system_prompt(self) -> str:
        """Retourne le prompt système pour l'IA"""
        return """
        Tu es un expert senior en développement Solidity et sécurité blockchain.
        Tes contrats sont utilisés en production avec des millions en valeur.
        
        TES PRINCIPES:
        1. SÉCURITÉ d'abord - auditée, testée, battle-tested
        2. GAS OPTIMIZATION - chaque opération compte
        3. READABILITY - code clair, commentaires NatSpec
        4. STANDARDS - suivre les meilleures pratiques de l'industrie
        5. UPGRADEABILITY - penser à l'évolution du contrat
        
        TU NE DOIS JAMAIS:
        - Oublier les checks d'overflow/underflow
        - Utiliser .transfer() ou .send()
        - Exposer des fonctions sensibles sans access control
        - Négliger les événements pour la traçabilité
        """
    
    def _analyze_generated_code(self, code: str, expected_type: str) -> Dict[str, Any]:
        """Analyse le code généré pour la qualité et sécurité"""
        
        analysis = {
            "is_valid": True,
            "issues": [],
            "warnings": [],
            "security_checks": {},
            "summary": "",
            "line_count": len(code.split('\n')),
            "has_pragma": "pragma solidity" in code,
            "has_spdx": "SPDX-License-Identifier" in code,
            "has_imports": "import" in code,
            "has_natspec": "@dev" in code or "@title" in code,
            "has_events": "event " in code,
            "has_requires": "require(" in code,
            "has_modifiers": "modifier " in code or "onlyOwner" in code,
            "has_reentrancy_guard": "nonReentrant" in code or "ReentrancyGuard" in code
        }
        
        # Vérifications de sécurité basiques
        if ".call.value" in code or ".call{" in code:
            analysis["issues"].append("Usage de .call.value() - risque de reentrancy")
            analysis["is_valid"] = False
            
        if "tx.origin" in code:
            analysis["warnings"].append("Usage de tx.origin - pattern non sécurisé, utiliser msg.sender")
            
        if expected_type == "erc20" and "function transfer" not in code:
            analysis["warnings"].append("Fonction transfer manquante pour ERC20")
            
        if "unchecked" in code and "SafeMath" not in code and "0.8" in code:
            analysis["warnings"].append("Blocks unchecked sans SafeMath - vérifier les arithmetic operations")
        
        # Vérifications de sécurité
        analysis["security_checks"] = {
            "reentrancy_risk": ".call.value" not in code and ".call{" not in code,
            "access_control": "onlyOwner" in code or "access control" in code.lower(),
            "error_handling": "require(" in code or "revert" in code,
            "overflow_protection": "unchecked" not in code or "0.8" in code,
            "events_emitted": "event " in code and "emit " in code
        }
        
        # Résumé
        issue_count = len(analysis["issues"]) + len(analysis["warnings"])
        status = "VALIDE" if analysis["is_valid"] else "À REVOIR"
        analysis["summary"] = f"Contrat {expected_type.upper()} - {analysis['line_count']} lignes - {status} - {issue_count} problème(s)"
        
        return analysis
    
    def _generate_filename(self, contract_type: str) -> str:
        """Génère un nom de fichier unique"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"Generated_{contract_type}_{timestamp}.sol"
    
    def save_contract(self, generation_result: Dict[str, Any], output_dir: Optional[Path] = None) -> Path:
        """
        Sauvegarde le contrat généré dans un fichier
        
        Args:
            generation_result: Résultat de generate_contract()
            output_dir: Dossier de sortie (défaut: contracts/generated/)
            
        Returns:
            Chemin du fichier créé
        """
        if output_dir is None:
            output_dir = self.project_root / "contracts" / "generated"
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = generation_result.get("file_name", "GeneratedContract.sol")
        filepath = output_dir / filename
        
        # Sauvegarde du code
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(generation_result["code"])
        
        # Sauvegarde des métadonnées
        metadata = {k: v for k, v in generation_result.items() if k != "code"}
        metafile = filepath.with_suffix('.json')
        with open(metafile, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, default=str)
        
        logger.info(f"💾 Contrat sauvegardé: {filepath}")
        logger.info(f"   Métadonnées: {metafile}")
        
        return filepath


# Interface CLI simplifiée
def main():
    """Point d'entrée pour l'agent"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Agent IA de génération de smart contracts")
    parser.add_argument("--requirements", "-r", required=False, 
                       default="Un token ERC20 simple avec mint et burn",
                       help="Exigences du contrat")
    parser.add_argument("--type", "-t", default="erc20", 
                       choices=["erc20", "erc721", "erc1155", "custom"],
                       help="Type de contrat à générer")
    parser.add_argument("--provider", "-p", default="openai",
                       choices=["openai", "anthropic", "google"],
                       help="Provider IA à utiliser")
    parser.add_argument("--save", "-s", action="store_true",
                       help="Sauvegarder le contrat généré")
    
    args = parser.parse_args()
    
    print("🤖 Agent de Génération de Contrats Solidity")
    print("=" * 50)
    
    try:
        # Initialiser l'agent
        print(f"🔧 Initialisation avec {args.provider}...")
        agent = ContractGeneratorAgent(ai_provider=args.provider)
        
        # Générer le contrat
        print(f"🎯 Génération d'un contrat {args.type.upper()}...")
        result = agent.generate_contract(args.requirements, args.type)
        
        if result["status"] == "error":
            print(f"❌ Erreur: {result.get('error', 'Unknown error')}")
            
            # Vérification clé API
            if "OPENAI_API_KEY" in str(result.get('error', '')):
                print("\n🔑 PROBLÈME CLÉ API:")
                print("   1. Ouvre ton fichier .env")
                print("   2. Remplace 'sk-xxx' par ta vraie clé OpenAI")
                print("   3. Obten une clé sur: https://platform.openai.com/api-keys")
            
            return 1
        
        # Afficher le résultat
        print(f"\n✅ {result['analysis']['summary']}")
        
        if result["analysis"]["issues"]:
            print("\n⚠️  Problèmes détectés:")
            for issue in result["analysis"]["issues"]:
                print(f"   • {issue}")
        
        if result["analysis"]["warnings"]:
            print("\n📝 Avertissements:")
            for warning in result["analysis"]["warnings"]:
                print(f"   • {warning}")
        
        # Sauvegarder si demandé
        if args.save and result["code"]:
            filepath = agent.save_contract(result)
            print(f"\n💾 Sauvegardé: {filepath}")
        
        # Afficher un aperçu du code
        print(f"\n📄 Aperçu du code ({result['analysis']['line_count']} lignes):")
        print("-" * 50)
        lines = result["code"].split('\n')[:15]
        for i, line in enumerate(lines, 1):
            print(f"{i:3d} | {line}")
        if len(result["code"].split('\n')) > 15:
            print("     ... (tronqué)")
        print("-" * 50)
        
        return 0
        
    except Exception as e:
        print(f"❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())