class WebPerformanceAgent:
    """Agent spécialisé en performance Web"""
    
    def analyze_web_performance(self, frontend_code, blockchain_context):
        """Analyse de performance pour applications Web3"""
        
        metrics = {
            'core_web_vitals': self.measure_core_web_vitals(frontend_code),
            'blockchain_specific': self.measure_blockchain_performance(frontend_code),
            'bundle_optimization': self.analyze_bundle_size(frontend_code),
            'caching_strategy': self.check_caching(frontend_code),
            'lazy_loading': self.check_lazy_loading(frontend_code)
        }
        
        # Métriques spécifiques Web3
        metrics['web3_performance'] = {
            'rpc_call_optimization': self.optimize_rpc_calls(frontend_code),
            'multicall_usage': self.check_multicall_usage(frontend_code),
            'indexer_integration': self.check_indexer_usage(frontend_code),
            'offchain_computation': self.check_offchain_computation(frontend_code)
        }
        
        # Optimisations recommandées
        recommendations = self.generate_performance_recommendations(metrics)
        
        return {
            'metrics': metrics,
            'recommendations': recommendations,
            'score': self.calculate_performance_score(metrics)
        }