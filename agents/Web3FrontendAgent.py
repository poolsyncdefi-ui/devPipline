class Web3FrontendAgent:
    """Agent spécialisé dans le frontend Web3"""
    
    def validate_frontend(self, frontend_code, blockchain_integration):
        """Valide un frontend Web3"""
        
        validation = {
            'wallet_integration': self.validate_wallet_integration(frontend_code),
            'web3_libraries': self.check_web3_libraries(frontend_code),
            'state_management': self.check_state_management(frontend_code),
            'error_handling': self.check_web3_error_handling(frontend_code),
            'loading_states': self.check_loading_states(frontend_code),
            'transaction_flow': self.check_transaction_flow(frontend_code)
        }
        
        # Intégration spécifique
        validation['integration'] = {
            'wagmi_hooks': self.check_wagmi_usage(frontend_code),
            'viem_actions': self.check_viem_usage(frontend_code),
            'rainbowkit': self.check_rainbowkit_integration(frontend_code),
            'transaction_monitoring': self.check_tx_monitoring(frontend_code)
        }
        
        # UX Web3 spécifique
        validation['ux_web3'] = {
            'gas_estimation_display': self.check_gas_display(frontend_code),
            'network_switching': self.check_network_switching(frontend_code),
            'wallet_connection_flow': self.check_wallet_connection(frontend_code),
            'mobile_compatibility': self.check_mobile_wallet_compatibility(frontend_code)
        }
        
        return validation