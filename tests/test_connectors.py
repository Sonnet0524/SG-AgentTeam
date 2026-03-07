"""
Unit tests for connector modules.

Tests for BaseConnector and EmailConnector using mocked IMAP connections.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from scripts.connectors.base import BaseConnector, ConnectorConfig, SearchResult
from scripts.connectors.email import EmailConnector, EmailConfig, EmailSummary


class TestConnectorConfig:
    """Test cases for ConnectorConfig."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = ConnectorConfig()
        
        assert config.timeout == 30
        assert config.retry_count == 3
        assert config.retry_delay == 1.0
        assert config.verify_ssl is True
        assert config.use_tls is True
    
    def test_custom_config(self):
        """Test custom configuration values."""
        config = ConnectorConfig(
            timeout=60,
            retry_count=5,
            retry_delay=2.0
        )
        
        assert config.timeout == 60
        assert config.retry_count == 5
        assert config.retry_delay == 2.0


class TestSearchResult:
    """Test cases for SearchResult dataclass."""
    
    def test_search_result_creation(self):
        """Test creating a search result."""
        result = SearchResult(
            id="test_1",
            title="Test Title",
            snippet="Test snippet content",
            source="email",
            metadata={"sender": "test@example.com"}
        )
        
        assert result.id == "test_1"
        assert result.title == "Test Title"
        assert result.snippet == "Test snippet content"
        assert result.source == "email"
        assert result.timestamp is None
        assert result.score is None
    
    def test_search_result_with_timestamp(self):
        """Test search result with timestamp."""
        now = datetime.now()
        result = SearchResult(
            id="test_2",
            title="Test",
            snippet="Content",
            source="email",
            metadata={},
            timestamp=now
        )
        
        assert result.timestamp == now


class TestEmailConfig:
    """Test cases for EmailConfig."""
    
    def test_default_email_config(self):
        """Test default email configuration."""
        config = EmailConfig()
        
        assert config.server == ""
        assert config.port == 993
        assert config.username == ""
        assert config.password == ""
        assert config.default_folder == "INBOX"
        assert config.use_ssl is True
    
    def test_custom_email_config(self):
        """Test custom email configuration."""
        config = EmailConfig(
            server="imap.gmail.com",
            port=993,
            username="test@gmail.com",
            password="app_password"
        )
        
        assert config.server == "imap.gmail.com"
        assert config.username == "test@gmail.com"
        assert config.password == "app_password"


class TestEmailSummary:
    """Test cases for EmailSummary dataclass."""
    
    def test_email_summary_creation(self):
        """Test creating an email summary."""
        summary = EmailSummary(
            id="msg_123",
            subject="Test Subject",
            sender="sender@example.com",
            sender_name="Test Sender",
            snippet="Email content preview..."
        )
        
        assert summary.id == "msg_123"
        assert summary.subject == "Test Subject"
        assert summary.sender == "sender@example.com"
        assert summary.is_read is False
        assert summary.has_attachments is False


class TestEmailConnector:
    """Test cases for EmailConnector."""
    
    def test_connector_initialization(self):
        """Test connector initialization."""
        config = EmailConfig(
            server="imap.test.com",
            username="test@test.com",
            password="password"
        )
        connector = EmailConnector(config=config)
        
        assert connector.config.server == "imap.test.com"
        assert connector.is_connected() is False
    
    def test_connect_missing_server(self):
        """Test connect with missing server."""
        config = EmailConfig(username="test", password="pass")
        connector = EmailConnector(config=config)
        
        result = connector.connect()
        
        assert result is False
        assert "Server address is required" in connector.get_last_error()
    
    def test_connect_missing_credentials(self):
        """Test connect with missing credentials."""
        config = EmailConfig(server="imap.test.com")
        connector = EmailConnector(config=config)
        
        result = connector.connect()
        
        assert result is False
        assert "Username and password are required" in connector.get_last_error()
    
    @patch('scripts.connectors.email.imaplib.IMAP4_SSL')
    def test_connect_success(self, mock_imap):
        """Test successful connection."""
        mock_client = MagicMock()
        mock_client.login.return_value = ('OK', [b''])
        mock_imap.return_value = mock_client
        
        config = EmailConfig(
            server="imap.test.com",
            username="test@test.com",
            password="password"
        )
        connector = EmailConnector(config=config)
        
        result = connector.connect()
        
        assert result is True
        assert connector.is_connected() is True
        mock_imap.assert_called_once()
        mock_client.login.assert_called_once_with("test@test.com", "password")
    
    @patch('scripts.connectors.email.imaplib.IMAP4_SSL')
    def test_connect_auth_failure(self, mock_imap):
        """Test connection with authentication failure."""
        mock_client = MagicMock()
        mock_client.login.side_effect = Exception("Authentication failed")
        mock_imap.return_value = mock_client
        
        config = EmailConfig(
            server="imap.test.com",
            username="test@test.com",
            password="wrong_password"
        )
        connector = EmailConnector(config=config)
        
        result = connector.connect()
        
        assert result is False
        assert connector.is_connected() is False
    
    @patch('scripts.connectors.email.imaplib.IMAP4_SSL')
    def test_disconnect(self, mock_imap):
        """Test disconnect."""
        mock_client = MagicMock()
        mock_client.login.return_value = ('OK', [b''])
        mock_client.logout.return_value = ('OK', [b''])
        mock_imap.return_value = mock_client
        
        config = EmailConfig(
            server="imap.test.com",
            username="test@test.com",
            password="password"
        )
        connector = EmailConnector(config=config)
        
        connector.connect()
        result = connector.disconnect()
        
        assert result is True
        assert connector.is_connected() is False
    
    @patch('scripts.connectors.email.imaplib.IMAP4_SSL')
    def test_search_empty_query(self, mock_imap):
        """Test search with empty query."""
        mock_client = MagicMock()
        mock_imap.return_value = mock_client
        
        config = EmailConfig(
            server="imap.test.com",
            username="test@test.com",
            password="password"
        )
        connector = EmailConnector(config=config)
        connector.connect()
        
        results = connector.search("")
        
        assert results == []
    
    @patch('scripts.connectors.email.imaplib.IMAP4_SSL')
    def test_context_manager(self, mock_imap):
        """Test using connector as context manager."""
        mock_client = MagicMock()
        mock_client.login.return_value = ('OK', [b''])
        mock_client.logout.return_value = ('OK', [b''])
        mock_imap.return_value = mock_client
        
        config = EmailConfig(
            server="imap.test.com",
            username="test@test.com",
            password="password"
        )
        
        with EmailConnector(config=config) as connector:
            assert connector.is_connected() is True
        
        # After exiting context, should be disconnected
        assert connector.is_connected() is False
    
    @patch('scripts.connectors.email.imaplib.IMAP4_SSL')
    def test_search_success(self, mock_imap):
        """Test successful email search."""
        mock_client = MagicMock()
        mock_client.login.return_value = ('OK', [b''])
        mock_client.select.return_value = ('OK', [b''])
        mock_client.search.return_value = ('OK', [b'1 2 3'])
        # Mock fetch response
        mock_client.fetch.return_value = (
            'OK',
            [(b'1 (FLAGS \\Seen)', b'From: sender@test.com\r\nSubject: Test Subject\r\nDate: Mon, 1 Jan 2024 10:00:00 +0000\r\n\r\n')]
        )
        mock_imap.return_value = mock_client
        
        config = EmailConfig(
            server="imap.test.com",
            username="test@test.com",
            password="password"
        )
        connector = EmailConnector(config=config)
        connector.connect()
        
        results = connector.search("test query", limit=5)
        
        assert isinstance(results, list)
    
    @patch('scripts.connectors.email.imaplib.IMAP4_SSL')
    def test_search_not_connected(self, mock_imap):
        """Test search when not connected."""
        config = EmailConfig(
            server="imap.test.com",
            username="test@test.com",
            password="password"
        )
        connector = EmailConnector(config=config)
        # Don't connect
        
        results = connector.search("test query")
        
        assert results == []
        assert "Not connected" in connector.get_last_error()
    
    @patch('scripts.connectors.email.imaplib.IMAP4_SSL')
    def test_get_by_id_success(self, mock_imap):
        """Test getting email by ID."""
        mock_client = MagicMock()
        mock_client.login.return_value = ('OK', [b''])
        mock_client.select.return_value = ('OK', [b''])
        mock_client.fetch.return_value = (
            'OK',
            [(b'1 (RFC822)', b'From: sender@test.com\r\nSubject: Test\r\nDate: Mon, 1 Jan 2024 10:00:00\r\n\r\nTest body')]
        )
        mock_imap.return_value = mock_client
        
        config = EmailConfig(
            server="imap.test.com",
            username="test@test.com",
            password="password"
        )
        connector = EmailConnector(config=config)
        connector.connect()
        
        result = connector.get_by_id("1")
        
        assert result is not None
        assert result['id'] == "1"
    
    @patch('scripts.connectors.email.imaplib.IMAP4_SSL')
    def test_get_by_id_not_connected(self, mock_imap):
        """Test get_by_id when not connected."""
        config = EmailConfig(
            server="imap.test.com",
            username="test@test.com",
            password="password"
        )
        connector = EmailConnector(config=config)
        
        result = connector.get_by_id("1")
        
        assert result is None
    
    @patch('scripts.connectors.email.imaplib.IMAP4_SSL')
    def test_list_folders_success(self, mock_imap):
        """Test listing folders."""
        mock_client = MagicMock()
        mock_client.login.return_value = ('OK', [b''])
        mock_client.list.return_value = (
            'OK',
            [b'(\\HasNoChildren) "." "INBOX"', b'(\\HasNoChildren) "." "Sent"']
        )
        mock_imap.return_value = mock_client
        
        config = EmailConfig(
            server="imap.test.com",
            username="test@test.com",
            password="password"
        )
        connector = EmailConnector(config=config)
        connector.connect()
        
        folders = connector.list_folders()
        
        assert isinstance(folders, list)
    
    @patch('scripts.connectors.email.imaplib.IMAP4_SSL')
    def test_get_recent_emails(self, mock_imap):
        """Test getting recent emails."""
        mock_client = MagicMock()
        mock_client.login.return_value = ('OK', [b''])
        mock_client.select.return_value = ('OK', [b''])
        mock_client.search.return_value = ('OK', [b'1 2 3'])
        mock_client.fetch.return_value = (
            'OK',
            [(b'1 (FLAGS \\Seen)', b'From: test@test.com\r\nSubject: Recent\r\n\r\n')]
        )
        mock_imap.return_value = mock_client
        
        config = EmailConfig(
            server="imap.test.com",
            username="test@test.com",
            password="password"
        )
        connector = EmailConnector(config=config)
        connector.connect()
        
        emails = connector.get_recent_emails(count=5)
        
        assert isinstance(emails, list)
    
    def test_check_attachments_no_attachment(self):
        """Test checking for attachments (no attachment)."""
        from email.message import Message
        
        config = EmailConfig(server="test.com", username="u", password="p")
        connector = EmailConnector(config=config)
        
        msg = Message()
        msg.set_payload("Test body")
        
        result = connector._check_attachments(msg)
        
        assert result is False
    
    def test_summary_to_search_result(self):
        """Test converting EmailSummary to SearchResult."""
        config = EmailConfig(server="test.com", username="u", password="p")
        connector = EmailConnector(config=config)
        
        summary = EmailSummary(
            id="123",
            subject="Test Subject",
            sender="sender@test.com",
            snippet="Test snippet..."
        )
        
        result = connector._summary_to_search_result(summary)
        
        assert result.id == "123"
        assert result.title == "Test Subject"
        assert result.source == "email"
        assert result.metadata['sender'] == "sender@test.com"
    
    @patch('scripts.connectors.email.imaplib.IMAP4_SSL')
    def test_select_folder_success(self, mock_imap):
        """Test selecting a folder."""
        mock_client = MagicMock()
        mock_client.login.return_value = ('OK', [b''])
        mock_client.select.return_value = ('OK', [b''])
        mock_imap.return_value = mock_client
        
        config = EmailConfig(
            server="imap.test.com",
            username="test@test.com",
            password="password"
        )
        connector = EmailConnector(config=config)
        connector.connect()
        
        result = connector._select_folder("INBOX")
        
        assert result is True
    
    @patch('scripts.connectors.email.imaplib.IMAP4_SSL')
    def test_select_folder_failure(self, mock_imap):
        """Test selecting a folder that fails."""
        mock_client = MagicMock()
        mock_client.login.return_value = ('OK', [b''])
        mock_client.select.return_value = ('NO', [b'Folder not found'])
        mock_imap.return_value = mock_client
        
        config = EmailConfig(
            server="imap.test.com",
            username="test@test.com",
            password="password"
        )
        connector = EmailConnector(config=config)
        connector.connect()
        
        result = connector._select_folder("NONEXISTENT")
        
        assert result is False
    
    def test_fetch_snippet_no_client(self):
        """Test fetching snippet without client."""
        config = EmailConfig(server="test.com", username="u", password="p")
        connector = EmailConnector(config=config)
        
        result = connector._fetch_snippet(b"1")
        
        assert result == ""
    
    def test_fetch_email_summary_no_client(self):
        """Test fetching email summary without client."""
        config = EmailConfig(server="test.com", username="u", password="p")
        connector = EmailConnector(config=config)
        
        result = connector._fetch_email_summary(b"1", "INBOX")
        
        assert result is None
    
    @patch('scripts.connectors.email.imaplib.IMAP4_SSL')
    def test_search_folder_failure(self, mock_imap):
        """Test search when folder selection fails."""
        mock_client = MagicMock()
        mock_client.login.return_value = ('OK', [b''])
        mock_client.select.return_value = ('NO', [b'Folder not found'])
        mock_imap.return_value = mock_client
        
        config = EmailConfig(
            server="imap.test.com",
            username="test@test.com",
            password="password"
        )
        connector = EmailConnector(config=config)
        connector.connect()
        
        results = connector.search("test", folders=["NONEXISTENT"])
        
        assert results == []
    
    def test_is_connected_no_client(self):
        """Test is_connected without client."""
        config = EmailConfig(server="test.com", username="u", password="p")
        connector = EmailConnector(config=config)
        
        result = connector.is_connected()
        
        assert result is False
    
    @patch('scripts.connectors.email.imaplib.IMAP4_SSL')
    def test_is_connected_noop_failure(self, mock_imap):
        """Test is_connected when NOOP fails."""
        mock_client = MagicMock()
        mock_client.login.return_value = ('OK', [b''])
        mock_client.noop.side_effect = Exception("Connection lost")
        mock_imap.return_value = mock_client
        
        config = EmailConfig(
            server="imap.test.com",
            username="test@test.com",
            password="password"
        )
        connector = EmailConnector(config=config)
        connector.connect()
        
        result = connector.is_connected()
        
        assert result is False
    
    def test_repr(self):
        """Test string representation."""
        config = EmailConfig(server="test.com", username="u", password="p")
        connector = EmailConnector(config=config)
        
        repr_str = repr(connector)
        
        assert "EmailConnector" in repr_str
        assert "disconnected" in repr_str
    
    def test_get_last_error_none(self):
        """Test get_last_error when no error."""
        config = EmailConfig(server="test.com", username="u", password="p")
        connector = EmailConnector(config=config)
        
        error = connector.get_last_error()
        
        assert error is None
    
    @patch('scripts.connectors.email.imaplib.IMAP4_SSL')
    def test_disconnect_with_close_error(self, mock_imap):
        """Test disconnect when close raises error."""
        mock_client = MagicMock()
        mock_client.login.return_value = ('OK', [b''])
        mock_client.close.side_effect = Exception("Close error")
        mock_client.logout.return_value = ('OK', [b''])
        mock_imap.return_value = mock_client
        
        config = EmailConfig(
            server="imap.test.com",
            username="test@test.com",
            password="password"
        )
        connector = EmailConnector(config=config)
        connector.connect()
        
        result = connector.disconnect()
        
        assert result is True


class TestBuildSearchCriteria:
    """Test cases for search criteria building."""
    
    def test_single_term_query(self):
        """Test building criteria for single term."""
        config = EmailConfig(server="test.com", username="u", password="p")
        connector = EmailConnector(config=config)
        
        criteria = connector._build_search_criteria("budget")
        
        assert 'SUBJECT' in criteria
        assert 'budget' in criteria
    
    def test_multi_term_query(self):
        """Test building criteria for multiple terms."""
        config = EmailConfig(server="test.com", username="u", password="p")
        connector = EmailConnector(config=config)
        
        criteria = connector._build_search_criteria("project budget 2024")
        
        assert 'OR' in criteria
    
    def test_date_filter(self):
        """Test building criteria with date filter."""
        config = EmailConfig(server="test.com", username="u", password="p")
        connector = EmailConnector(config=config)
        
        criteria = connector._build_search_criteria(
            "budget",
            filters={'date_from': '2024-01-01', 'date_to': '2024-12-31'}
        )
        
        assert 'SINCE' in criteria
        assert 'BEFORE' in criteria
    
    def test_sender_filter(self):
        """Test building criteria with sender filter."""
        config = EmailConfig(server="test.com", username="u", password="p")
        connector = EmailConnector(config=config)
        
        criteria = connector._build_search_criteria(
            "budget",
            filters={'sender': 'boss@company.com'}
        )
        
        assert 'FROM' in criteria
        assert 'boss@company.com' in criteria
    
    def test_unread_filter(self):
        """Test building criteria for unread emails."""
        config = EmailConfig(server="test.com", username="u", password="p")
        connector = EmailConnector(config=config)
        
        criteria = connector._build_search_criteria(
            "budget",
            filters={'unread_only': True}
        )
        
        assert 'UNSEEN' in criteria


class TestDecodeHeader:
    """Test cases for header decoding."""
    
    def test_simple_header(self):
        """Test decoding simple ASCII header."""
        config = EmailConfig(server="test.com", username="u", password="p")
        connector = EmailConnector(config=config)
        
        result = connector._decode_header("Simple Subject")
        
        assert result == "Simple Subject"
    
    def test_encoded_header(self):
        """Test decoding encoded header."""
        config = EmailConfig(server="test.com", username="u", password="p")
        connector = EmailConnector(config=config)
        
        # UTF-8 encoded subject
        result = connector._decode_header("=?utf-8?b?5rWL6K+V6YKu5Lu2?=")
        
        # Should decode without error
        assert isinstance(result, str)
    
    def test_empty_header(self):
        """Test decoding empty header."""
        config = EmailConfig(server="test.com", username="u", password="p")
        connector = EmailConnector(config=config)
        
        result = connector._decode_header("")
        
        assert result == ""


# Integration test placeholder (requires real IMAP server)
@pytest.mark.integration
class TestEmailConnectorIntegration:
    """Integration tests for EmailConnector (requires real IMAP)."""
    
    @pytest.mark.skip(reason="Requires real IMAP server credentials")
    def test_real_connection(self):
        """Test connection to real IMAP server."""
        # This test requires real credentials
        # Set environment variables or use test configuration
        pass
    
    @pytest.mark.skip(reason="Requires real IMAP server credentials")
    def test_real_search(self):
        """Test search on real IMAP server."""
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
