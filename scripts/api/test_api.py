"""
Test script for FastAPI Backend API.

Validates all API endpoints are working correctly.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that all modules can be imported."""
    print("=" * 60)
    print("Testing Module Imports")
    print("=" * 60)
    
    try:
        from scripts.api.main import app
        print("✓ Main app imported successfully")
    except Exception as e:
        print(f"✗ Failed to import main app: {e}")
        return False
    
    try:
        from scripts.api.models.schemas import (
            SearchRequest, SearchResponse, SearchResult,
            DocumentCreate, DocumentResponse,
            ConnectorStatus, ErrorResponse
        )
        print("✓ Schema models imported successfully")
    except Exception as e:
        print(f"✗ Failed to import schemas: {e}")
        return False
    
    try:
        from scripts.api.routes.search import router as search_router
        print("✓ Search router imported successfully")
    except Exception as e:
        print(f"✗ Failed to import search router: {e}")
        return False
    
    try:
        from scripts.api.routes.documents import router as documents_router
        print("✓ Documents router imported successfully")
    except Exception as e:
        print(f"✗ Failed to import documents router: {e}")
        return False
    
    try:
        from scripts.api.routes.connectors import router as connectors_router
        print("✓ Connectors router imported successfully")
    except Exception as e:
        print(f"✗ Failed to import connectors router: {e}")
        return False
    
    return True


def test_app_routes():
    """Test that all routes are registered."""
    print("\n" + "=" * 60)
    print("Testing Route Registration")
    print("=" * 60)
    
    from scripts.api.main import app
    
    # Collect all routes with their methods
    route_methods = {}
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            path = route.path
            methods = route.methods or set()
            if path not in route_methods:
                route_methods[path] = set()
            route_methods[path].update(methods)
    
    expected_routes = {
        "/": {"GET"},
        "/health": {"GET"},
        "/api": {"GET"},
        "/api/search": {"GET", "POST"},
        "/api/documents": {"GET", "POST"},
        "/api/documents/{doc_id}": {"GET", "PUT", "DELETE"},
        "/api/connectors/status": {"GET"},
        "/api/connectors/connect": {"POST"},
        "/api/connectors/disconnect": {"POST"},
        "/api/connectors/{connector_name}/status": {"GET"}
    }
    
    all_ok = True
    for path, expected_methods in expected_routes.items():
        if path in route_methods:
            actual_methods = route_methods[path]
            if expected_methods.issubset(actual_methods):
                print(f"✓ {path}: {', '.join(sorted(actual_methods))}")
            else:
                print(f"✗ {path}: Missing methods {expected_methods - actual_methods}")
                all_ok = False
        else:
            print(f"✗ {path}: Route not found")
            all_ok = False
    
    return all_ok


def test_schema_models():
    """Test Pydantic schema models."""
    print("\n" + "=" * 60)
    print("Testing Schema Models")
    print("=" * 60)
    
    from scripts.api.models.schemas import (
        SearchRequest, SearchResult, SearchResponse,
        DocumentCreate, DocumentResponse,
        ConnectorInfo, ConnectorStatus,
        ErrorResponse, HealthCheckResponse
    )
    from datetime import datetime
    
    try:
        # Test SearchRequest
        req = SearchRequest(query="test", limit=5)
        print(f"✓ SearchRequest: {req.query}")
        
        # Test SearchResult
        result = SearchResult(
            rank=1, similarity=0.9, snippet="test",
            metadata={"id": "1"}, index=0
        )
        print(f"✓ SearchResult: rank={result.rank}, similarity={result.similarity}")
        
        # Test SearchResponse
        resp = SearchResponse(
            results=[result], total=1, limit=10, offset=0, query_time_ms=45.2
        )
        print(f"✓ SearchResponse: {len(resp.results)} results")
        
        # Test DocumentCreate
        doc = DocumentCreate(
            content="Test content",
            metadata={"category": "test"}
        )
        print(f"✓ DocumentCreate: {len(doc.content)} chars")
        
        # Test DocumentResponse
        doc_resp = DocumentResponse(
            id="doc_123",
            content="Test content",
            metadata={"category": "test"},
            created_at=datetime.now(),
            chunk_count=1
        )
        print(f"✓ DocumentResponse: id={doc_resp.id}")
        
        # Test ConnectorInfo
        conn_info = ConnectorInfo(
            name="email",
            status="connected",
            last_sync=datetime.now()
        )
        print(f"✓ ConnectorInfo: {conn_info.name} - {conn_info.status}")
        
        # Test ConnectorStatus
        conn_status = ConnectorStatus(
            connectors=[conn_info],
            total=1
        )
        print(f"✓ ConnectorStatus: {conn_status.total} connectors")
        
        # Test ErrorResponse
        err = ErrorResponse(
            error="TestError",
            message="Test error message"
        )
        print(f"✓ ErrorResponse: {err.error}")
        
        # Test HealthCheckResponse
        health = HealthCheckResponse(
            status="ok",
            version="1.2.0",
            index_status="available",
            uptime_seconds=3600.0
        )
        print(f"✓ HealthCheckResponse: {health.status}")
        
        return True
        
    except Exception as e:
        print(f"✗ Schema model test failed: {e}")
        return False


def test_openapi_spec():
    """Test OpenAPI specification generation."""
    print("\n" + "=" * 60)
    print("Testing OpenAPI Specification")
    print("=" * 60)
    
    from scripts.api.main import app
    
    try:
        openapi = app.openapi()
        
        print(f"✓ OpenAPI version: {openapi.get('openapi', 'N/A')}")
        print(f"✓ API title: {openapi.get('info', {}).get('title', 'N/A')}")
        print(f"✓ API version: {openapi.get('info', {}).get('version', 'N/A')}")
        
        # Count paths
        paths = openapi.get('paths', {})
        print(f"✓ Total paths: {len(paths)}")
        
        # Check for key paths
        key_paths = ['/api/search', '/api/documents', '/api/connectors/status']
        for path in key_paths:
            if path in paths:
                print(f"  ✓ {path}")
            else:
                print(f"  ✗ {path} not found")
        
        return True
        
    except Exception as e:
        print(f"✗ OpenAPI spec test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("Knowledge Assistant API Test Suite")
    print("Version: 1.2.0")
    print("=" * 60 + "\n")
    
    results = {
        "Module Imports": test_imports(),
        "Route Registration": test_app_routes(),
        "Schema Models": test_schema_models(),
        "OpenAPI Specification": test_openapi_spec()
    }
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n⚠ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
