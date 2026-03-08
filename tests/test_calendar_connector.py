"""
Unit tests for Calendar Connector.

Tests the calendar connector functionality including:
- Mock provider (for testing)
- Event search and retrieval
- Date filtering
- iCal parsing (if icalendar is installed)

Implements TASK-C2: Calendar Connector Tests
"""

import pytest
from datetime import datetime, timedelta
from pathlib import Path

from scripts.connectors.calendar import (
    CalendarConnector,
    CalendarConfig,
    CalendarEvent
)


class TestCalendarConfig:
    """Tests for CalendarConfig."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = CalendarConfig()
        
        assert config.provider == "mock"
        assert config.calendar_id == "primary"
        assert config.max_results == 50
        assert config.timeout == 30
    
    def test_custom_config(self):
        """Test custom configuration values."""
        config = CalendarConfig(
            provider="google",
            credentials_file="creds.json",
            calendar_id="work@company.com",
            max_results=100
        )
        
        assert config.provider == "google"
        assert config.credentials_file == "creds.json"
        assert config.calendar_id == "work@company.com"
        assert config.max_results == 100
    
    def test_config_validation(self):
        """Test configuration validation."""
        config = CalendarConfig(timeout=30)
        assert config.validate() is True
        
        with pytest.raises(ValueError):
            CalendarConfig(timeout=-1).validate()


class TestCalendarEvent:
    """Tests for CalendarEvent dataclass."""
    
    def test_create_event(self):
        """Test creating a calendar event."""
        event = CalendarEvent(
            id="event_1",
            title="Test Meeting",
            description="A test meeting",
            location="Room 101",
            start_time=datetime(2026, 3, 8, 10, 0),
            end_time=datetime(2026, 3, 8, 11, 0),
            attendees=["alice@example.com"]
        )
        
        assert event.id == "event_1"
        assert event.title == "Test Meeting"
        assert event.location == "Room 101"
        assert len(event.attendees) == 1
        assert event.status == "confirmed"
    
    def test_event_defaults(self):
        """Test default values for event."""
        event = CalendarEvent(id="event_2", title="Simple Event")
        
        assert event.description == ""
        assert event.location == ""
        assert event.start_time is None
        assert event.end_time is None
        assert event.is_all_day is False
        assert event.attendees == []
        assert event.reminders == []


class TestCalendarConnector:
    """Tests for CalendarConnector with mock provider."""
    
    @pytest.fixture
    def connector(self):
        """Create a connector with mock provider."""
        config = CalendarConfig(provider="mock")
        connector = CalendarConnector(config=config)
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
            events = conn.search_events("meeting")
            assert len(events) > 0
        
        assert not connector.is_connected()
    
    def test_search_events(self, connector):
        """Test searching events."""
        with connector as conn:
            events = conn.search_events("meeting", limit=10)
            
            assert len(events) > 0
            assert all(isinstance(e, CalendarEvent) for e in events)
            # Check that results match the query in title, description, or location
            for event in events:
                query_in_event = (
                    "meeting" in event.title.lower() or
                    "meeting" in event.description.lower() or
                    "meeting" in event.location.lower()
                )
                assert query_in_event
    
    def test_search_with_limit(self, connector):
        """Test search with limit parameter."""
        with connector as conn:
            events = conn.search_events("", limit=2)
            assert len(events) <= 2
    
    def test_search_with_date_filter(self, connector):
        """Test search with date range filter."""
        with connector as conn:
            now = datetime.now()
            date_from = (now - timedelta(days=1)).strftime('%Y-%m-%d')
            date_to = (now + timedelta(days=5)).strftime('%Y-%m-%d')
            
            events = conn.search_events(
                "",
                filters={'date_from': date_from, 'date_to': date_to}
            )
            
            # All events should be within the date range
            for event in events:
                if event.start_time:
                    assert event.start_time >= datetime.strptime(date_from, '%Y-%m-%d')
                    assert event.start_time <= datetime.strptime(date_to, '%Y-%m-%d') + timedelta(days=1)
    
    def test_search_with_date_range_tuple(self, connector):
        """Test search with date_range tuple parameter."""
        with connector as conn:
            now = datetime.now()
            events = conn.search_events(
                "",
                date_range=(
                    now.strftime('%Y-%m-%d'),
                    (now + timedelta(days=10)).strftime('%Y-%m-%d')
                )
            )
            
            assert isinstance(events, list)
    
    def test_search_returns_search_results(self, connector):
        """Test that search returns SearchResult objects."""
        with connector as conn:
            results = conn.search("meeting")
            
            assert len(results) > 0
            assert all(r.source == 'calendar' for r in results)
            assert all(r.id for r in results)
            assert all(r.title for r in results)
    
    def test_get_by_id(self, connector):
        """Test retrieving an event by ID."""
        with connector as conn:
            # First search to get an event ID
            events = conn.search_events("")
            assert len(events) > 0
            
            event_id = events[0].id
            
            # Retrieve by ID
            event_data = conn.get_by_id(event_id)
            
            assert event_data is not None
            assert event_data['id'] == event_id
            assert event_data['title'] == events[0].title
    
    def test_get_by_id_not_found(self, connector):
        """Test retrieving a non-existent event."""
        with connector as conn:
            event_data = conn.get_by_id("nonexistent_id")
            assert event_data is None
    
    def test_get_upcoming_events(self, connector):
        """Test getting upcoming events."""
        with connector as conn:
            events = conn.get_upcoming_events(days=7, limit=10)
            
            assert isinstance(events, list)
            assert all(isinstance(e, CalendarEvent) for e in events)
            
            # All events should be in the future
            now = datetime.now()
            for event in events:
                if event.start_time:
                    assert event.start_time >= now - timedelta(days=1)
    
    def test_get_events_by_date(self, connector):
        """Test getting events for a specific date."""
        with connector as conn:
            # Get tomorrow's date
            tomorrow = datetime.now() + timedelta(days=1)
            events = connector.get_events_by_date(tomorrow)
            
            assert isinstance(events, list)
    
    def test_search_not_connected(self, connector):
        """Test searching when not connected."""
        events = connector.search_events("meeting")
        assert events == []
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
            events = conn.search_events("")
            # Empty query should return all events (or first page)
            assert isinstance(events, list)


class TestCalendarConnectorLocationFilter:
    """Tests for location filtering."""
    
    @pytest.fixture
    def connector(self):
        """Create a connector with mock provider."""
        config = CalendarConfig(provider="mock")
        return CalendarConnector(config=config)
    
    def test_filter_by_location(self, connector):
        """Test filtering events by location."""
        with connector as conn:
            # Search for events in a specific location
            events = conn.search_events(
                "",
                filters={'location': 'Conference Room'}
            )
            
            # All returned events should have matching location
            for event in events:
                assert 'Conference Room' in event.location


class TestCalendarConnectorAttendeeFilter:
    """Tests for attendee filtering."""
    
    @pytest.fixture
    def connector(self):
        """Create a connector with mock provider."""
        config = CalendarConfig(provider="mock")
        return CalendarConnector(config=config)
    
    def test_filter_by_attendee(self, connector):
        """Test filtering events by attendee."""
        with connector as conn:
            events = conn.search_events(
                "",
                filters={'attendee': 'alice@example.com'}
            )
            
            # All returned events should have this attendee
            for event in events:
                assert 'alice@example.com' in event.attendees


class TestCalendarConnectorErrors:
    """Tests for error handling."""
    
    def test_unsupported_provider(self):
        """Test connecting with unsupported provider."""
        config = CalendarConfig(provider="unsupported")
        connector = CalendarConnector(config=config)
        
        result = connector.connect()
        assert result is False
        assert "Unsupported provider" in connector.get_last_error()
    
    def test_connection_duration(self):
        """Test getting connection duration."""
        config = CalendarConfig(provider="mock")
        connector = CalendarConnector(config=config)
        
        # Not connected
        assert connector.get_connection_duration() is None
        
        # Connected
        connector.connect()
        duration = connector.get_connection_duration()
        assert duration is not None
        assert duration >= 0
    
    def test_reconnect(self):
        """Test reconnecting to provider."""
        config = CalendarConfig(provider="mock")
        connector = CalendarConnector(config=config)
        
        # Initial connection
        assert connector.connect() is True
        assert connector.is_connected()
        
        # Reconnect
        assert connector.reconnect() is True
        assert connector.is_connected()


class TestCalendarConnectorSerialization:
    """Tests for serialization and data conversion."""
    
    @pytest.fixture
    def connector(self):
        """Create a connector with mock provider."""
        config = CalendarConfig(provider="mock")
        return CalendarConnector(config=config)
    
    def test_search_result_metadata(self, connector):
        """Test that search results include proper metadata."""
        with connector as conn:
            results = conn.search("meeting")
            
            assert len(results) > 0
            
            for result in results:
                assert 'location' in result.metadata
                assert 'start_time' in result.metadata
                assert 'end_time' in result.metadata
                assert 'provider' in result.metadata
                assert result.metadata['provider'] == 'mock'
    
    def test_event_to_dict(self, connector):
        """Test converting event to dictionary."""
        with connector as conn:
            events = conn.search_events("")
            assert len(events) > 0
            
            event_data = conn.get_by_id(events[0].id)
            assert event_data is not None
            
            # Check required fields
            assert 'id' in event_data
            assert 'title' in event_data
            assert 'provider' in event_data


# Integration tests (require actual Google/iCal setup)
@pytest.mark.skip(reason="Requires Google Calendar credentials")
class TestGoogleCalendarIntegration:
    """Integration tests for Google Calendar."""
    
    def test_google_connect(self):
        """Test connecting to Google Calendar."""
        config = CalendarConfig(
            provider="google",
            credentials_file="credentials.json"
        )
        connector = CalendarConnector(config=config)
        
        assert connector.connect() is True
        assert connector.is_connected()


@pytest.mark.skip(reason="Requires iCal file")
class TestICalIntegration:
    """Integration tests for iCal files."""
    
    def test_ical_parse(self):
        """Test parsing an iCal file."""
        config = CalendarConfig(
            provider="ical",
            ical_file="calendar.ics"
        )
        connector = CalendarConnector(config=config)
        
        assert connector.connect() is True
        assert connector.is_connected()
        
        events = connector.search_events("")
        assert len(events) > 0
