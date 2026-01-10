import os
import openai
from dotenv import load_dotenv

load_dotenv()

class ContractGeneratorAgent:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4"  # ou "gpt-3.5-turbo" pour moins cher
    
    def generate_contract(self, requirements):
        """Génère un smart contract basé sur des exigences"""
        prompt = f"""
        Tu es un expert Solidity. Génère un smart contract sécurisé avec:
        
        Exigences: {requirements}
        
        Règles:
        1. Utilise Solidity 0.8.20+
        2. Implémente OpenZeppelin quand possible
        3. Ajoute des commentaires NatSpec
        4. Inclure les fonctions essentielles
        5. Ajouter des modificateurs de sécurité
        
        Retourne SEULEMENT le code Solidity.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Tu es un expert en développement Web3 et sécurité des smart contracts."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Erreur: {e}"

# Test rapide
if __name__ == "__main__":
    agent = ContractGeneratorAgent()
    
    # Test avec des exigences simples
    requirements = "Un ERC20 token appelé 'Web3Token' avec symbol 'W3T', mintable par le owner, et burnable par les holders"
    
    print("🤖 Génération d'un contrat ERC20...")
    contract_code = agent.generate_contract(requirements)
    
    print("\n" + "="*50)
    print(contract_code[:500] + "..." if len(contract_code) > 500 else contract_code)
    print("="*50)
    
    # Sauvegarder dans un fichier
    with open("contracts/GeneratedToken.sol", "w") as f:
        f.write(contract_code)
    
    print("\n✅ Contrat sauvegardé dans contracts/GeneratedToken.sol")
