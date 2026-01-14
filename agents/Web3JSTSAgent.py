class Web3JSTSAgent:
    """Agent spécialisé dans les best practices JS/TS Web3"""
    
    def validate_web3_js_code(self, code):
        """Valide le code JavaScript/TypeScript Web3"""
        
        validation = {
            'typescript_strictness': self.check_tsconfig_strictness(code),
            'web3_library_usage': self.check_web3_library_usage(code),
            'async_await_patterns': self.check_async_patterns(code),
            'error_handling': self.check_js_error_handling(code),
            'type_safety': self.check_type_safety(code)
        }
        
        # Patterns spécifiques Web3
        validation['web3_patterns'] = {
            'provider_management': self.check_provider_management(code),
            'signer_handling': self.check_signer_handling(code),
            'contract_instance_management': self.check_contract_instances(code),
            'event_listening': self.check_event_listeners(code)
        }
        
        # Performance Web3
        validation['performance'] = {
            'rpc_calls_optimization': self.optimize_rpc_calls_js(code),
            'batch_requests': self.check_batch_requests(code),
            'caching_strategies': self.check_caching_strategies(code),
            'polling_optimization': self.optimize_polling(code)
        }
        
        return validation