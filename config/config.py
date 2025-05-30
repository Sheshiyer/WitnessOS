"""
WitnessOS Environment Configuration

This module handles environment variable loading and configuration management
following best practices for security and maintainability.
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any
import logging

# Try to import python-dotenv, fall back to manual loading if not available
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

logger = logging.getLogger(__name__)

class WitnessOSConfig:
    """
    WitnessOS Configuration Manager
    
    Handles environment variable loading with proper precedence:
    1. System environment variables (highest priority)
    2. .env.local (local development)
    3. .env (shared development)
    4. .env.template (fallback defaults)
    """
    
    def __init__(self, base_dir: Optional[Path] = None):
        """
        Initialize configuration manager
        
        Args:
            base_dir: Base directory for .env files (defaults to current file's directory)
        """
        self.base_dir = base_dir or Path(__file__).parent
        self.config: Dict[str, Any] = {}
        self.load_environment()
    
    def load_environment(self):
        """Load environment variables with proper precedence"""
        
        # Define .env file precedence (first found wins for each variable)
        env_files = [
            self.base_dir / ".env.local",    # Local development (highest priority)
            self.base_dir / ".env",          # Shared development
            self.base_dir / ".env.template"  # Template/defaults
        ]
        
        if DOTENV_AVAILABLE:
            # Use python-dotenv for proper loading
            for env_file in env_files:
                if env_file.exists():
                    load_dotenv(env_file, override=False)  # Don't override existing vars
                    logger.info(f"Loaded environment from: {env_file}")
        else:
            # Fallback to manual loading
            logger.warning("python-dotenv not available, using manual .env loading")
            self._manual_load_env_files(env_files)
        
        # Load configuration values
        self._load_config_values()
    
    def _manual_load_env_files(self, env_files: list):
        """Manually load .env files when python-dotenv is not available"""
        loaded_vars = set()
        
        for env_file in env_files:
            if env_file.exists():
                with open(env_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip()
                            
                            # Only set if not already loaded (precedence)
                            if key not in loaded_vars and key not in os.environ:
                                os.environ[key] = value
                                loaded_vars.add(key)
                
                logger.info(f"Manually loaded environment from: {env_file}")
    
    def _load_config_values(self):
        """Load and validate configuration values"""
        
        # OpenRouter Configuration
        self.config['openrouter_api_key'] = os.getenv('OPENROUTER_API_KEY')
        
        # WitnessOS API Configuration
        self.config['production_api_url'] = os.getenv('WITNESSOS_PRODUCTION_API_URL', 'http://localhost:8002')
        self.config['api_keys'] = self._parse_api_keys(os.getenv('WITNESSOS_API_KEYS'))
        
        # Agent API Configuration
        self.config['agent_host'] = os.getenv('AGENT_API_HOST', '0.0.0.0')
        self.config['agent_port'] = int(os.getenv('AGENT_API_PORT', '8003'))
        
        # Logging Configuration
        self.config['log_level'] = os.getenv('LOG_LEVEL', 'INFO').upper()
        
        # Model Configuration
        self.config['default_model_type'] = os.getenv('DEFAULT_MODEL_TYPE', 'balanced')
        
        # Development Configuration
        self.config['dev_mode'] = os.getenv('DEV_MODE', 'false').lower() == 'true'
        
        # Database Configuration (optional)
        self.config['database_url'] = os.getenv('DATABASE_URL')
    
    def _parse_api_keys(self, api_keys_str: Optional[str]) -> Dict[str, str]:
        """Parse API keys from environment variable"""
        if not api_keys_str:
            return {}
        
        api_keys = {}
        for pair in api_keys_str.split(','):
            if ':' in pair:
                key, user = pair.split(':', 1)
                api_keys[key.strip()] = user.strip()
        
        return api_keys
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    def is_openrouter_configured(self) -> bool:
        """Check if OpenRouter API key is properly configured"""
        api_key = self.config.get('openrouter_api_key')
        return bool(api_key and api_key != 'your_openrouter_api_key_here')
    
    def validate_configuration(self) -> Dict[str, Any]:
        """Validate configuration and return status"""
        status = {
            'valid': True,
            'issues': [],
            'warnings': []
        }
        
        # Check OpenRouter API key
        if not self.is_openrouter_configured():
            status['issues'].append('OpenRouter API key not configured')
            status['valid'] = False
        
        # Check required dependencies
        try:
            import fastapi
            import uvicorn
            import httpx
        except ImportError as e:
            status['issues'].append(f'Missing required dependency: {e}')
            status['valid'] = False
        
        # Check if python-dotenv is available
        if not DOTENV_AVAILABLE:
            status['warnings'].append('python-dotenv not installed - using manual .env loading')
        
        return status
    
    def get_env_file_status(self) -> Dict[str, bool]:
        """Get status of .env files"""
        return {
            '.env.local': (self.base_dir / '.env.local').exists(),
            '.env': (self.base_dir / '.env').exists(),
            '.env.template': (self.base_dir / '.env.template').exists()
        }

# Global configuration instance
config = WitnessOSConfig()

# Convenience functions for backward compatibility
def get_openrouter_api_key() -> Optional[str]:
    """Get OpenRouter API key"""
    return config.get('openrouter_api_key')

def get_production_api_url() -> str:
    """Get Production API URL"""
    return config.get('production_api_url')

def is_openrouter_configured() -> bool:
    """Check if OpenRouter is configured"""
    return config.is_openrouter_configured()

def validate_environment() -> Dict[str, Any]:
    """Validate environment configuration"""
    return config.validate_configuration()

def get_config() -> WitnessOSConfig:
    """Get the global configuration instance"""
    return config
