"""
Unit tests for connector framework components.

Tests for configuration management, registry, and base connector enhancements.

Implements TASK-C1: Connector Framework Refactoring
"""

import pytest
import json
import os
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile

from scripts.connectors.config import (
    BaseConnectorConfig,
    RetryConfig,
    ConnectionPoolConfig,
    ConfigManager,
    config_manager
)
from scripts.connectors.registry import (
    ConnectorRegistry,
    ConnectorInfo,
    connector_registry,
    connector
)
from scripts.connectors.base import (
    BaseConnector,
    SearchResult,
    with_retry
)


# ==================== Configuration Tests ====================

class TestRetryConfig:
    """Test cases for RetryConfig."""
    
    def test_default_values(self):
        """Test default configuration values."""
        config = RetryConfig()
        
        assert config.max_retries == 3
        assert config.retry_delay == 1.0
        assert config.exponential_backoff is True
        assert config.max_delay == 30.0
        assert 'ConnectionError' in config.retry_exceptions
        assert 'TimeoutError' in config.retry_exceptions
    
    def test_get_exception_types(self):
        """Test getting exception types from names."""
        config = RetryConfig()
        
        exceptions = config.get_exception_types()
        assert ConnectionError in exceptions
        assert TimeoutError in exceptions
    
    def test_custom_values(self):
        """Test custom configuration values."""
        config = RetryConfig(
            max_retries=5,
            retry_delay=2.0,
            exponential_backoff=False,
            max_delay=60.0
        )
        
        assert config.max_retries == 5
        assert config.retry_delay == 2.0
        assert config.exponential_backoff is False
        assert config.max_delay == 60.0
    
    def test_get_delay_linear(self):
        """Test delay calculation without exponential backoff."""
        config = RetryConfig(exponential_backoff=False, retry_delay=1.0)
        
        assert config.get_delay(0) == 1.0
        assert config.get_delay(1) == 1.0
        assert config.get_delay(2) == 1.0
    
    def test_get_delay_exponential(self):
        """Test delay calculation with exponential backoff."""
        config = RetryConfig(exponential_backoff=True, retry_delay=1.0, max_delay=30.0)
        
        assert config.get_delay(0) == 1.0
        assert config.get_delay(1) == 2.0
        assert config.get_delay(2) == 4.0
        assert config.get_delay(10) == 30.0  # Capped at max_delay


class TestConnectionPoolConfig:
    """Test cases for ConnectionPoolConfig."""
    
    def test_default_values(self):
        """Test default configuration values."""
        config = ConnectionPoolConfig()
        
        assert config.enabled is False
        assert config.max_connections == 10
        assert config.min_connections == 1
        assert config.idle_timeout == 300.0
        assert config.connection_timeout == 30.0
    
    def test_custom_values(self):
        """Test custom configuration values."""
        config = ConnectionPoolConfig(
            enabled=True,
            max_connections=20,
            min_connections=5,
            idle_timeout=600.0
        )
        
        assert config.enabled is True
        assert config.max_connections == 20
        assert config.min_connections == 5


class TestBaseConnectorConfig:
    """Test cases for BaseConnectorConfig."""
    
    def test_default_values(self):
        """Test default configuration values."""
        config = BaseConnectorConfig()
        
        assert config.timeout == 30
        assert config.verify_ssl is True
        assert config.use_tls is True
        assert isinstance(config.retry, RetryConfig)
        assert isinstance(config.pool, ConnectionPoolConfig)
    
    def test_validate_success(self):
        """Test successful validation."""
        config = BaseConnectorConfig(timeout=60)
        
        assert config.validate() is True
    
    def test_validate_invalid_timeout(self):
        """Test validation with invalid timeout."""
        config = BaseConnectorConfig(timeout=0)
        
        with pytest.raises(ValueError, match="timeout must be positive"):
            config.validate()
    
    def test_validate_invalid_retry(self):
        """Test validation with invalid retry config."""
        config = BaseConnectorConfig()
        config.retry.max_retries = -1
        
        with pytest.raises(ValueError, match="max_retries cannot be negative"):
            config.validate()
    
    def test_validate_invalid_pool(self):
        """Test validation with invalid pool config."""
        config = BaseConnectorConfig()
        config.pool.enabled = True
        config.pool.max_connections = 0
        
        with pytest.raises(ValueError, match="max_connections must be positive"):
            config.validate()
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        config = BaseConnectorConfig(timeout=60)
        data = config.to_dict()
        
        assert data['timeout'] == 60
        assert 'retry' in data
        assert 'pool' in data
    
    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {
            'timeout': 60,
            'retry': {'max_retries': 5, 'retry_delay': 2.0},
            'pool': {'enabled': True}
        }
        config = BaseConnectorConfig.from_dict(data)
        
        assert config.timeout == 60
        assert config.retry.max_retries == 5
        assert config.retry.retry_delay == 2.0
        assert config.pool.enabled is True
    
    def test_to_json_and_from_json(self):
        """Test JSON serialization and deserialization."""
        config = BaseConnectorConfig(timeout=60)
        json_str = config.to_json()
        
        assert isinstance(json_str, str)
        
        restored = BaseConnectorConfig.from_json(json_str)
        assert restored.timeout == 60
    
    def test_save_and_load_file(self):
        """Test saving and loading from file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "config.json"
            
            config = BaseConnectorConfig(timeout=60)
            config.save_to_file(filepath)
            
            assert filepath.exists()
            
            loaded = BaseConnectorConfig.load_from_file(filepath)
            assert loaded.timeout == 60
    
    def test_from_env(self, monkeypatch):
        """Test loading from environment variables."""
        monkeypatch.setenv('TEST_TIMEOUT', '120')
        monkeypatch.setenv('TEST_VERIFY_SSL', 'false')
        monkeypatch.setenv('TEST_RETRY_MAX_RETRIES', '5')
        
        config = BaseConnectorConfig.from_env(prefix='TEST_')
        
        assert config.timeout == 120
        assert config.verify_ssl is False
        assert config.retry.max_retries == 5


class TestConfigManager:
    """Test cases for ConfigManager."""
    
    def test_singleton(self):
        """Test that ConfigManager is a singleton."""
        manager1 = ConfigManager()
        manager2 = ConfigManager()
        
        assert manager1 is manager2
    
    def test_register_and_get(self):
        """Test registering and getting a config."""
        manager = ConfigManager()
        manager._configs.clear()  # Clear cache for clean test
        
        manager.register_config('test', BaseConnectorConfig)
        
        assert 'test' in manager.list_configs()
    
    def test_get_config(self):
        """Test getting a configuration instance."""
        manager = ConfigManager()
        manager._configs.clear()
        manager.register_config('test2', BaseConnectorConfig)
        
        config = manager.get_config('test2', timeout=90)
        
        assert config.timeout == 90
    
    def test_get_unknown_config(self):
        """Test getting an unknown config raises error."""
        manager = ConfigManager()
        
        with pytest.raises(ValueError, match="Unknown config"):
            manager.get_config('unknown')
    
    def test_clear_cache(self):
        """Test clearing the cache."""
        manager = ConfigManager()
        manager._configs['test_key'] = BaseConnectorConfig()
        
        manager.clear_cache()
        
        assert len(manager._configs) == 0


# ==================== Registry Tests ====================

class TestConnectorRegistry:
    """Test cases for ConnectorRegistry."""
    
    def test_singleton(self):
        """Test that registry is a singleton."""
        registry1 = ConnectorRegistry()
        registry2 = ConnectorRegistry()
        
        assert registry1 is registry2
    
    def test_register_connector(self):
        """Test registering a connector."""
        registry = ConnectorRegistry()
        
        # Create a mock connector class
        class MockConnector(BaseConnector):
            def connect(self): return True
            def disconnect(self): return True
            def is_connected(self): return False
            def search(self, query, limit=10, filters=None, **kwargs): return []
            def get_by_id(self, id): return None
        
        registry.register(
            name='test_connector',
            connector_class=MockConnector,
            description='Test connector'
        )
        
        assert registry.exists('test_connector')
        info = registry.get('test_connector')
        assert info.description == 'Test connector'
        
        # Cleanup
        registry.unregister('test_connector')
    
    def test_register_duplicate(self):
        """Test registering duplicate connector raises error."""
        registry = ConnectorRegistry()
        
        class MockConnector(BaseConnector):
            def connect(self): return True
            def disconnect(self): return True
            def is_connected(self): return False
            def search(self, query, limit=10, filters=None, **kwargs): return []
            def get_by_id(self, id): return None
        
        registry.register('dup_test', MockConnector)
        
        with pytest.raises(ValueError, match="already registered"):
            registry.register('dup_test', MockConnector)
        
        registry.unregister('dup_test')
    
    def test_register_invalid_class(self):
        """Test registering invalid class raises error."""
        registry = ConnectorRegistry()
        
        with pytest.raises(ValueError, match="must inherit from BaseConnector"):
            registry.register('invalid', str)
    
    def test_unregister(self):
        """Test unregistering a connector."""
        registry = ConnectorRegistry()
        
        class MockConnector(BaseConnector):
            def connect(self): return True
            def disconnect(self): return True
            def is_connected(self): return False
            def search(self, query, limit=10, filters=None, **kwargs): return []
            def get_by_id(self, id): return None
        
        registry.register('to_remove', MockConnector)
        assert registry.exists('to_remove')
        
        result = registry.unregister('to_remove')
        assert result is True
        assert not registry.exists('to_remove')
    
    def test_unregister_unknown(self):
        """Test unregistering unknown connector."""
        registry = ConnectorRegistry()
        
        result = registry.unregister('unknown_connector')
        assert result is False
    
    def test_create_connector(self):
        """Test creating a connector instance."""
        registry = ConnectorRegistry()
        
        class MockConnector(BaseConnector):
            def connect(self): return True
            def disconnect(self): return True
            def is_connected(self): return False
            def search(self, query, limit=10, filters=None, **kwargs): return []
            def get_by_id(self, id): return None
        
        registry.register('create_test', MockConnector)
        
        instance = registry.create('create_test')
        assert isinstance(instance, MockConnector)
        
        registry.unregister('create_test')
    
    def test_create_unknown_connector(self):
        """Test creating unknown connector raises error."""
        registry = ConnectorRegistry()
        
        with pytest.raises(ValueError, match="not found"):
            registry.create('unknown')
    
    def test_aliases(self):
        """Test connector aliases."""
        registry = ConnectorRegistry()
        
        class MockConnector(BaseConnector):
            def connect(self): return True
            def disconnect(self): return True
            def is_connected(self): return False
            def search(self, query, limit=10, filters=None, **kwargs): return []
            def get_by_id(self, id): return None
        
        registry.register(
            name='aliased_connector',
            connector_class=MockConnector,
            aliases=['alias1', 'alias2']
        )
        
        assert registry.exists('alias1')
        assert registry.exists('alias2')
        
        info = registry.get('alias1')
        assert info.name == 'aliased_connector'
        
        registry.unregister('aliased_connector')
    
    def test_list_connectors(self):
        """Test listing connectors."""
        registry = ConnectorRegistry()
        
        class MockConnector(BaseConnector):
            def connect(self): return True
            def disconnect(self): return True
            def is_connected(self): return False
            def search(self, query, limit=10, filters=None, **kwargs): return []
            def get_by_id(self, id): return None
        
        registry.register('list_test1', MockConnector)
        registry.register('list_test2', MockConnector)
        
        names = registry.get_names()
        assert 'list_test1' in names
        assert 'list_test2' in names
        
        registry.unregister('list_test1')
        registry.unregister('list_test2')
    
    def test_get_by_tag(self):
        """Test getting connectors by tag."""
        registry = ConnectorRegistry()
        
        class MockConnector(BaseConnector):
            def connect(self): return True
            def disconnect(self): return True
            def is_connected(self): return False
            def search(self, query, limit=10, filters=None, **kwargs): return []
            def get_by_id(self, id): return None
        
        registry.register('tag_test1', MockConnector, tags=['email', 'test'])
        registry.register('tag_test2', MockConnector, tags=['database'])
        registry.register('tag_test3', MockConnector, tags=['email', 'production'])
        
        email_connectors = registry.get_by_tag('email')
        assert len(email_connectors) == 2
        
        registry.unregister('tag_test1')
        registry.unregister('tag_test2')
        registry.unregister('tag_test3')
    
    def test_to_json(self):
        """Test exporting registry to JSON."""
        registry = ConnectorRegistry()
        
        class MockConnector(BaseConnector):
            def connect(self): return True
            def disconnect(self): return True
            def is_connected(self): return False
            def search(self, query, limit=10, filters=None, **kwargs): return []
            def get_by_id(self, id): return None
        
        registry.register('json_test', MockConnector, description='JSON test')
        
        json_str = registry.to_json()
        data = json.loads(json_str)
        
        assert 'json_test' in data
        assert data['json_test']['description'] == 'JSON test'
        
        registry.unregister('json_test')


class TestConnectorDecorator:
    """Test cases for @connector decorator."""
    
    def test_connector_decorator(self):
        """Test the @connector decorator."""
        registry = ConnectorRegistry()
        
        @connector(
            name='decorated_connector',
            description='A decorated connector',
            tags=['test']
        )
        class DecoratedConnector(BaseConnector):
            def connect(self): return True
            def disconnect(self): return True
            def is_connected(self): return False
            def search(self, query, limit=10, filters=None, **kwargs): return []
            def get_by_id(self, id): return None
        
        assert registry.exists('decorated_connector')
        
        info = registry.get('decorated_connector')
        assert info.description == 'A decorated connector'
        assert 'test' in info.tags
        
        registry.unregister('decorated_connector')


# ==================== Base Connector Tests ====================

class TestSearchResult:
    """Test cases for SearchResult."""
    
    def test_creation(self):
        """Test creating a search result."""
        result = SearchResult(
            id='test_1',
            title='Test Title',
            snippet='Test snippet',
            source='test',
            metadata={'key': 'value'}
        )
        
        assert result.id == 'test_1'
        assert result.title == 'Test Title'
        assert result.snippet == 'Test snippet'
        assert result.source == 'test'
        assert result.metadata == {'key': 'value'}
    
    def test_with_timestamp(self):
        """Test search result with timestamp."""
        now = datetime.now()
        result = SearchResult(
            id='test_2',
            title='Test',
            snippet='Content',
            source='test',
            metadata={},
            timestamp=now
        )
        
        assert result.timestamp == now


class TestWithRetryDecorator:
    """Test cases for with_retry decorator."""
    
    def test_retry_success_on_first_try(self):
        """Test successful call without retry."""
        class MockConnector(BaseConnector):
            def __init__(self):
                self.call_count = 0
                super().__init__()
            
            @with_retry(max_retries=3)
            def connect(self):
                self.call_count += 1
                self._on_connect_success()
                return True
            
            def disconnect(self): return True
            def is_connected(self): return self._connected
            def search(self, query, limit=10, filters=None, **kwargs): return []
            def get_by_id(self, id): return None
        
        connector = MockConnector()
        result = connector.connect()
        
        assert result is True
        assert connector.call_count == 1
    
    def test_retry_on_failure(self):
        """Test retry on failure."""
        class MockConnector(BaseConnector):
            def __init__(self):
                self.call_count = 0
                super().__init__()
            
            @with_retry(max_retries=2, retry_delay=0.1)
            def connect(self):
                self.call_count += 1
                if self.call_count < 3:
                    raise ConnectionError("Simulated failure")
                self._on_connect_success()
                return True
            
            def disconnect(self): return True
            def is_connected(self): return self._connected
            def search(self, query, limit=10, filters=None, **kwargs): return []
            def get_by_id(self, id): return None
        
        connector = MockConnector()
        result = connector.connect()
        
        assert result is True
        assert connector.call_count == 3
    
    def test_retry_exhausted(self):
        """Test retry exhausted."""
        class MockConnector(BaseConnector):
            def __init__(self):
                self.call_count = 0
                super().__init__()
            
            @with_retry(max_retries=2, retry_delay=0.1)
            def connect(self):
                self.call_count += 1
                raise ConnectionError("Persistent failure")
            
            def disconnect(self): return True
            def is_connected(self): return self._connected
            def search(self, query, limit=10, filters=None, **kwargs): return []
            def get_by_id(self, id): return None
        
        connector = MockConnector()
        
        with pytest.raises(ConnectionError, match="Persistent failure"):
            connector.connect()
        
        assert connector.call_count == 3  # Initial + 2 retries


class TestBaseConnectorEnhancements:
    """Test cases for BaseConnector enhancements."""
    
    def test_health_check_disconnected(self):
        """Test health check when disconnected."""
        class MockConnector(BaseConnector):
            def connect(self): return True
            def disconnect(self): return True
            def is_connected(self): return self._connected
            def search(self, query, limit=10, filters=None, **kwargs): return []
            def get_by_id(self, id): return None
        
        connector = MockConnector()
        health = connector.health_check()
        
        assert health['healthy'] is False
        assert health['connected'] is False
    
    def test_health_check_connected(self):
        """Test health check when connected."""
        class MockConnector(BaseConnector):
            def connect(self):
                self._on_connect_success()
                return True
            def disconnect(self):
                self._on_disconnect()
                return True
            def is_connected(self): return self._connected
            def search(self, query, limit=10, filters=None, **kwargs): return []
            def get_by_id(self, id): return None
        
        connector = MockConnector()
        connector.connect()
        health = connector.health_check()
        
        assert health['healthy'] is True
        assert health['connected'] is True
    
    def test_reconnect(self):
        """Test reconnection."""
        class MockConnector(BaseConnector):
            def __init__(self):
                self.connect_count = 0
                super().__init__()
            
            def connect(self):
                self.connect_count += 1
                self._on_connect_success()
                return True
            
            def disconnect(self):
                self._on_disconnect()
                return True
            
            def is_connected(self): return self._connected
            def search(self, query, limit=10, filters=None, **kwargs): return []
            def get_by_id(self, id): return None
        
        connector = MockConnector()
        connector.connect()
        assert connector.connect_count == 1
        
        connector.reconnect()
        assert connector.connect_count == 2
    
    def test_get_connection_duration(self):
        """Test getting connection duration."""
        class MockConnector(BaseConnector):
            def connect(self):
                self._on_connect_success()
                return True
            def disconnect(self):
                self._on_disconnect()
                return True
            def is_connected(self): return self._connected
            def search(self, query, limit=10, filters=None, **kwargs): return []
            def get_by_id(self, id): return None
        
        connector = MockConnector()
        
        # Not connected
        assert connector.get_connection_duration() is None
        
        # Connected
        connector.connect()
        duration = connector.get_connection_duration()
        assert duration is not None
        assert duration >= 0
    
    def test_repr(self):
        """Test string representation."""
        class MockConnector(BaseConnector):
            def connect(self):
                self._on_connect_success()
                return True
            def disconnect(self):
                self._on_disconnect()
                return True
            def is_connected(self): return self._connected
            def search(self, query, limit=10, filters=None, **kwargs): return []
            def get_by_id(self, id): return None
        
        connector = MockConnector()
        
        repr_str = repr(connector)
        assert 'MockConnector' in repr_str
        assert 'disconnected' in repr_str
        
        connector.connect()
        repr_str = repr(connector)
        assert 'connected' in repr_str


# ==================== Integration Tests ====================

class TestIntegration:
    """Integration tests for the connector framework."""
    
    def test_full_workflow(self):
        """Test complete workflow: config -> registry -> create -> use."""
        # Create configuration
        config = BaseConnectorConfig(
            timeout=60,
            retry=RetryConfig(max_retries=2, retry_delay=0.1)
        )
        
        # Define a test connector
        @connector(name='workflow_test', description='Workflow test connector')
        class WorkflowConnector(BaseConnector):
            def connect(self):
                self._on_connect_success()
                return True
            
            def disconnect(self):
                self._on_disconnect()
                return True
            
            def is_connected(self):
                return self._connected
            
            def search(self, query, limit=10, filters=None, **kwargs):
                self._update_activity_time()
                return [
                    SearchResult(
                        id='1',
                        title=query,
                        snippet=f'Result for {query}',
                        source='workflow_test',
                        metadata={}
                    )
                ]
            
            def get_by_id(self, id):
                return {'id': id, 'data': 'test'}
        
        # Create instance
        registry = ConnectorRegistry()
        instance = registry.create('workflow_test', config=config)
        
        # Use instance
        assert instance.connect() is True
        assert instance.is_connected() is True
        
        results = instance.search('test query')
        assert len(results) == 1
        assert results[0].title == 'test query'
        
        health = instance.health_check()
        assert health['healthy'] is True
        
        instance.disconnect()
        assert instance.is_connected() is False
        
        # Cleanup
        registry.unregister('workflow_test')
    
    def test_config_manager_integration(self):
        """Test config manager with registry."""
        manager = ConfigManager()
        manager.clear_cache()
        
        # Register config
        manager.register_config('integration_test', BaseConnectorConfig)
        
        # Get config with overrides
        config = manager.get_config(
            'integration_test',
            timeout=90,
            retry={'max_retries': 5}
        )
        
        assert config.timeout == 90
        assert config.retry.max_retries == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
