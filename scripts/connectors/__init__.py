"""
Connectors module for external data sources.

Provides base classes and implementations for connecting to various
external data sources like email servers, databases, etc.

Implements:
- TASK-INT1: Email Connector
- TASK-C1: Connector Framework Refactoring
- TASK-C2: Calendar Connector (Issue #38)
- TASK-C3: Notes Connector (Issue #39)
"""

from .config import (
    BaseConnectorConfig,
    RetryConfig,
    ConnectionPoolConfig,
    ConfigManager,
    config_manager
)
from .base import BaseConnector, SearchResult, with_retry
from .registry import (
    ConnectorRegistry,
    ConnectorInfo,
    connector_registry,
    connector
)
from .email import EmailConnector
from .calendar import CalendarConnector, CalendarConfig, CalendarEvent
from .notes import NotesConnector, NotesConfig, Note

# Backward compatibility alias
ConnectorConfig = BaseConnectorConfig

# Register connectors with registry
connector_registry.register(
    name='calendar',
    connector_class=CalendarConnector,
    config_class=CalendarConfig,
    description='Calendar connector supporting Google Calendar and iCal files',
    version='1.0.0',
    tags=['calendar', 'google', 'ical', 'events'],
    aliases=['google_calendar', 'ical']
)

connector_registry.register(
    name='notes',
    connector_class=NotesConnector,
    config_class=NotesConfig,
    description='Notes connector supporting Apple Notes and Notion',
    version='1.0.0',
    tags=['notes', 'apple', 'notion', 'productivity'],
    aliases=['apple_notes', 'notion']
)

__all__ = [
    # Base classes
    'BaseConnector',
    'SearchResult',
    'with_retry',
    
    # Configuration
    'BaseConnectorConfig',
    'ConnectorConfig',
    'RetryConfig',
    'ConnectionPoolConfig',
    'ConfigManager',
    'config_manager',
    
    # Registry
    'ConnectorRegistry',
    'ConnectorInfo',
    'connector_registry',
    'connector',
    
    # Connectors
    'EmailConnector',
    'CalendarConnector',
    'CalendarConfig',
    'CalendarEvent',
    'NotesConnector',
    'NotesConfig',
    'Note',
]
