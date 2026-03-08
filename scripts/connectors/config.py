"""
Connector configuration management module.

Provides unified configuration interface for all connectors,
including validation, serialization, and environment variable support.

Implements TASK-C1: Connector Framework Refactoring
"""

import os
import json
from typing import Dict, Any, Optional, Type, TypeVar, get_type_hints
from dataclasses import dataclass, field, asdict, fields
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T', bound='BaseConnectorConfig')


@dataclass
class RetryConfig:
    """Configuration for retry behavior.
    
    Attributes:
        max_retries: Maximum number of retry attempts (default: 3)
        retry_delay: Initial delay between retries in seconds (default: 1.0)
        exponential_backoff: Whether to use exponential backoff (default: True)
        max_delay: Maximum delay between retries in seconds (default: 30.0)
        retry_exceptions: List of exception type names to retry on
    """
    
    max_retries: int = 3
    retry_delay: float = 1.0
    exponential_backoff: bool = True
    max_delay: float = 30.0
    retry_exceptions: list = field(default_factory=lambda: ['ConnectionError', 'TimeoutError'])
    
    def get_exception_types(self) -> tuple:
        """Get exception types from string names.
        
        Returns:
            Tuple of exception classes
        """
        exception_map = {
            'ConnectionError': ConnectionError,
            'TimeoutError': TimeoutError,
            'Exception': Exception,
        }
        
        exceptions = []
        for name in self.retry_exceptions:
            if name in exception_map:
                exceptions.append(exception_map[name])
        
        return tuple(exceptions) if exceptions else (ConnectionError, TimeoutError)
    
    def get_delay(self, attempt: int) -> float:
        """Calculate delay for a given retry attempt.
        
        Args:
            attempt: Current attempt number (0-indexed)
            
        Returns:
            Delay in seconds
        """
        if not self.exponential_backoff:
            return self.retry_delay
        
        delay = self.retry_delay * (2 ** attempt)
        return min(delay, self.max_delay)


@dataclass
class ConnectionPoolConfig:
    """Configuration for connection pooling.
    
    Attributes:
        enabled: Whether to enable connection pooling (default: False)
        max_connections: Maximum number of connections in pool (default: 10)
        min_connections: Minimum number of idle connections (default: 1)
        idle_timeout: Seconds before idle connections are closed (default: 300)
        connection_timeout: Seconds to wait for a connection from pool (default: 30)
    """
    
    enabled: bool = False
    max_connections: int = 10
    min_connections: int = 1
    idle_timeout: float = 300.0
    connection_timeout: float = 30.0


@dataclass
class BaseConnectorConfig:
    """Base configuration for all connectors.
    
    Provides common configuration options and validation.
    All connector-specific configurations should inherit from this class.
    
    Attributes:
        timeout: Connection timeout in seconds (default: 30)
        verify_ssl: Whether to verify SSL certificates (default: True)
        use_tls: Whether to use TLS encryption (default: True)
        retry: Retry configuration
        pool: Connection pool configuration
        metadata: Additional metadata for the connector
    """
    
    timeout: int = 30
    verify_ssl: bool = True
    use_tls: bool = True
    
    retry: RetryConfig = field(default_factory=RetryConfig)
    pool: ConnectionPoolConfig = field(default_factory=ConnectionPoolConfig)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def validate(self) -> bool:
        """Validate the configuration.
        
        Returns:
            True if configuration is valid
            
        Raises:
            ValueError: If configuration is invalid
        """
        if self.timeout <= 0:
            raise ValueError("timeout must be positive")
        
        if self.retry.max_retries < 0:
            raise ValueError("max_retries cannot be negative")
        
        if self.retry.retry_delay <= 0:
            raise ValueError("retry_delay must be positive")
        
        if self.pool.enabled:
            if self.pool.max_connections <= 0:
                raise ValueError("max_connections must be positive")
            if self.pool.min_connections < 0:
                raise ValueError("min_connections cannot be negative")
            if self.pool.min_connections > self.pool.max_connections:
                raise ValueError("min_connections cannot exceed max_connections")
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary.
        
        Returns:
            Dictionary representation of the configuration
        """
        result = asdict(self)
        # Convert nested dataclasses
        if 'retry' in result and isinstance(result['retry'], dict):
            pass  # Already a dict from asdict
        return result
    
    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """Create configuration from dictionary.
        
        Args:
            data: Dictionary with configuration values
            
        Returns:
            Configuration instance
        """
        # Handle nested dataclasses
        if 'retry' in data and isinstance(data['retry'], dict):
            data['retry'] = RetryConfig(**data['retry'])
        if 'pool' in data and isinstance(data['pool'], dict):
            data['pool'] = ConnectionPoolConfig(**data['pool'])
        
        # Filter out unknown fields
        valid_fields = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        
        return cls(**filtered_data)
    
    def to_json(self) -> str:
        """Serialize configuration to JSON string.
        
        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_json(cls: Type[T], json_str: str) -> T:
        """Create configuration from JSON string.
        
        Args:
            json_str: JSON string with configuration values
            
        Returns:
            Configuration instance
        """
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def save_to_file(self, filepath: Path) -> None:
        """Save configuration to a JSON file.
        
        Args:
            filepath: Path to the configuration file
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.to_json())
        
        logger.info(f"Configuration saved to {filepath}")
    
    @classmethod
    def load_from_file(cls: Type[T], filepath: Path) -> T:
        """Load configuration from a JSON file.
        
        Args:
            filepath: Path to the configuration file
            
        Returns:
            Configuration instance
        """
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"Configuration file not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return cls.from_json(f.read())
    
    @classmethod
    def from_env(cls: Type[T], prefix: str = "CONNECTOR_") -> T:
        """Create configuration from environment variables.
        
        Environment variables should be in format: PREFIX_FIELD_NAME
        For nested fields: PREFIX_RETRY_MAX_RETRIES
        
        Args:
            prefix: Environment variable prefix
            
        Returns:
            Configuration instance
        """
        data: Dict[str, Any] = {}
        
        # Get type hints for the class
        type_hints = get_type_hints(cls)
        
        for f in fields(cls):
            env_name = f"{prefix}{f.name.upper()}"
            env_value = os.environ.get(env_name)
            
            if env_value is not None:
                # Convert based on type
                field_type = type_hints.get(f.name, str)
                
                if field_type == bool:
                    data[f.name] = env_value.lower() in ('true', '1', 'yes')
                elif field_type == int:
                    data[f.name] = int(env_value)
                elif field_type == float:
                    data[f.name] = float(env_value)
                else:
                    data[f.name] = env_value
        
        # Handle nested retry config
        retry_data = {}
        retry_prefix = f"{prefix}RETRY_"
        for key, value in os.environ.items():
            if key.startswith(retry_prefix):
                field_name = key[len(retry_prefix):].lower()
                retry_data[field_name] = value
        
        if retry_data:
            # Convert types
            if 'max_retries' in retry_data:
                retry_data['max_retries'] = int(retry_data['max_retries'])
            if 'retry_delay' in retry_data:
                retry_data['retry_delay'] = float(retry_data['retry_delay'])
            if 'max_delay' in retry_data:
                retry_data['max_delay'] = float(retry_data['max_delay'])
            if 'exponential_backoff' in retry_data:
                retry_data['exponential_backoff'] = retry_data['exponential_backoff'].lower() in ('true', '1', 'yes')
            data['retry'] = RetryConfig(**retry_data)
        
        # Handle nested pool config
        pool_data = {}
        pool_prefix = f"{prefix}POOL_"
        for key, value in os.environ.items():
            if key.startswith(pool_prefix):
                field_name = key[len(pool_prefix):].lower()
                pool_data[field_name] = value
        
        if pool_data:
            # Convert types
            if 'enabled' in pool_data:
                pool_data['enabled'] = pool_data['enabled'].lower() in ('true', '1', 'yes')
            if 'max_connections' in pool_data:
                pool_data['max_connections'] = int(pool_data['max_connections'])
            if 'min_connections' in pool_data:
                pool_data['min_connections'] = int(pool_data['min_connections'])
            if 'idle_timeout' in pool_data:
                pool_data['idle_timeout'] = float(pool_data['idle_timeout'])
            if 'connection_timeout' in pool_data:
                pool_data['connection_timeout'] = float(pool_data['connection_timeout'])
            data['pool'] = ConnectionPoolConfig(**pool_data)
        
        return cls.from_dict(data)


class ConfigManager:
    """Manager for connector configurations.
    
    Provides centralized configuration management with caching,
    validation, and environment variable support.
    
    Example:
        >>> manager = ConfigManager()
        >>> manager.register_config('email', EmailConfig)
        >>> config = manager.get_config('email', config_file='email.json')
    """
    
    _instance: Optional['ConfigManager'] = None
    
    def __new__(cls) -> 'ConfigManager':
        """Singleton pattern for configuration manager."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the configuration manager."""
        if self._initialized:
            return
        
        self._initialized = True
        self._config_classes: Dict[str, Type[BaseConnectorConfig]] = {}
        self._configs: Dict[str, BaseConnectorConfig] = {}
        self._config_paths: Dict[str, Path] = {}
    
    def register_config(
        self,
        name: str,
        config_class: Type[BaseConnectorConfig]
    ) -> None:
        """Register a configuration class.
        
        Args:
            name: Unique name for the configuration
            config_class: Configuration class (must inherit from BaseConnectorConfig)
        """
        if not issubclass(config_class, BaseConnectorConfig):
            raise ValueError(
                f"config_class must inherit from BaseConnectorConfig"
            )
        
        self._config_classes[name] = config_class
        logger.debug(f"Registered config class: {name}")
    
    def get_config(
        self,
        name: str,
        config_file: Optional[Path] = None,
        env_prefix: Optional[str] = None,
        **overrides
    ) -> BaseConnectorConfig:
        """Get a configuration instance.
        
        Configuration is loaded in the following order (later overrides earlier):
        1. Default values
        2. Configuration file (if provided)
        3. Environment variables (if env_prefix provided)
        4. Override arguments
        
        Args:
            name: Registered configuration name
            config_file: Path to configuration file
            env_prefix: Environment variable prefix
            **overrides: Additional override values
            
        Returns:
            Configuration instance
        """
        if name not in self._config_classes:
            raise ValueError(f"Unknown config: {name}. Did you forget to register it?")
        
        config_class = self._config_classes[name]
        
        # Check cache
        cache_key = f"{name}_{config_file}_{env_prefix}"
        if cache_key in self._configs and not overrides:
            return self._configs[cache_key]
        
        # Start with defaults
        config = config_class()
        
        # Load from file
        if config_file:
            try:
                file_config = config_class.load_from_file(config_file)
                config = config_class.from_dict({
                    **config.to_dict(),
                    **file_config.to_dict()
                })
            except FileNotFoundError:
                logger.warning(f"Config file not found: {config_file}, using defaults")
        
        # Load from environment
        if env_prefix:
            env_config = config_class.from_env(env_prefix)
            config = config_class.from_dict({
                **config.to_dict(),
                **env_config.to_dict()
            })
        
        # Apply overrides
        if overrides:
            config = config_class.from_dict({
                **config.to_dict(),
                **overrides
            })
        
        # Validate
        config.validate()
        
        # Cache
        if not overrides:
            self._configs[cache_key] = config
        
        return config
    
    def save_config(
        self,
        name: str,
        config: BaseConnectorConfig,
        filepath: Path
    ) -> None:
        """Save a configuration to file.
        
        Args:
            name: Configuration name
            config: Configuration instance
            filepath: Path to save the configuration
        """
        config.save_to_file(filepath)
        self._config_paths[name] = filepath
        logger.info(f"Saved config '{name}' to {filepath}")
    
    def list_configs(self) -> list:
        """List all registered configuration names.
        
        Returns:
            List of configuration names
        """
        return list(self._config_classes.keys())
    
    def clear_cache(self) -> None:
        """Clear the configuration cache."""
        self._configs.clear()
        logger.debug("Configuration cache cleared")


# Global config manager instance
config_manager = ConfigManager()


# Alias for backward compatibility
ConnectorConfig = BaseConnectorConfig
