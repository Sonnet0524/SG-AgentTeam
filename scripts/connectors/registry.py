"""
Connector registry module.

Provides plugin-style registration and discovery mechanism for connectors.
Allows dynamic registration and instantiation of connector classes.

Implements TASK-C1: Connector Framework Refactoring
"""

import importlib
import inspect
from typing import Dict, Type, Optional, List, Any, Callable
from dataclasses import dataclass
import logging
from pathlib import Path
import json

from .base import BaseConnector
from .config import BaseConnectorConfig, config_manager

logger = logging.getLogger(__name__)


@dataclass
class ConnectorInfo:
    """Information about a registered connector.
    
    Attributes:
        name: Unique connector name
        connector_class: The connector class
        config_class: Configuration class for the connector
        description: Human-readable description
        version: Connector version
        tags: List of tags for categorization
    """
    
    name: str
    connector_class: Type[BaseConnector]
    config_class: Optional[Type[BaseConnectorConfig]] = None
    description: str = ""
    version: str = "1.0.0"
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class ConnectorRegistry:
    """Registry for connector plugins.
    
    Provides a centralized registry for all connector implementations,
    enabling plugin-style architecture where new connectors can be
    added without modifying existing code.
    
    Features:
    - Register connectors with metadata
    - Discover connectors by name or tags
    - Create connector instances with configuration
    - Auto-discovery from packages
    
    Example:
        >>> registry = ConnectorRegistry()
        >>> 
        >>> # Register a connector
        >>> registry.register(
        ...     name='email',
        ...     connector_class=EmailConnector,
        ...     config_class=EmailConfig,
        ...     description='IMAP email connector'
        ... )
        >>> 
        >>> # Create an instance
        >>> connector = registry.create('email', config=my_config)
        >>> 
        >>> # List available connectors
        >>> for name, info in registry.list_connectors():
        ...     print(f"{name}: {info.description}")
    """
    
    _instance: Optional['ConnectorRegistry'] = None
    
    def __new__(cls) -> 'ConnectorRegistry':
        """Singleton pattern for registry."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the registry."""
        if self._initialized:
            return
        
        self._initialized = True
        self._connectors: Dict[str, ConnectorInfo] = {}
        self._factories: Dict[str, Callable] = {}
        self._aliases: Dict[str, str] = {}
    
    def register(
        self,
        name: str,
        connector_class: Type[BaseConnector],
        config_class: Optional[Type[BaseConnectorConfig]] = None,
        description: str = "",
        version: str = "1.0.0",
        tags: Optional[List[str]] = None,
        aliases: Optional[List[str]] = None,
        factory: Optional[Callable] = None
    ) -> None:
        """Register a connector class.
        
        Args:
            name: Unique name for the connector
            connector_class: The connector class (must inherit from BaseConnector)
            config_class: Configuration class for the connector
            description: Human-readable description
            version: Connector version string
            tags: List of tags for categorization
            aliases: Alternative names for the connector
            factory: Optional factory function for creating instances
            
        Raises:
            ValueError: If name is already registered or class is invalid
        """
        # Validate
        if name in self._connectors:
            raise ValueError(f"Connector '{name}' is already registered")
        
        if not inspect.isclass(connector_class):
            raise ValueError("connector_class must be a class")
        
        if not issubclass(connector_class, BaseConnector):
            raise ValueError(
                "connector_class must inherit from BaseConnector"
            )
        
        # Register in config manager if config class provided
        if config_class is not None:
            config_manager.register_config(name, config_class)
        
        # Store connector info
        self._connectors[name] = ConnectorInfo(
            name=name,
            connector_class=connector_class,
            config_class=config_class,
            description=description,
            version=version,
            tags=tags or []
        )
        
        # Store factory if provided
        if factory is not None:
            self._factories[name] = factory
        
        # Register aliases
        if aliases:
            for alias in aliases:
                if alias in self._aliases:
                    logger.warning(f"Alias '{alias}' already registered, overwriting")
                self._aliases[alias] = name
        
        logger.info(
            f"Registered connector: {name} v{version} - {description}"
        )
    
    def unregister(self, name: str) -> bool:
        """Unregister a connector.
        
        Args:
            name: Connector name to unregister
            
        Returns:
            True if connector was unregistered, False if not found
        """
        if name not in self._connectors:
            return False
        
        del self._connectors[name]
        
        if name in self._factories:
            del self._factories[name]
        
        # Remove aliases pointing to this connector
        self._aliases = {
            k: v for k, v in self._aliases.items() if v != name
        }
        
        logger.info(f"Unregistered connector: {name}")
        return True
    
    def get(self, name: str) -> Optional[ConnectorInfo]:
        """Get connector information by name.
        
        Args:
            name: Connector name or alias
            
        Returns:
            ConnectorInfo if found, None otherwise
        """
        # Check aliases
        resolved_name = self._aliases.get(name, name)
        return self._connectors.get(resolved_name)
    
    def create(
        self,
        name: str,
        config: Optional[BaseConnectorConfig] = None,
        **kwargs
    ) -> BaseConnector:
        """Create a connector instance.
        
        Args:
            name: Connector name or alias
            config: Configuration instance
            **kwargs: Additional arguments passed to connector constructor
            
        Returns:
            Connector instance
            
        Raises:
            ValueError: If connector not found
        """
        info = self.get(name)
        
        if info is None:
            available = list(self._connectors.keys())
            raise ValueError(
                f"Connector '{name}' not found. Available: {available}"
            )
        
        # Use factory if available
        if info.name in self._factories:
            return self._factories[info.name](config=config, **kwargs)
        
        # Otherwise, instantiate directly
        if config is not None:
            return info.connector_class(config=config, **kwargs)
        else:
            return info.connector_class(**kwargs)
    
    def list_connectors(self) -> List[tuple]:
        """List all registered connectors.
        
        Returns:
            List of (name, ConnectorInfo) tuples
        """
        return list(self._connectors.items())
    
    def get_by_tag(self, tag: str) -> List[ConnectorInfo]:
        """Get connectors by tag.
        
        Args:
            tag: Tag to search for
            
        Returns:
            List of matching ConnectorInfo objects
        """
        return [
            info for info in self._connectors.values()
            if tag in info.tags
        ]
    
    def get_names(self) -> List[str]:
        """Get all registered connector names.
        
        Returns:
            List of connector names
        """
        return list(self._connectors.keys())
    
    def exists(self, name: str) -> bool:
        """Check if a connector is registered.
        
        Args:
            name: Connector name or alias
            
        Returns:
            True if connector exists
        """
        return self.get(name) is not None
    
    def discover_and_register(
        self,
        package_name: str,
        module_name: str = None
    ) -> int:
        """Auto-discover and register connectors from a package.
        
        Scans a package for connector classes and registers them.
        Connector classes should have a CONNECTOR_INFO class attribute
        with registration metadata.
        
        Expected CONNECTOR_INFO format:
            CONNECTOR_INFO = {
                'name': 'my_connector',
                'description': 'My connector description',
                'version': '1.0.0',
                'tags': ['email', 'custom'],
                'config_class': MyConfig
            }
        
        Args:
            package_name: Package name to scan
            module_name: Specific module to scan (optional)
            
        Returns:
            Number of connectors registered
        """
        count = 0
        
        try:
            if module_name:
                module = importlib.import_module(f"{package_name}.{module_name}")
                modules = [module]
            else:
                package = importlib.import_module(package_name)
                modules = [package]
                
                # Try to import all submodules
                if hasattr(package, '__path__'):
                    for path in package.__path__:
                        for file in Path(path).glob("*.py"):
                            if file.name.startswith("_"):
                                continue
                            
                            submodule_name = f"{package_name}.{file.stem}"
                            try:
                                submodule = importlib.import_module(submodule_name)
                                modules.append(submodule)
                            except ImportError as e:
                                logger.debug(
                                    f"Could not import {submodule_name}: {e}"
                                )
            
            # Scan modules for connector classes
            for module in modules:
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    # Skip imported classes
                    if obj.__module__ != module.__name__:
                        continue
                    
                    # Check if it's a connector
                    if not issubclass(obj, BaseConnector):
                        continue
                    
                    if obj is BaseConnector:
                        continue
                    
                    # Check for CONNECTOR_INFO
                    if hasattr(obj, 'CONNECTOR_INFO'):
                        info = obj.CONNECTOR_INFO
                        try:
                            self.register(
                                name=info.get('name', name.lower()),
                                connector_class=obj,
                                config_class=info.get('config_class'),
                                description=info.get('description', ''),
                                version=info.get('version', '1.0.0'),
                                tags=info.get('tags', []),
                                aliases=info.get('aliases', [])
                            )
                            count += 1
                        except ValueError as e:
                            logger.warning(
                                f"Could not register connector {name}: {e}"
                            )
                    else:
                        # Auto-register with defaults
                        try:
                            self.register(
                                name=name.lower(),
                                connector_class=obj,
                                description=f"Auto-discovered connector: {name}"
                            )
                            count += 1
                        except ValueError:
                            # Already registered
                            pass
                            
        except ImportError as e:
            logger.error(f"Could not import package {package_name}: {e}")
        
        return count
    
    def to_json(self) -> str:
        """Export registry information to JSON.
        
        Returns:
            JSON string with connector information
        """
        data = {
            name: {
                'description': info.description,
                'version': info.version,
                'tags': info.tags,
                'has_config': info.config_class is not None
            }
            for name, info in self._connectors.items()
        }
        return json.dumps(data, indent=2)


def connector(
    name: str = None,
    description: str = "",
    version: str = "1.0.0",
    tags: List[str] = None,
    aliases: List[str] = None,
    config_class: Type[BaseConnectorConfig] = None
):
    """Decorator for registering connector classes.
    
    Example:
        >>> @connector(
        ...     name='my_connector',
        ...     description='My custom connector',
        ...     tags=['custom']
        ... )
        ... class MyConnector(BaseConnector):
        ...     pass
    
    Args:
        name: Connector name (defaults to class name lowercase)
        description: Human-readable description
        version: Connector version
        tags: List of tags
        aliases: Alternative names
        config_class: Configuration class
        
    Returns:
        Decorator function
    """
    def decorator(cls: Type[BaseConnector]) -> Type[BaseConnector]:
        # Get the global registry
        registry = ConnectorRegistry()
        
        # Determine name
        connector_name = name or cls.__name__.lower()
        
        # Register
        registry.register(
            name=connector_name,
            connector_class=cls,
            config_class=config_class,
            description=description,
            version=version,
            tags=tags,
            aliases=aliases
        )
        
        return cls
    
    return decorator


# Global registry instance
connector_registry = ConnectorRegistry()
