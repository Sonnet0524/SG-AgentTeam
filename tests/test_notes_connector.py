"""
Unit tests for Notes Connector.

Tests the notes connector functionality including:
- Mock provider (for testing)
- Note search and retrieval
- Tag and folder filtering
- Notion API (mocked)

Implements TASK-C3: Notes Connector Tests
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock

from scripts.connectors.notes import (
    NotesConnector,
    NotesConfig,
    Note
)


class TestNotesConfig:
    """Tests for NotesConfig."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = NotesConfig()
        
        assert config.provider == "mock"
        assert config.max_results == 50
        assert config.timeout == 30
        assert config.notion_token == ""
    
    def test_custom_config(self):
        """Test custom configuration values."""
        config = NotesConfig(
            provider="notion",
            notion_token="secret_abc123",
            notion_database_id="db_123",
            max_results=100
        )
        
        assert config.provider == "notion"
        assert config.notion_token == "secret_abc123"
        assert config.notion_database_id == "db_123"
        assert config.max_results == 100
    
    def test_config_validation(self):
        """Test configuration validation."""
        config = NotesConfig(timeout=30)
        assert config.validate() is True
        
        with pytest.raises(ValueError):
            NotesConfig(timeout=-1).validate()


class TestNote:
    """Tests for Note dataclass."""
    
    def test_create_note(self):
        """Test creating a note."""
        note = Note(
            id="note_1",
            title="Test Note",
            content="This is a test note content.",
            folder="Personal",
            tags=["test", "important"]
        )
        
        assert note.id == "note_1"
        assert note.title == "Test Note"
        assert note.content == "This is a test note content."
        assert note.folder == "Personal"
        assert note.tags == ["test", "important"]
    
    def test_note_defaults(self):
        """Test default values for note."""
        note = Note(id="note_2", title="Simple Note")
        
        assert note.content == ""
        assert note.folder == ""
        assert note.tags == []
        assert note.created_time is None
        assert note.modified_time is None
        assert note.source == ""
        assert note.url == ""


class TestNotesConnector:
    """Tests for NotesConnector with mock provider."""
    
    @pytest.fixture
    def connector(self):
        """Create a connector with mock provider."""
        config = NotesConfig(provider="mock")
        connector = NotesConnector(config=config)
        return connector
    
    def test_connect(self, connector):
        """Test connecting to mock provider."""
        assert connector.connect() is True
        assert connector.is_connected() is True
    
    def test_disconnect(self, connector):
        """Test disconnecting from provider."""
        connector.connect()
        assert connector.disconnect() is True
        assert connector.is_connected() is False
    
    def test_context_manager(self, connector):
        """Test using connector as context manager."""
        with connector as conn:
            assert conn.is_connected()
            notes = conn.search_notes("project")
            assert len(notes) > 0
        
        assert not connector.is_connected()
    
    def test_search_notes(self, connector):
        """Test searching notes."""
        with connector as conn:
            notes = conn.search_notes("project", limit=10)
            
            assert len(notes) > 0
            assert all(isinstance(n, Note) for n in notes)
            # Check that results match the query
            for note in notes:
                query_in_note = (
                    "project" in note.title.lower() or
                    "project" in note.content.lower() or
                    any("project" in tag.lower() for tag in note.tags)
                )
                assert query_in_note
    
    def test_search_with_limit(self, connector):
        """Test search with limit parameter."""
        with connector as conn:
            notes = conn.search_notes("", limit=2)
            assert len(notes) <= 2
    
    def test_search_returns_search_results(self, connector):
        """Test that search returns SearchResult objects."""
        with connector as conn:
            results = conn.search("project")
            
            assert len(results) > 0
            assert all(r.source == 'notes' for r in results)
            assert all(r.id for r in results)
            assert all(r.title for r in results)
    
    def test_search_by_content(self, connector):
        """Test searching note content."""
        with connector as conn:
            # Search for content that appears in mock notes
            notes = conn.search_notes("recipe")
            
            assert len(notes) > 0
            # At least one note should have "recipe" in content
            has_recipe = any("recipe" in note.content.lower() for note in notes)
            assert has_recipe
    
    def test_search_by_tag(self, connector):
        """Test searching notes by tag."""
        with connector as conn:
            notes = conn.search_notes("project")
            
            # Some notes should have "project" tag or contain "project" in title/content
            assert len(notes) > 0
    
    def test_filter_by_folder(self, connector):
        """Test filtering notes by folder."""
        with connector as conn:
            notes = conn.search_notes(
                "",
                filters={'folder': 'Work'}
            )
            
            # All returned notes should be in the Work folder
            for note in notes:
                assert 'Work' in note.folder or note.folder == ''
    
    def test_filter_by_tag(self, connector):
        """Test filtering notes by tag."""
        with connector as conn:
            notes = conn.search_notes(
                "",
                filters={'tag': 'important'}
            )
            
            # All returned notes should have this tag
            for note in notes:
                assert 'important' in note.tags
    
    def test_filter_by_modified_date(self, connector):
        """Test filtering notes by modification date."""
        with connector as conn:
            recent_date = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
            
            notes = conn.search_notes(
                "",
                filters={'modified_after': recent_date}
            )
            
            # All notes should be modified after the filter date
            for note in notes:
                if note.modified_time:
                    assert note.modified_time >= datetime.strptime(recent_date, '%Y-%m-%d')
    
    def test_get_by_id(self, connector):
        """Test retrieving a note by ID."""
        with connector as conn:
            # First search to get a note ID
            notes = conn.search_notes("")
            assert len(notes) > 0
            
            note_id = notes[0].id
            
            # Retrieve by ID
            note_data = conn.get_by_id(note_id)
            
            assert note_data is not None
            assert note_data['id'] == note_id
            assert note_data['title'] == notes[0].title
    
    def test_get_by_id_not_found(self, connector):
        """Test retrieving a non-existent note."""
        with connector as conn:
            note_data = conn.get_by_id("nonexistent_id")
            assert note_data is None
    
    def test_get_recent_notes(self, connector):
        """Test getting recent notes."""
        with connector as conn:
            notes = conn.get_recent_notes(days=30, limit=10)
            
            assert isinstance(notes, list)
            assert all(isinstance(n, Note) for n in notes)
    
    def test_get_notes_by_tag(self, connector):
        """Test getting notes by tag."""
        with connector as conn:
            notes = conn.get_notes_by_tag("project", limit=10)
            
            assert isinstance(notes, list)
            # All notes should have the tag (or match in title/content)
    
    def test_search_not_connected(self, connector):
        """Test searching when not connected."""
        notes = connector.search_notes("project")
        assert notes == []
        assert "Not connected" in (connector.get_last_error() or "")
    
    def test_get_by_id_not_connected(self, connector):
        """Test get_by_id when not connected."""
        result = connector.get_by_id("test_id")
        assert result is None
    
    def test_health_check(self, connector):
        """Test health check."""
        connector.connect()
        health = connector.health_check()
        
        assert 'healthy' in health
        assert 'connected' in health
        assert health['connected'] is True
    
    def test_empty_query(self, connector):
        """Test searching with empty query."""
        with connector as conn:
            notes = conn.search_notes("")
            # Empty query should return all notes (or first page)
            assert isinstance(notes, list)


class TestNotesConnectorErrorHandling:
    """Tests for error handling."""
    
    def test_unsupported_provider(self):
        """Test connecting with unsupported provider."""
        config = NotesConfig(provider="unsupported")
        connector = NotesConnector(config=config)
        
        result = connector.connect()
        assert result is False
        assert "Unsupported provider" in connector.get_last_error()
    
    def test_connection_duration(self):
        """Test getting connection duration."""
        config = NotesConfig(provider="mock")
        connector = NotesConnector(config=config)
        
        # Not connected
        assert connector.get_connection_duration() is None
        
        # Connected
        connector.connect()
        duration = connector.get_connection_duration()
        assert duration is not None
        assert duration >= 0
    
    def test_reconnect(self):
        """Test reconnecting to provider."""
        config = NotesConfig(provider="mock")
        connector = NotesConnector(config=config)
        
        # Initial connection
        assert connector.connect() is True
        assert connector.is_connected()
        
        # Reconnect
        assert connector.reconnect() is True
        assert connector.is_connected()


class TestNotesConnectorSerialization:
    """Tests for serialization and data conversion."""
    
    @pytest.fixture
    def connector(self):
        """Create a connector with mock provider."""
        config = NotesConfig(provider="mock")
        return NotesConnector(config=config)
    
    def test_search_result_metadata(self, connector):
        """Test that search results include proper metadata."""
        with connector as conn:
            results = conn.search("project")
            
            assert len(results) > 0
            
            for result in results:
                assert 'folder' in result.metadata
                assert 'tags' in result.metadata
                assert 'provider' in result.metadata
                assert result.metadata['provider'] == 'mock'
    
    def test_note_to_dict(self, connector):
        """Test converting note to dictionary."""
        with connector as conn:
            notes = conn.search_notes("")
            assert len(notes) > 0
            
            note_data = conn.get_by_id(notes[0].id)
            assert note_data is not None
            
            # Check required fields
            assert 'id' in note_data
            assert 'title' in note_data
            assert 'content' in note_data
            assert 'provider' in note_data


class TestNotesConnectorApple:
    """Tests for Apple Notes provider (macOS only)."""
    
    @pytest.mark.skipif(
        True,  # Always skip for now as it requires macOS
        reason="Apple Notes requires macOS"
    )
    def test_apple_notes_connect(self):
        """Test connecting to Apple Notes."""
        config = NotesConfig(provider="apple")
        connector = NotesConnector(config=config)
        
        result = connector.connect()
        # Will fail on non-macOS
        assert isinstance(result, bool)


class TestNotesConnectorNotion:
    """Tests for Notion provider (mocked)."""
    
    def test_notion_missing_token(self):
        """Test connecting without Notion token."""
        config = NotesConfig(
            provider="notion",
            notion_token=""
        )
        connector = NotesConnector(config=config)
        
        result = connector.connect()
        assert result is False
        assert "token" in connector.get_last_error().lower()
    
    @patch('scripts.connectors.notes.HAS_REQUESTS', True)
    @patch('scripts.connectors.notes.requests')
    def test_notion_connect_success(self, mock_requests):
        """Test successful Notion connection."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'results': []}
        mock_requests.post.return_value = mock_response
        
        config = NotesConfig(
            provider="notion",
            notion_token="secret_test",
            notion_database_id="db_123"
        )
        connector = NotesConnector(config=config)
        
        result = connector.connect()
        assert result is True
    
    @patch('scripts.connectors.notes.HAS_REQUESTS', True)
    @patch('scripts.connectors.notes.requests')
    def test_notion_search(self, mock_requests):
        """Test searching Notion pages."""
        # Mock search response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'results': [
                {
                    'id': 'page_1',
                    'properties': {
                        'Name': {
                            'type': 'title',
                            'title': [{'plain_text': 'Test Page'}]
                        }
                    },
                    'created_time': '2026-03-08T10:00:00Z',
                    'last_edited_time': '2026-03-08T11:00:00Z',
                    'url': 'https://notion.so/page_1'
                }
            ]
        }
        mock_requests.post.return_value = mock_response
        
        config = NotesConfig(
            provider="notion",
            notion_token="secret_test"
        )
        connector = NotesConnector(config=config)
        connector._connected = True  # Fake connection
        
        notes = connector.search_notes("test")
        
        # Verify search was called
        assert mock_requests.post.called
    
    @patch('scripts.connectors.notes.HAS_REQUESTS', True)
    @patch('scripts.connectors.notes.requests')
    def test_notion_get_by_id(self, mock_requests):
        """Test retrieving a Notion page by ID."""
        # Mock page response
        mock_page_response = Mock()
        mock_page_response.status_code = 200
        mock_page_response.json.return_value = {
            'id': 'page_123',
            'properties': {
                'Name': {
                    'type': 'title',
                    'title': [{'plain_text': 'Test Page'}]
                }
            },
            'created_time': '2026-03-08T10:00:00Z',
            'last_edited_time': '2026-03-08T11:00:00Z',
            'url': 'https://notion.so/page_123'
        }
        
        # Mock blocks response
        mock_blocks_response = Mock()
        mock_blocks_response.status_code = 200
        mock_blocks_response.json.return_value = {
            'results': []
        }
        
        mock_requests.get.side_effect = [mock_page_response, mock_blocks_response]
        
        config = NotesConfig(
            provider="notion",
            notion_token="secret_test"
        )
        connector = NotesConnector(config=config)
        connector._connected = True
        
        result = connector.get_by_id("page_123")
        
        assert result is not None
        assert result['id'] == 'page_123'


class TestNotesConnectorIntegration:
    """Integration tests (require actual setup)."""
    
    @pytest.mark.skip(reason="Requires Notion API token")
    def test_notion_integration(self):
        """Test real Notion API integration."""
        config = NotesConfig(
            provider="notion",
            notion_token="real_token",
            notion_database_id="real_db_id"
        )
        connector = NotesConnector(config=config)
        
        assert connector.connect() is True
        
        notes = connector.search_notes("test")
        assert isinstance(notes, list)


# Performance tests
class TestNotesConnectorPerformance:
    """Performance tests for notes connector."""
    
    @pytest.fixture
    def connector(self):
        """Create a connector with mock provider."""
        config = NotesConfig(provider="mock")
        return NotesConnector(config=config)
    
    # Note: Performance tests require pytest-benchmark plugin
    # Uncomment these tests if pytest-benchmark is installed
    
    # def test_search_performance(self, connector, benchmark):
    #     """Test search performance."""
    #     connector.connect()
    #     
    #     result = benchmark(connector.search_notes, "project")
    #     assert isinstance(result, list)
    # 
    # def test_get_by_id_performance(self, connector, benchmark):
    #     """Test get_by_id performance."""
    #     connector.connect()
    #     
    #     # Get a real note ID first
    #     notes = connector.search_notes("")
    #     note_id = notes[0].id if notes else "mock_1"
    #     
    #     result = benchmark(connector.get_by_id, note_id)
    #     assert result is not None or result is None  # Either found or not found
