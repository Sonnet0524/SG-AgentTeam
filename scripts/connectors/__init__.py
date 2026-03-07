"""
Connectors module for external data sources.

Provides base classes and implementations for connecting to various
external data sources like email servers, databases, etc.

Implements TASK-INT1: Email Connector
"""

from .base import BaseConnector
from .email import EmailConnector

__all__ = ['BaseConnector', 'EmailConnector']
