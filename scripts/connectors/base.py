"""
Base connector abstract class for external data sources.

Defines the interface that all connectors must implement.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class ConnectorConfig:
    """Base configuration for connectors."""
    
    # Connection settings
    timeout: int = 30
    retry_count: int = 3
    retry_delay: float = 1.0
    
    # Security settings
    verify_ssl: bool = True
    use_tls: bool = True


@dataclass
class SearchResult:
    """Standard search result from any connector."""
    
    id: str                           # Unique identifier
    title: str                        # Result title/subject
    snippet: str                      # Brief content preview
    source: str                       # Source identifier (e.g., 'email', 'database')
    metadata: Dict[str, Any]          # Additional metadata
    timestamp: Optional[datetime] = None  # Creation/modification time
    score: Optional[float] = None     # Relevance score (if applicable)


class BaseConnector(ABC):
    """
    Abstract base class for all data source connectors.
    
    All connectors must implement the following methods:
    - connect(): Establish connection to the data source
    - disconnect(): Close the connection
    - is_connected(): Check if connection is active
    - search(): Search for data in the source
    
    The connector pattern ensures consistent API across different
    data sources (email, databases, APIs, etc.).
    
    Attributes:
        config: Connector configuration
        _connected: Internal connection state flag
    
    Example:
        >>> class MyConnector(BaseConnector):
        ...     def connect(self) -> bool:
        ...         # Implementation
        ...         pass
        ...
        >>> connector = MyConnector(config=ConnectorConfig())
        >>> if connector.connect():
        ...     results = connector.search("query")
        ...     connector.disconnect()
    """
    
    def __init__(self, config: Optional[ConnectorConfig] = None):
        """
        Initialize the connector.
        
        Args:
            config: Optional configuration object. If None, uses defaults.
        """
        self.config = config or ConnectorConfig()
        self._connected = False
        self._last_error: Optional[str] = None
    
    @abstractmethod
    def connect(self) -> bool:
        """
        Establish connection to the data source.
        
        This method should:
        1. Validate configuration
        2. Establish the connection
        3. Set _connected = True on success
        4. Set _last_error on failure
        
        Returns:
            bool: True if connection successful, False otherwise
        
        Raises:
            ConnectionError: If connection fails after all retries
        
        Example:
            >>> connector = EmailConnector(server="imap.gmail.com", ...)
            >>> success = connector.connect()
            >>> if not success:
            ...     print(connector.get_last_error())
        """
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        """
        Close the connection to the data source.
        
        This method should:
        1. Close any open connections
        2. Clean up resources
        3. Set _connected = False
        
        Returns:
            bool: True if disconnection successful, False otherwise
        
        Example:
            >>> connector.disconnect()
            True
        """
        pass
    
    @abstractmethod
    def is_connected(self) -> bool:
        """
        Check if the connection is currently active.
        
        Returns:
            bool: True if connected, False otherwise
        
        Example:
            >>> if connector.is_connected():
            ...     results = connector.search("query")
        """
        pass
    
    @abstractmethod
    def search(
        self,
        query: str,
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> List[SearchResult]:
        """
        Search for data in the connected source.
        
        Args:
            query: Search query string
            limit: Maximum number of results to return (default: 10)
            filters: Optional filters to narrow results
                Example: {'folder': 'INBOX', 'date_from': '2024-01-01'}
            **kwargs: Additional connector-specific parameters
        
        Returns:
            List of SearchResult objects matching the query
        
        Raises:
            ConnectionError: If not connected
            ValueError: If query is invalid
        
        Example:
            >>> results = connector.search("project budget", limit=5)
            >>> for result in results:
            ...     print(f"{result.title}: {result.snippet}")
        """
        pass
    
    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific item by its unique identifier.
        
        Args:
            id: Unique identifier of the item
        
        Returns:
            Dict containing the full item data, or None if not found
        
        Example:
            >>> email = connector.get_by_id("msg_123")
            >>> if email:
            ...     print(email['body'])
        """
        pass
    
    def get_last_error(self) -> Optional[str]:
        """
        Get the last error message.
        
        Returns:
            str or None: Last error message, or None if no error
        """
        return self._last_error
    
    def _set_error(self, message: str) -> None:
        """Set the last error message."""
        self._last_error = message
        logger.error(f"[{self.__class__.__name__}] {message}")
    
    def _clear_error(self) -> None:
        """Clear the last error message."""
        self._last_error = None
    
    def __enter__(self):
        """Context manager entry - connect automatically."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - disconnect automatically."""
        self.disconnect()
        return False
    
    def __repr__(self) -> str:
        """String representation of the connector."""
        status = "connected" if self._connected else "disconnected"
        return f"{self.__class__.__name__}({status})"
