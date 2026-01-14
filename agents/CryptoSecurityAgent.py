class CryptoSecurityAgent:
    """Agent spécialisé en sécurité cryptographique et wallets"""
    
    def validate_crypto_security(self, project):
        """Valide la sécurité cryptographique"""
        
        security_report = {
            'key_management': self.validate_key_management(project),
            'signature_security': self.validate_signature_schemes(project),
            'encryption': self.validate_encryption(project),
            'randomness': self.validate_randomness_generation(project),
            'wallet_security': self.validate_wallet_security(project)
        }
        
        # Standards cryptographiques
        security_report['crypto_standards'] = {
            'ECDSA_usage': self.check_ecdsa_usage(project),
            'BLS_signatures': self.check_bls_signatures(project),
            'zk_snarks': self.check_zk_snarks(project),
            'multi_sig': self.check_multisig_implementation(project)
        }
        
        # Bonnes pratiques
        security_report['best_practices'] = {
            'private_key_storage': self.check_private_key_storage(project),
            'mnemonic_handling': self.check_mnemonic_handling(project),
            'transaction_signing': self.check_tx_signing(project),
            'nonce_management': self.check_nonce_management(project)
        }
        
        return security_report