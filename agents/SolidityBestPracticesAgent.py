class SolidityBestPracticesAgent:
    """Agent spécialisé dans les best practices Solidity"""
    
    def check_solidity_practices(self, contract_code):
        """Vérifie les best practices Solidity"""
        
        practices = {
            'style_guide': self.check_style_guide(contract_code),
            'naming_conventions': self.check_naming_conventions(contract_code),
            'comments_natspec': self.check_natspec_comments(contract_code),
            'function_ordering': self.check_function_ordering(contract_code),
            'modifier_usage': self.check_modifier_usage(contract_code),
            'error_handling': self.check_error_handling_practices(contract_code)
        }
        
        # Patterns recommandés
        practices['recommended_patterns'] = {
            'checks_effects_interactions': self.enforce_cei(contract_code),
            'pull_over_push': self.check_pull_pattern(contract_code),
            'upgradeability_patterns': self.check_upgrade_patterns(contract_code),
            'gas_optimization_patterns': self.check_gas_patterns(contract_code)
        }
        
        # Outils et frameworks
        practices['tooling'] = {
            'slither_checks': self.run_slither_checks(contract_code),
            'mythril_checks': self.run_mythril_checks(contract_code),
            'hardhat_best_practices': self.check_hardhat_config(contract_code),
            'foundry_standards': self.check_foundry_standards(contract_code)
        }
        
        return practices