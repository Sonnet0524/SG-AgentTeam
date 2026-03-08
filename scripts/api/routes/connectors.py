"""
Connector status API routes.

Provides endpoints to check and manage connector statuses.
"""

import os
import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from scripts.connectors.email import EmailConnector, EmailConfig
from ..models.schemas import (
    ConnectorStatus,
    ConnectorInfo,
    ConnectorConnectRequest,
    ErrorResponse
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/connectors", tags=["connectors"])

# In-memory connector instances and statuses
_connector_instances: dict = {}
_connector_statuses: dict = {}


def _get_email_connector_status() -> ConnectorInfo:
    """Get status of email connector."""
    # Check if we have a configured email connector
    if 'email' not in _connector_statuses:
        return ConnectorInfo(
            name="email",
            status="disconnected",
            last_sync=None,
            error=None,
            config=None
        )
    
    status_info = _connector_statuses['email']
    
    # Check if actually connected
    if 'email' in _connector_instances:
        connector = _connector_instances['email']
        if connector.is_connected():
            return ConnectorInfo(
                name="email",
                status="connected",
                last_sync=status_info.get('last_sync'),
                error=None,
                config=status_info.get('config_masked')
            )
    
    return ConnectorInfo(
        name="email",
        status=status_info.get('status', 'disconnected'),
        last_sync=status_info.get('last_sync'),
        error=status_info.get('error'),
        config=status_info.get('config_masked')
    )


def _mask_config(config: dict) -> dict:
    """Mask sensitive fields in configuration."""
    masked = config.copy()
    sensitive_fields = ['password', 'token', 'secret', 'api_key', 'credential']
    
    for field in sensitive_fields:
        if field in masked:
            masked[field] = '********'
    
    return masked


@router.get(
    "/status",
    response_model=ConnectorStatus,
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Get Connector Statuses",
    description="Retrieve the status of all configured connectors."
)
async def get_connector_status():
    """
    Get the status of all connectors.
    
    Returns a list of connector statuses including:
    - Connection status (connected/disconnected/error)
    - Last synchronization time
    - Error messages (if any)
    - Masked configuration (sensitive fields hidden)
    """
    try:
        connectors = []
        
        # Get email connector status
        email_status = _get_email_connector_status()
        connectors.append(email_status)
        
        # Add placeholder for future connectors
        # Calendar connector (not implemented yet)
        connectors.append(ConnectorInfo(
            name="calendar",
            status="not_configured",
            last_sync=None,
            error=None,
            config=None
        ))
        
        # Cloud storage connector (not implemented yet)
        connectors.append(ConnectorInfo(
            name="cloud_storage",
            status="not_configured",
            last_sync=None,
            error=None,
            config=None
        ))
        
        return ConnectorStatus(
            connectors=connectors,
            total=len(connectors)
        )
        
    except Exception as e:
        logger.error(f"Failed to get connector status: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": f"Failed to get connector status: {str(e)}"
            }
        )


@router.post(
    "/connect",
    response_model=ConnectorInfo,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Connection failed"}
    },
    summary="Connect Connector",
    description="Connect to a data source using provided configuration."
)
async def connect_connector(request: ConnectorConnectRequest):
    """
    Connect to a connector.
    
    Request body:
    - **connector_name**: Name of connector to connect (e.g., "email")
    - **config**: Connector configuration
    
    Returns the connector status after connection attempt.
    """
    try:
        connector_name = request.connector_name.lower()
        
        if connector_name == "email":
            # Create email connector
            config = EmailConfig(
                server=request.config.get('server', ''),
                port=request.config.get('port', 993),
                username=request.config.get('username', ''),
                password=request.config.get('password', ''),
                use_ssl=request.config.get('use_ssl', True)
            )
            
            connector = EmailConnector(config=config)
            
            # Attempt connection
            success = connector.connect()
            
            if success:
                # Store connector instance and status
                _connector_instances['email'] = connector
                _connector_statuses['email'] = {
                    'status': 'connected',
                    'last_sync': datetime.now(),
                    'error': None,
                    'config_masked': _mask_config(request.config)
                }
                
                logger.info(f"Successfully connected to email connector")
                
                return ConnectorInfo(
                    name="email",
                    status="connected",
                    last_sync=datetime.now(),
                    error=None,
                    config=_mask_config(request.config)
                )
            else:
                # Connection failed
                error_msg = connector.get_last_error() or "Connection failed"
                _connector_statuses['email'] = {
                    'status': 'error',
                    'last_sync': None,
                    'error': error_msg,
                    'config_masked': _mask_config(request.config)
                }
                
                logger.error(f"Failed to connect email connector: {error_msg}")
                
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error": "ConnectionFailed",
                        "message": f"Failed to connect to email server: {error_msg}",
                        "details": {"connector": "email"}
                    }
                )
        
        else:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "InvalidConnector",
                    "message": f"Unknown connector: {connector_name}",
                    "details": {"available_connectors": ["email"]}
                }
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to connect connector: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": f"Failed to connect connector: {str(e)}"
            }
        )


@router.post(
    "/disconnect",
    response_model=ConnectorInfo,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        404: {"model": ErrorResponse, "description": "Connector not found"}
    },
    summary="Disconnect Connector",
    description="Disconnect from a data source."
)
async def disconnect_connector(connector_name: str):
    """
    Disconnect a connector.
    
    - **connector_name**: Name of connector to disconnect
    
    Returns the connector status after disconnection.
    """
    try:
        connector_name = connector_name.lower()
        
        if connector_name not in _connector_instances:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "NotFoundError",
                    "message": f"Connector not connected: {connector_name}",
                    "details": {"connector_name": connector_name}
                }
            )
        
        # Disconnect
        connector = _connector_instances[connector_name]
        connector.disconnect()
        
        # Update status
        if connector_name in _connector_statuses:
            _connector_statuses[connector_name]['status'] = 'disconnected'
            _connector_statuses[connector_name]['error'] = None
        
        # Remove instance
        del _connector_instances[connector_name]
        
        logger.info(f"Disconnected from {connector_name} connector")
        
        return ConnectorInfo(
            name=connector_name,
            status="disconnected",
            last_sync=None,
            error=None,
            config=_connector_statuses.get(connector_name, {}).get('config_masked')
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to disconnect connector: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": f"Failed to disconnect connector: {str(e)}"
            }
        )


@router.get(
    "/{connector_name}/status",
    response_model=ConnectorInfo,
    responses={
        404: {"model": ErrorResponse, "description": "Connector not found"}
    },
    summary="Get Single Connector Status",
    description="Get the status of a specific connector."
)
async def get_single_connector_status(connector_name: str):
    """
    Get status of a specific connector.
    
    - **connector_name**: Name of the connector
    
    Returns detailed status information for the specified connector.
    """
    connector_name = connector_name.lower()
    
    if connector_name == "email":
        return _get_email_connector_status()
    elif connector_name in ["calendar", "cloud_storage"]:
        return ConnectorInfo(
            name=connector_name,
            status="not_configured",
            last_sync=None,
            error=None,
            config=None
        )
    else:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "NotFoundError",
                "message": f"Unknown connector: {connector_name}",
                "details": {"connector_name": connector_name}
            }
        )
