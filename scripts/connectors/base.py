"""
Base connector abstract class for external data sources.

Defines the interface that all connectors must implement.
Includes retry logic, health checks, and connection management.

Implements TASK-C1: Connector Framework Refactoring
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Callable, TypeVar, Union
from dataclasses import dataclass
from datetime import datetime
from functools import wraps
import time
import logging
import threading

from .config import BaseConnectorConfig, RetryConfig, ConnectionPoolConfig

logger = logging.getLogger(__name__)

T = TypeVar('T')
F = TypeVar('F', bound=Callable)


# Re-export config classes for backward compatibility
# Use BaseConnectorConfig from config.py instead
ConnectorConfig = BaseConnectorConfig


def with_retry(
    max_retries: Optional[int] = None,
    retry_delay: Optional[float] = None,
    exponential_backoff: Optional[bool] = None,
    exceptions: tuple = (ConnectionError, TimeoutError)
):
    """Decorator for adding retry logic to methods.
    
    Args:
        max_retries: Maximum retry attempts (uses config if None)
        retry_delay: Initial delay between retries (uses config if None)
        exponential_backoff: Whether to use exponential backoff
        exceptions: Exception types to retry on
        
    Returns:
        Decorated function with retry logic
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Get retry config from connector
            config = getattr(self, 'config', None)
            
            retries = max_retries
            delay = retry_delay
            use_exponential_backoff = exponential_backoff
            
            if config and hasattr(config, 'retry'):
                if retries is None:
                    retries = config.retry.max_retries
                if delay is None:
                    delay = config.retry.retry_delay
                if use_exponential_backoff is None:
                    use_exponential_backoff = config.retry.exponential_backoff
            
            # Set defaults
            if retries is None:
                retries = 3
            if delay is None:
                delay = 1.0
            if use_exponential_backoff is None:
                use_exponential_backoff = True
            
            last_exception: Optional[Exception] = None
            
            for attempt in range(retries + 1):
                try:
                    return func(self, *args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < retries:
                        current_delay = delay * (2 ** attempt) if use_exponential_backoff else delay
                        logger.warning(
                            f"Retry {attempt + 1}/{retries} for {func.__name__}: {e}. "
                            f"Waiting {current_delay:.1f}s..."
                        )
                        time.sleep(current_delay)
                    else:
                        logger.error(
                            f"All {retries + 1} attempts failed for {func.__name__}: {e}"
                        )
            
            # Raise the last exception - at this point last_exception is guaranteed to be set
            if last_exception:
                raise last_exception
            raise ConnectionError("Retry failed with unknown error")
        
        return wrapper
    
    return decorator


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
    
    Features:
    - Automatic retry with exponential backoff
    - Health check mechanism
    - Connection state management
    - Context manager support
    
    Attributes:
        config: Connector configuration
        _connected: Internal connection state flag
        _connection_time: Timestamp when connection was established
    
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
    
    def __init__(self, config: Optional[BaseConnectorConfig] = None):
        """
        Initialize the connector.
        
        Args:
            config: Optional configuration object. If None, uses defaults.
        """
        self.config = config or BaseConnectorConfig()
        self._connected = False
        self._last_error: Optional[str] = None
        self._connection_time: Optional[datetime] = None
        self._last_activity_time: Optional[datetime] = None
        self._lock = threading.Lock()
    
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
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check on the connector.
        
        Returns:
            Dict containing health check results:
                - 'healthy': bool - overall health status
                - 'connected': bool - connection status
                - 'connection_time': datetime or None - when connected
                - 'idle_time': float or None - seconds since last activity
                - 'last_error': str or None - last error message
                
        Example:
            >>> health = connector.health_check()
            >>> if not health['healthy']:
            ...     print(f"Connector unhealthy: {health['last_error']}")
        """
        result = {
            'healthy': True,
            'connected': self._connected,
            'connection_time': self._connection_time,
            'idle_time': None,
            'last_error': self._last_error
        }
        
        if not self._connected:
            result['healthy'] = False
            return result
        
        # Calculate idle time
        if self._last_activity_time:
            idle_seconds = (datetime.now() - self._last_activity_time).total_seconds()
            result['idle_time'] = idle_seconds
            
            # Check if connection has been idle too long
            if hasattr(self.config, 'pool') and self.config.pool.enabled:
                if idle_seconds > self.config.pool.idle_timeout:
                    result['healthy'] = False
                    result['warning'] = 'Connection idle for too long'
        
        # Try a lightweight operation to verify connection
        try:
            if not self.is_connected():
                result['healthy'] = False
                result['warning'] = 'Connection check failed'
        except Exception as e:
            result['healthy'] = False
            result['warning'] = str(e)
        
        return result
    
    def reconnect(self) -> bool:
        """
        Attempt to reconnect to the data source.
        
        Returns:
            bool: True if reconnection successful
            
        Example:
            >>> if not connector.is_connected():
            ...     connector.reconnect()
        """
        with self._lock:
            if self._connected:
                try:
                    self.disconnect()
                except Exception as e:
                    logger.warning(f"Error during disconnect: {e}")
            
            return self.connect()
    
    def get_connection_duration(self) -> Optional[float]:
        """
        Get the duration of the current connection in seconds.
        
        Returns:
            float: Duration in seconds, or None if not connected
        """
        if not self._connected or not self._connection_time:
            return None
        
        return (datetime.now() - self._connection_time).total_seconds()
    
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
    
    def _update_activity_time(self) -> None:
        """Update the last activity timestamp."""
        self._last_activity_time = datetime.now()
    
    def _on_connect_success(self) -> None:
        """Called when connection is successful."""
        self._connected = True
        self._connection_time = datetime.now()
        self._last_activity_time = datetime.now()
        self._clear_error()
    
    def _on_disconnect(self) -> None:
        """Called when disconnected."""
        self._connected = False
        self._connection_time = None
        self._last_activity_time = None
    
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
        duration = ""
        if self._connected and self._connection_time:
            duration = f", duration={self.get_connection_duration():.1f}s"
        return f"{self.__class__.__name__}({status}{duration})"
