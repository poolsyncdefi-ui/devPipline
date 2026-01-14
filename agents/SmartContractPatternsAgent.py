class SmartContractPatternsAgent:
    """Agent spécialisé dans les patterns et best practices Solidity"""
    
    def analyze_contract(self, contract_code):
        """Analyse complète d'un smart contract"""
        
        analysis = {
            'design_patterns': self.identify_design_patterns(contract_code),
            'security_patterns': self.check_security_patterns(contract_code),
            'gas_optimization': self.analyze_gas_usage(contract_code),
            'upgradeability': self.check_upgradeability(contract_code),
            'reentrancy_guards': self.check_reentrancy_protection(contract_code),
            'access_control': self.check_access_control(contract_code)
        }
        
        # Vérification des standards
        analysis['standards_compliance'] = self.check_standards(
            contract_code,
            ['ERC-20', 'ERC-721', 'ERC-1155', 'ERC-4626']
        )
        
        # Best practices spécifiques
        analysis['best_practices'] = {
            'checks_effects_interactions': self.check_cei_pattern(contract_code),
            'pull_vs_push': self.check_payment_patterns(contract_code),
            'error_handling': self.check_error_patterns(contract_code),
            'event_usage': self.check_event_usage(contract_code)
        }
        
        return analysis
    
    def identify_design_patterns(self, code):
        """Identifie les design patterns utilisés"""
        patterns = {
            'factory': self.detect_factory_pattern(code),
            'proxy': self.detect_proxy_pattern(code),
            'diamond': self.detect_diamond_pattern(code),
            'governance': self.detect_governance_pattern(code),
            'vesting': self.detect_vesting_pattern(code),
            'staking': self.detect_staking_pattern(code)
        }
        return {k: v for k, v in patterns.items() if v}