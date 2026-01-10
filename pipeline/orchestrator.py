"""
Orchestrateur principal du pipeline IA Web3
"""
import asyncio
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
from enum import Enum

# Configuration logging avancée
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)-20s | %(levelname)-8s | %(message)s',
    datefmt='%H:%M:%S',
    handlers=[
        logging.FileHandler("logs/pipeline.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class PipelinePhase(Enum):
    """Phases du pipeline"""
    CONCEPTION = "conception"
    DEVELOPMENT = "development"
    VALIDATION = "validation"
    DEPLOYMENT = "deployment"
    MONITORING = "monitoring"


class ValidationGate(Enum):
    """Portes de validation du pipeline"""
    REQUIREMENTS = "requirements"
    ARCHITECTURE = "architecture"
    SECURITY = "security"
    CODE_QUALITY = "code_quality"
    PERFORMANCE = "performance"
    COMPLIANCE = "compliance"


class AgentStatus(Enum):
    """Statut des agents"""
    IDLE = "idle"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    DISABLED = "disabled"


class Web3PipelineOrchestrator:
    """Orchestrateur principal du pipeline IA Web3"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.agents: Dict[str, Dict] = {}
        self.validation_gates: Dict[ValidationGate, bool] = {}
        self.current_phase: Optional[PipelinePhase] = None
        self.is_running = False
        
        # Initialisation
        self._setup_directories()
        self._load_configuration()
        self._initialize_agents()
        
        logger.info(f"🚀 Orchestrateur initialisé pour {project_root.name}")
    
    def _setup_directories(self):
        """Crée la structure de dossiers nécessaire"""
        directories = [
            "logs",
            "artifacts",
            "cache",
            "reports",
            "contracts/generated",
            "agents/blockchain",
            "agents/security",
            "agents/frontend",
            "agents/testing",
            ".validation-gates"
        ]
        
        for directory in directories:
            path = self.project_root / directory
            path.mkdir(parents=True, exist_ok=True)
    
    def _load_configuration(self):
        """Charge la configuration du pipeline"""
        config_path = self.project_root / "config" / "pipeline_config.json"
        
        if config_path.exists():
            import json
            with open(config_path, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = self._create_default_config()
            self._save_configuration()
    
    def _create_default_config(self) -> Dict[str, Any]:
        """Crée une configuration par défaut"""
        return {
            "pipeline": {
                "name": "Web3 AI Pipeline",
                "version": "1.0.0",
                "auto_start": False,
                "watch_mode": True,
                "max_concurrent_agents": 3
            },
            "agents": {
                "contract_generator": {
                    "enabled": True,
                    "provider": "openai",
                    "auto_save": True,
                    "validate_after_generate": True
                },
                "security_auditor": {
                    "enabled": True,
                    "tools": ["slither", "mythril"],
                    "auto_fix": False
                },
                "test_generator": {
                    "enabled": True,
                    "framework": "hardhat",
                    "coverage_target": 80
                },
                "deployment_manager": {
                    "enabled": True,
                    "networks": ["hardhat", "sepolia"],
                    "auto_verify": True
                }
            },
            "validation": {
                "gates": [
                    {"name": "requirements", "required": True},
                    {"name": "architecture", "required": True},
                    {"name": "security", "required": True},
                    {"name": "code_quality", "required": False},
                    {"name": "performance", "required": False}
                ],
                "strict_mode": True
            },
            "monitoring": {
                "enabled": True,
                "metrics_interval": 60,
                "alert_channels": []
            }
        }
    
    def _save_configuration(self):
        """Sauvegarde la configuration"""
        config_dir = self.project_root / "config"
        config_dir.mkdir(exist_ok=True)
        
        import json
        config_path = config_dir / "pipeline_config.json"
        
        with open(config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
        
        logger.info(f"📁 Configuration sauvegardée: {config_path}")
    
    def _initialize_agents(self):
        """Initialise tous les agents disponibles"""
        agents_config = self.config.get("agents", {})
        
        # Agent: Générateur de contrats
        if agents_config.get("contract_generator", {}).get("enabled", False):
            self.agents["contract_generator"] = {
                "name": "Contract Generator",
                "module": "agents.blockchain.contract_generator",
                "status": AgentStatus.IDLE,
                "last_run": None,
                "config": agents_config["contract_generator"]
            }
        
        # Agent: Auditeur de sécurité
        if agents_config.get("security_auditor", {}).get("enabled", False):
            self.agents["security_auditor"] = {
                "name": "Security Auditor",
                "module": "agents.security.audit_agent",
                "status": AgentStatus.IDLE,
                "last_run": None,
                "config": agents_config["security_auditor"]
            }
        
        # Agent: Générateur de tests
        if agents_config.get("test_generator", {}).get("enabled", False):
            self.agents["test_generator"] = {
                "name": "Test Generator",
                "module": "agents.testing.test_generator",
                "status": AgentStatus.IDLE,
                "last_run": None,
                "config": agents_config["test_generator"]
            }
        
        logger.info(f"🤖 {len(self.agents)} agents initialisés")
    
    async def run_agent(self, agent_name: str, task: str, **kwargs) -> Dict[str, Any]:
        """
        Exécute un agent spécifique
        
        Args:
            agent_name: Nom de l'agent
            task: Tâche à exécuter
            **kwargs: Arguments supplémentaires
            
        Returns:
            Résultats de l'exécution
        """
        if agent_name not in self.agents:
            return {
                "success": False,
                "error": f"Agent '{agent_name}' non trouvé",
                "agent": agent_name
            }
        
        agent = self.agents[agent_name]
        agent["status"] = AgentStatus.RUNNING
        
        logger.info(f"▶️  Exécution: {agent['name']} - {task}")
        
        try:
            # Import dynamique de l'agent
            import importlib.util
            
            module_path = self.project_root / agent["module"].replace(".", "/") + ".py"
            
            if not module_path.exists():
                # Créer un agent minimal si le fichier n'existe pas
                result = await self._create_minimal_agent(agent_name, task, **kwargs)
            else:
                spec = importlib.util.spec_from_file_location(agent_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if hasattr(module, 'run'):
                    result = await module.run(task, **kwargs)
                else:
                    result = {
                        "success": False,
                        "error": f"Module {agent_name} n'a pas de fonction 'run'",
                        "agent": agent_name
                    }
            
            # Mettre à jour le statut
            if result.get("success", False):
                agent["status"] = AgentStatus.SUCCESS
            else:
                agent["status"] = AgentStatus.FAILED
            
            agent["last_run"] = datetime.now().isoformat()
            
            # Sauvegarder les résultats
            self._save_agent_results(agent_name, result)
            
            return result
            
        except Exception as e:
            error_msg = f"Erreur exécution agent {agent_name}: {str(e)}"
            logger.error(error_msg)
            
            agent["status"] = AgentStatus.FAILED
            agent["last_run"] = datetime.now().isoformat()
            
            return {
                "success": False,
                "error": error_msg,
                "agent": agent_name,
                "traceback": str(e)
            }
    
    async def _create_minimal_agent(self, agent_name: str, task: str, **kwargs) -> Dict[str, Any]:
        """Crée un agent minimal si le fichier n'existe pas"""
        logger.warning(f"⚠️  Agent {agent_name} non trouvé, création minimaliste")
        
        if agent_name == "contract_generator":
            return {
                "success": True,
                "agent": agent_name,
                "task": task,
                "message": "Agent minimal - ajoutez le vrai agent dans agents/blockchain/",
                "timestamp": datetime.now().isoformat()
            }
        
        return {
            "success": False,
            "agent": agent_name,
            "error": f"Agent {agent_name} non implémenté",
            "suggestion": f"Créez le fichier agents/{agent_name.replace('_', '/')}.py"
        }
    
    def _save_agent_results(self, agent_name: str, results: Dict[str, Any]):
        """Sauvegarde les résultats d'un agent"""
        reports_dir = self.project_root / "reports" / "agents"
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        import json
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{agent_name}_{timestamp}.json"
        filepath = reports_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        logger.debug(f"📊 Résultats sauvegardés: {filepath}")
    
    async def run_validation_gate(self, gate: ValidationGate) -> Dict[str, Any]:
        """
        Exécute une porte de validation
        
        Args:
            gate: Porte de validation à exécuter
            
        Returns:
            Résultats de la validation
        """
        logger.info(f"🔍 Validation Gate: {gate.value}")
        
        validation_methods = {
            ValidationGate.REQUIREMENTS: self._validate_requirements,
            ValidationGate.ARCHITECTURE: self._validate_architecture,
            ValidationGate.SECURITY: self._validate_security,
            ValidationGate.CODE_QUALITY: self._validate_code_quality,
            ValidationGate.PERFORMANCE: self._validate_performance,
            ValidationGate.COMPLIANCE: self._validate_compliance
        }
        
        if gate in validation_methods:
            try:
                result = await validation_methods[gate]()
                self.validation_gates[gate] = result.get("passed", False)
                
                # Sauvegarder le rapport
                self._save_validation_report(gate, result)
                
                return result
            except Exception as e:
                error_result = {
                    "gate": gate.value,
                    "passed": False,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
                self.validation_gates[gate] = False
                return error_result
        else:
            return {
                "gate": gate.value,
                "passed": False,
                "error": f"Gate de validation inconnue: {gate}",
                "timestamp": datetime.now().isoformat()
            }
    
    async def _validate_requirements(self) -> Dict[str, Any]:
        """Valide les exigences du projet"""
        # Vérifier la présence de fichiers essentiels
        essential_files = [
            self.project_root / "contracts",
            self.project_root / "hardhat.config.js",
            self.project_root / ".env"
        ]
        
        missing_files = []
        for filepath in essential_files:
            if not filepath.exists():
                missing_files.append(str(filepath.relative_to(self.project_root)))
        
        return {
            "gate": "requirements",
            "passed": len(missing_files) == 0,
            "missing_files": missing_files,
            "checks": [
                {"check": "contracts directory", "passed": (self.project_root / "contracts").exists()},
                {"check": "hardhat.config.js", "passed": (self.project_root / "hardhat.config.js").exists()},
                {"check": ".env file", "passed": (self.project_root / ".env").exists()},
                {"check": "package.json", "passed": (self.project_root / "package.json").exists()}
            ],
            "timestamp": datetime.now().isoformat()
        }
    
    async def _validate_architecture(self) -> Dict[str, Any]:
        """Valide l'architecture du projet"""
        import subprocess
        
        # Vérifier la compilation Hardhat
        try:
            result = subprocess.run(
                ["npx", "hardhat", "compile"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            compiled = "Successfully" in result.stdout
            
            return {
                "gate": "architecture",
                "passed": compiled,
                "compilation_success": compiled,
                "output": result.stdout[-500:] if result.stdout else "",
                "checks": [
                    {"check": "Hardhat compilation", "passed": compiled},
                    {"check": "Solidity version", "passed": "0.8" in result.stdout if result.stdout else False}
                ],
                "timestamp": datetime.now().isoformat()
            }
            
        except subprocess.TimeoutExpired:
            return {
                "gate": "architecture",
                "passed": False,
                "error": "Timeout lors de la compilation",
                "timestamp": datetime.now().isoformat()
            }
    
    async def _validate_security(self) -> Dict[str, Any]:
        """Valide la sécurité du projet"""
        # Vérifications de sécurité basiques
        security_issues = []
        
        # Vérifier le fichier .env pour les clés sensibles en clair
        env_path = self.project_root / ".env"
        if env_path.exists():
            with open(env_path, 'r') as f:
                content = f.read()
                
                if "PRIVATE_KEY=0x" in content and "test test" not in content:
                    security_issues.append("Clé privée réelle dans .env - utiliser des variables d'environnement")
                
                if "MNEMONIC=" in content and "test test" not in content:
                    security_issues.append("Seed phrase réelle dans .env")
        
        return {
            "gate": "security",
            "passed": len(security_issues) == 0,
            "security_issues": security_issues,
            "checks": [
                {"check": "No private keys in .env", "passed": len(security_issues) == 0},
                {"check": ".env in .gitignore", "passed": self._is_env_gitignored()}
            ],
            "timestamp": datetime.now().isoformat()
        }
    
    def _is_env_gitignored(self) -> bool:
        """Vérifie si .env est dans .gitignore"""
        gitignore_path = self.project_root / ".gitignore"
        if gitignore_path.exists():
            with open(gitignore_path, 'r') as f:
                content = f.read()
                return ".env" in content
        return False
    
    async def _validate_code_quality(self) -> Dict[str, Any]:
        """Valide la qualité du code"""
        # Vérifications basiques de qualité
        issues = []
        
        # Vérifier les contrats Solidity
        contracts_dir = self.project_root / "contracts"
        if contracts_dir.exists():
            for sol_file in contracts_dir.glob("**/*.sol"):
                with open(sol_file, 'r') as f:
                    content = f.read()
                    
                    if "SPDX-License-Identifier" not in content:
                        issues.append(f"{sol_file.name}: Licence SPDX manquante")
                    
                    if "@dev" not in content and "@title" not in content:
                        issues.append(f"{sol_file.name}: Documentation NatSpec manquante")
        
        return {
            "gate": "code_quality",
            "passed": len(issues) == 0,
            "issues": issues,
            "file_count": len(list(contracts_dir.glob("**/*.sol"))) if contracts_dir.exists() else 0,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _validate_performance(self) -> Dict[str, Any]:
        """Valide la performance"""
        # Placeholder pour les vérifications de performance
        return {
            "gate": "performance",
            "passed": True,
            "message": "Vérifications de performance à implémenter",
            "timestamp": datetime.now().isoformat()
        }
    
    async def _validate_compliance(self) -> Dict[str, Any]:
        """Valide la conformité"""
        # Placeholder pour les vérifications de conformité
        return {
            "gate": "compliance",
            "passed": True,
            "message": "Vérifications de conformité à implémenter",
            "timestamp": datetime.now().isoformat()
        }
    
    def _save_validation_report(self, gate: ValidationGate, results: Dict[str, Any]):
        """Sauvegarde le rapport de validation"""
        reports_dir = self.project_root / "reports" / "validations"
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        import json
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"validation_{gate.value}_{timestamp}.json"
        filepath = reports_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2, default=str)
    
    async def run_pipeline_phase(self, phase: PipelinePhase) -> Dict[str, Any]:
        """
        Exécute une phase complète du pipeline
        
        Args:
            phase: Phase à exécuter
            
        Returns:
            Résultats de la phase
        """
        logger.info(f"🚀 Démarrage phase: {phase.value}")
        self.current_phase = phase
        self.is_running = True
        
        phase_results = {
            "phase": phase.value,
            "start_time": datetime.now().isoformat(),
            "agents_executed": [],
            "validations": [],
            "success": True
        }
        
        try:
            if phase == PipelinePhase.CONCEPTION:
                # Génération de contrat avec IA
                result = await self.run_agent(
                    "contract_generator",
                    "generate",
                    requirements="NFT Marketplace avec fonctionnalités de base",
                    contract_type="erc721"
                )
                phase_results["agents_executed"].append(result)
                
            elif phase == PipelinePhase.DEVELOPMENT:
                # Validation des exigences et architecture
                req_validation = await self.run_validation_gate(ValidationGate.REQUIREMENTS)
                arch_validation = await self.run_validation_gate(ValidationGate.ARCHITECTURE)
                
                phase_results["validations"].extend([req_validation, arch_validation])
                
                if not (req_validation.get("passed", False) and arch_validation.get("passed", False)):
                    phase_results["success"] = False
            
            elif phase == PipelinePhase.VALIDATION:
                # Validation sécurité et qualité
                sec_validation = await self.run_validation_gate(ValidationGate.SECURITY)
                quality_validation = await self.run_validation_gate(ValidationGate.CODE_QUALITY)
                
                phase_results["validations"].extend([sec_validation, quality_validation])
                
                if not (sec_validation.get("passed", False) and quality_validation.get("passed", False)):
                    phase_results["success"] = False
            
            elif phase == PipelinePhase.DEPLOYMENT:
                # Préparation au déploiement
                result = await self.run_agent(
                    "deployment_manager",
                    "prepare",
                    network="sepolia",
                    contract_name="SimpleNFT"
                )
                phase_results["agents_executed"].append(result)
            
            elif phase == PipelinePhase.MONITORING:
                # Surveillance continue
                logger.info("👁️  Surveillance activée")
                # À implémenter: monitoring en temps réel
            
        except Exception as e:
            phase_results["success"] = False
            phase_results["error"] = str(e)
            logger.error(f"❌ Erreur phase {phase.value}: {e}")
        
        phase_results["end_time"] = datetime.now().isoformat()
        phase_results["duration"] = (
            datetime.fromisoformat(phase_results["end_time"]) - 
            datetime.fromisoformat(phase_results["start_time"])
        ).total_seconds()
        
        # Sauvegarder les résultats
        self._save_phase_report(phase, phase_results)
        
        self.current_phase = None
        self.is_running = False
        
        logger.info(f"✅ Phase {phase.value} terminée: {'SUCCÈS' if phase_results['success'] else 'ÉCHEC'}")
        
        return phase_results
    
    def _save_phase_report(self, phase: PipelinePhase, results: Dict[str, Any]):
        """Sauvegarde le rapport de phase"""
        reports_dir = self.project_root / "reports" / "phases"
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        import json
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"phase_{phase.value}_{timestamp}.json"
        filepath = reports_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2, default=str)
    
    async def watch_mode(self):
        """Mode surveillance de fichiers"""
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
        
        logger.info("👁️  Mode surveillance activé")
        logger.info("   Surveillance des modifications de fichiers...")
        logger.info("   Ctrl+C pour arrêter")
        
        class PipelineFileHandler(FileSystemEventHandler):
            def __init__(self, orchestrator):
                self.orchestrator = orchestrator
                self.last_trigger = datetime.now()
            
            def on_modified(self, event):
                if not event.is_directory:
                    # Éviter les triggers trop fréquents
                    now = datetime.now()
                    if (now - self.last_trigger).seconds < 2:
                        return
                    
                    self.last_trigger = now
                    
                    filename = Path(event.src_path).name
                    logger.info(f"📄 Modifié: {filename}")
                    
                    # Déclencher des actions basées sur le type de fichier
                    if event.src_path.endswith('.sol'):
                        asyncio.create_task(self._handle_solidity_change(event.src_path))
                    elif event.src_path.endswith('.js'):
                        asyncio.create_task(self._handle_javascript_change(event.src_path))
            
            async def _handle_solidity_change(self, filepath):
                """Gère les modifications de fichiers Solidity"""
                logger.info(f"   → Validation du contrat: {Path(filepath).name}")
                
                # Exécuter la validation sécurité
                validation = await self.orchestrator.run_validation_gate(ValidationGate.SECURITY)
                
                if not validation.get("passed", False):
                    logger.warning(f"   ⚠️  Problèmes de sécurité détectés")
            
            async def _handle_javascript_change(self, filepath):
                """Gère les modifications de fichiers JavaScript"""
                if "test" in filepath:
                    logger.info(f"   → Tests modifiés, revalidation suggérée")
        
        event_handler = PipelineFileHandler(self)
        observer = Observer()
        observer.schedule(event_handler, str(self.project_root), recursive=True)
        observer.start()
        
        try:
            # Afficher le dashboard en temps réel
            asyncio.create_task(self._display_dashboard())
            
            while True:
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            observer.stop()
            logger.info("\n👋 Surveillance arrêtée")
        
        observer.join()
    
    async def _display_dashboard(self):
        """Affiche un dashboard en temps réel"""
        import time
        
        while True:
            await asyncio.sleep(5)
            
            # Afficher le statut actuel
            print("\n" + "=" * 60)
            print("📊 DASHBOARD PIPELINE IA WEB3")
            print("=" * 60)
            
            # Agents
            print("🤖 AGENTS:")
            for agent_name, agent in self.agents.items():
                status_icon = {
                    AgentStatus.IDLE: "⚪",
                    AgentStatus.RUNNING: "🟡",
                    AgentStatus.SUCCESS: "🟢",
                    AgentStatus.FAILED: "🔴",
                    AgentStatus.DISABLED: "⚫"
                }.get(agent["status"], "❓")
                
                print(f"  {status_icon} {agent['name']:20} {agent['status'].value}")
            
            # Validations
            print("\n🔍 VALIDATIONS:")
            for gate in ValidationGate:
                status = self.validation_gates.get(gate)
                icon = "🟢" if status else "🔴" if status is False else "⚪"
                print(f"  {icon} {gate.value.replace('_', ' ').title():20}")
            
            # Phase courante
            if self.current_phase:
                print(f"\n🚀 PHASE ACTUELLE: {self.current_phase.value.upper()}")
            
            print("=" * 60)
    
    def print_status(self):
        """Affiche le statut complet du pipeline"""
        print("\n" + "=" * 70)
        print("🚀 STATUT DU PIPELINE IA WEB3")
        print("=" * 70)
        
        # Informations projet
        print(f"📁 Projet: {self.project_root.name}")
        print(f"📅 Initialisé: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⚙️  Phase: {self.current_phase.value if self.current_phase else 'Aucune'}")
        print(f"🏃‍♂️ En cours: {'Oui' if self.is_running else 'Non'}")
        
        # Agents
        print(f"\n🤖 Agents ({len(self.agents)}):")
        for agent_name, agent in self.agents.items():
            enabled = agent['config'].get('enabled', False)
            status = agent['status'].value
            last_run = agent['last_run'][:19] if agent['last_run'] else 'Jamais'
            
            print(f"  • {agent['name']:25} {'✅' if enabled else '❌'} {status:10} {last_run}")
        
        # Validations
        print(f"\n🔍 Validations:")
        passed = sum(1 for v in self.validation_gates.values() if v)
        total = len(self.validation_gates)
        print(f"  Portes passées: {passed}/{total}")
        
        for gate, status in self.validation_gates.items():
            icon = "✅" if status else "❌" if status is False else "⚪"
            print(f"  {icon} {gate.value.replace('_', ' ').title()}")
        
        # Commandes disponibles
        print("\n🎯 Commandes disponibles:")
        print("  python pipeline/orchestrator.py --mode watch     # Mode surveillance")
        print("  python pipeline/orchestrator.py --phase develop  # Phase développement")
        print("  python pipeline/orchestrator.py --validate       # Validation complète")
        print("  python pipeline/orchestrator.py --agent generate # Exécuter un agent")
        
        print("=" * 70)


# Interface CLI principale
async def main():
    """Point d'entrée principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Orchestrateur du Pipeline IA Web3")
    parser.add_argument("--project", "-p", default=".", help="Chemin du projet")
    parser.add_argument("--mode", "-m", choices=["watch", "validate", "run"], default="watch",
                       help="Mode d'exécution")
    parser.add_argument("--phase", choices=[p.value for p in PipelinePhase],
                       help="Phase spécifique à exécuter")
    parser.add_argument("--agent", help="Agent spécifique à exécuter")
    parser.add_argument("--task", help="Tâche pour l'agent")
    parser.add_argument("--gate", choices=[g.value for g in ValidationGate],
                       help="Porte de validation à exécuter")
    parser.add_argument("--verbose", "-v", action="store_true", help="Mode verbeux")
    
    args = parser.parse_args()
    
    # Niveau de log
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Chemin du projet
    project_root = Path(args.project).resolve()
    if not project_root.exists():
        print(f"❌ Dossier projet non trouvé: {project_root}")
        return 1
    
    # Initialiser l'orchestrateur
    orchestrator = Web3PipelineOrchestrator(project_root)
    
    try:
        if args.mode == "watch":
            # Mode surveillance
            orchestrator.print_status()
            await orchestrator.watch_mode()
            
        elif args.mode == "validate":
            # Mode validation complète
            print("🔍 Validation complète du pipeline...")
            
            gates_to_run = [
                ValidationGate.REQUIREMENTS,
                ValidationGate.ARCHITECTURE,
                ValidationGate.SECURITY,
                ValidationGate.CODE_QUALITY
            ]
            
            all_passed = True
            for gate in gates_to_run:
                result = await orchestrator.run_validation_gate(gate)
                
                icon = "✅" if result.get("passed", False) else "❌"
                print(f"{icon} {gate.value.replace('_', ' ').title():20} ", end="")
                
                if not result.get("passed", False):
                    all_passed = False
                    if "error" in result:
                        print(f"- {result['error']}")
                    elif "missing_files" in result:
                        print(f"- Fichiers manquants: {len(result['missing_files'])}")
                else:
                    print(f"- OK")
            
            if all_passed:
                print("\n🎉 Toutes les validations sont passées!")
            else:
                print("\n⚠️  Certaines validations ont échoué")
            
        elif args.phase:
            # Exécuter une phase spécifique
            phase = PipelinePhase(args.phase)
            result = await orchestrator.run_pipeline_phase(phase)
            
            if result.get("success", False):
                print(f"✅ Phase {phase.value} terminée avec succès")
            else:
                print(f"❌ Phase {phase.value} a échoué")
                if "error" in result:
                    print(f"   Erreur: {result['error']}")
        
        elif args.agent:
            # Exécuter un agent spécifique
            if args.task:
                result = await orchestrator.run_agent(args.agent, args.task)
                
                if result.get("success", False):
                    print(f"✅ Agent {args.agent} exécuté avec succès")
                else:
                    print(f"❌ Agent {args.agent} a échoué")
                    if "error" in result:
                        print(f"   Erreur: {result['error']}")
            else:
                print(f"❌ Spécifiez une tâche avec --task")
        
        elif args.gate:
            # Exécuter une porte de validation
            gate = ValidationGate(args.gate)
            result = await orchestrator.run_validation_gate(gate)
            
            icon = "✅" if result.get("passed", False) else "❌"
            print(f"{icon} {gate.value.replace('_', ' ').title()}")
            print(f"   Passed: {result.get('passed', False)}")
            
            if "error" in result:
                print(f"   Error: {result['error']}")
        
        else:
            # Mode par défaut: afficher le statut
            orchestrator.print_status()
        
        return 0
        
    except KeyboardInterrupt:
        print("\n👋 Pipeline arrêté par l'utilisateur")
        return 0
    except Exception as e:
        print(f"❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(asyncio.run(main()))