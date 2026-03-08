"""
Calendar connector implementation supporting Google Calendar API and iCal files.

Provides functionality to connect to calendar services, search events,
and retrieve event details.

Implements TASK-C2: Calendar Connector (Issue #38)
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import logging
import re

from .base import BaseConnector, ConnectorConfig, SearchResult
from .config import BaseConnectorConfig

logger = logging.getLogger(__name__)

# Type checking imports
try:
    from icalendar import Calendar as ICalCalendar, Event as ICalEvent
    HAS_ICAL = True
except ImportError:
    HAS_ICAL = False
    logger.debug("icalendar not installed, iCal support disabled")

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    HAS_GOOGLE = True
except ImportError:
    HAS_GOOGLE = False
    logger.debug("Google API libraries not installed, Google Calendar support disabled")


@dataclass
class CalendarConfig(BaseConnectorConfig):
    """Configuration for calendar connector.
    
    Attributes:
        provider: Calendar provider ('google', 'ical', or 'mock')
        credentials_file: Path to Google credentials JSON file
        token_file: Path to store Google OAuth token
        ical_file: Path to iCal file (for iCal provider)
        calendar_id: Google Calendar ID (default: 'primary')
        max_results: Maximum number of events to return
    """
    
    provider: str = "mock"
    credentials_file: str = ""
    token_file: str = ""
    ical_file: str = ""
    calendar_id: str = "primary"
    max_results: int = 50


@dataclass
class CalendarEvent:
    """Represents a calendar event.
    
    Attributes:
        id: Unique event identifier
        title: Event title/summary
        description: Event description
        location: Event location
        start_time: Event start time
        end_time: Event end time
        is_all_day: Whether it's an all-day event
        attendees: List of attendee emails
        organizer: Organizer email
        status: Event status (confirmed, tentative, cancelled)
        recurrence: Recurrence rule (if recurring event)
        reminders: Reminder settings
        metadata: Additional provider-specific metadata
    """
    
    id: str
    title: str
    description: str = ""
    location: str = ""
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_all_day: bool = False
    attendees: List[str] = field(default_factory=list)
    organizer: str = ""
    status: str = "confirmed"
    recurrence: str = ""
    reminders: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class CalendarConnector(BaseConnector):
    """
    Calendar connector supporting multiple providers.
    
    Provides a unified interface for accessing calendar events from:
    - Google Calendar (via Google Calendar API)
    - iCal files (via icalendar library)
    - Mock calendar (for testing)
    
    Attributes:
        config: CalendarConfig instance
        _service: Provider-specific service client
        _events_cache: Cache for loaded events
    
    Example:
        >>> # Google Calendar
        >>> config = CalendarConfig(
        ...     provider="google",
        ...     credentials_file="credentials.json",
        ...     token_file="token.json"
        ... )
        >>> connector = CalendarConnector(config=config)
        >>> 
        >>> with CalendarConnector(config=config) as conn:
        ...     events = conn.search_events("meeting", limit=10)
        ...     for event in events:
        ...         print(f"{event.title} at {event.start_time}")
        >>> 
        >>> # iCal file
        >>> config = CalendarConfig(
        ...     provider="ical",
        ...     ical_file="calendar.ics"
        ... )
        >>> connector = CalendarConnector(config=config)
        >>> if connector.connect():
        ...     events = connector.search_events("project")
        ...     connector.disconnect()
    """
    
    def __init__(self, config: Optional[CalendarConfig] = None):
        """
        Initialize the calendar connector.
        
        Args:
            config: CalendarConfig instance
        """
        if config is None:
            config = CalendarConfig()
        super().__init__(config)
        self.config: CalendarConfig = config
        self._service: Any = None
        self._events_cache: List[CalendarEvent] = []
    
    def connect(self) -> bool:
        """
        Establish connection to the calendar provider.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        self._clear_error()
        
        try:
            if self.config.provider == "google":
                return self._connect_google()
            elif self.config.provider == "ical":
                return self._connect_ical()
            elif self.config.provider == "mock":
                return self._connect_mock()
            else:
                self._set_error(f"Unsupported provider: {self.config.provider}")
                return False
        except Exception as e:
            self._set_error(f"Connection failed: {e}")
            return False
    
    def disconnect(self) -> bool:
        """
        Close the connection and cleanup resources.
        
        Returns:
            bool: True if disconnection successful
        """
        self._service = None
        self._events_cache = []
        self._on_disconnect()
        return True
    
    def is_connected(self) -> bool:
        """
        Check if the connection is active.
        
        Returns:
            bool: True if connected
        """
        if self.config.provider == "google":
            return self._service is not None
        elif self.config.provider == "ical":
            return len(self._events_cache) > 0
        elif self.config.provider == "mock":
            return self._connected
        return False
    
    def _connect_google(self) -> bool:
        """Connect to Google Calendar API."""
        if not HAS_GOOGLE:
            self._set_error("Google API libraries not installed. Install with: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
            return False
        
        if not self.config.credentials_file:
            self._set_error("Google credentials file not specified")
            return False
        
        creds = None
        token_path = Path(self.config.token_file) if self.config.token_file else None
        
        # Load existing token
        if token_path and token_path.exists():
            try:
                creds = Credentials.from_authorized_user_file(str(token_path))
            except Exception as e:
                logger.warning(f"Failed to load token: {e}")
        
        # If no valid credentials, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    logger.warning(f"Token refresh failed: {e}")
                    creds = None
            
            if not creds:
                # Need to authenticate
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.config.credentials_file,
                    ['https://www.googleapis.com/auth/calendar.readonly']
                )
                creds = flow.run_local_server(port=0)
            
            # Save token
            if token_path:
                token_path.parent.mkdir(parents=True, exist_ok=True)
                with open(token_path, 'w') as token:
                    token.write(creds.to_json())
        
        # Build service
        self._service = build('calendar', 'v3', credentials=creds)
        self._on_connect_success()
        return True
    
    def _connect_ical(self) -> bool:
        """Connect to iCal file."""
        if not HAS_ICAL:
            self._set_error("icalendar library not installed. Install with: pip install icalendar")
            return False
        
        if not self.config.ical_file:
            self._set_error("iCal file not specified")
            return False
        
        ical_path = Path(self.config.ical_file)
        if not ical_path.exists():
            self._set_error(f"iCal file not found: {self.config.ical_file}")
            return False
        
        # Load and parse iCal file
        try:
            with open(ical_path, 'rb') as f:
                cal = ICalCalendar.from_ical(f.read())
            
            # Parse events
            self._events_cache = []
            for component in cal.walk():
                if component.name == "VEVENT":
                    event = self._parse_ical_event(component)
                    if event:
                        self._events_cache.append(event)
            
            self._on_connect_success()
            return True
        except Exception as e:
            self._set_error(f"Failed to parse iCal file: {e}")
            return False
    
    def _connect_mock(self) -> bool:
        """Connect to mock calendar (for testing)."""
        # Create some mock events
        now = datetime.now()
        self._events_cache = [
            CalendarEvent(
                id="mock_1",
                title="Team Meeting",
                description="Weekly team sync meeting",
                location="Conference Room A",
                start_time=now + timedelta(days=1, hours=10),
                end_time=now + timedelta(days=1, hours=11),
                attendees=["alice@example.com", "bob@example.com"],
                organizer="alice@example.com"
            ),
            CalendarEvent(
                id="mock_2",
                title="Project Review",
                description="Review project progress and next steps",
                location="Meeting Room B",
                start_time=now + timedelta(days=2, hours=14),
                end_time=now + timedelta(days=2, hours=15),
                attendees=["charlie@example.com"],
                organizer="charlie@example.com"
            ),
            CalendarEvent(
                id="mock_3",
                title="Lunch with Client",
                description="Discuss partnership opportunities",
                location="Downtown Restaurant",
                start_time=now + timedelta(days=3, hours=12),
                end_time=now + timedelta(days=3, hours=13, minutes=30),
                attendees=["client@example.com"],
                organizer="user@example.com"
            )
        ]
        self._on_connect_success()
        return True
    
    def _parse_ical_event(self, component: Any) -> Optional[CalendarEvent]:
        """Parse an iCal event component into CalendarEvent."""
        try:
            # Extract basic properties
            uid = str(component.get('uid', ''))
            summary = str(component.get('summary', 'Untitled'))
            description = str(component.get('description', ''))
            location = str(component.get('location', ''))
            
            # Parse dates
            dtstart = component.get('dtstart')
            dtend = component.get('dtend')
            
            start_time = None
            end_time = None
            is_all_day = False
            
            if dtstart:
                start_val = dtstart.dt
                if isinstance(start_val, datetime):
                    start_time = start_val
                else:
                    # Date only (all-day event)
                    start_time = datetime.combine(start_val, datetime.min.time())
                    is_all_day = True
            
            if dtend:
                end_val = dtend.dt
                if isinstance(end_val, datetime):
                    end_time = end_val
                else:
                    end_time = datetime.combine(end_val, datetime.min.time())
            
            # Extract attendees
            attendees = []
            if component.get('attendee'):
                for attendee in component.get('attendee'):
                    email = str(attendee).replace('mailto:', '')
                    attendees.append(email)
            
            # Extract organizer
            organizer = ""
            if component.get('organizer'):
                organizer = str(component.get('organizer')).replace('mailto:', '')
            
            # Extract recurrence rule
            recurrence = ""
            if component.get('rrule'):
                recurrence = str(component.get('rrule'))
            
            return CalendarEvent(
                id=uid,
                title=summary,
                description=description,
                location=location,
                start_time=start_time,
                end_time=end_time,
                is_all_day=is_all_day,
                attendees=attendees,
                organizer=organizer,
                recurrence=recurrence
            )
        except Exception as e:
            logger.warning(f"Failed to parse iCal event: {e}")
            return None
    
    def search(
        self,
        query: str,
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> List[SearchResult]:
        """
        Search for calendar events matching the query.
        
        Args:
            query: Search query (keywords)
            limit: Maximum number of results
            filters: Optional filters:
                - date_from: Start date (datetime or str)
                - date_to: End date (datetime or str)
                - location: Filter by location
                - attendee: Filter by attendee email
            **kwargs: Additional parameters
        
        Returns:
            List of SearchResult objects
        """
        # Use search_events method for backward compatibility
        events = self.search_events(query, limit=limit, filters=filters, **kwargs)
        
        # Convert to SearchResult
        results = []
        for event in events:
            result = SearchResult(
                id=event.id,
                title=event.title,
                snippet=event.description[:200] if event.description else "",
                source='calendar',
                metadata={
                    'location': event.location,
                    'start_time': event.start_time.isoformat() if event.start_time else None,
                    'end_time': event.end_time.isoformat() if event.end_time else None,
                    'is_all_day': event.is_all_day,
                    'attendees': event.attendees,
                    'organizer': event.organizer,
                    'status': event.status,
                    'provider': self.config.provider
                },
                timestamp=event.start_time
            )
            results.append(result)
        
        return results
    
    def search_events(
        self,
        query: str,
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        date_range: Optional[Tuple[str, str]] = None,
        **kwargs
    ) -> List[CalendarEvent]:
        """
        Search for calendar events matching the query.
        
        Args:
            query: Search query (keywords)
            limit: Maximum number of results
            filters: Optional filters
            date_range: Optional tuple of (start_date, end_date) as YYYY-MM-DD strings
            **kwargs: Additional parameters
        
        Returns:
            List of CalendarEvent objects
        
        Example:
            >>> events = connector.search_events(
            ...     "meeting",
            ...     limit=5,
            ...     date_range=("2026-03-01", "2026-03-31")
            ... )
        """
        if not self.is_connected():
            self._set_error("Not connected to calendar provider")
            return []
        
        # Empty query is allowed - will return all events (up to limit)
        query = query.strip() if query else ""
        
        self._clear_error()
        
        # Handle date_range parameter
        if date_range and not filters:
            filters = {}
        
        if date_range:
            filters['date_from'] = date_range[0]
            filters['date_to'] = date_range[1]
        
        try:
            if self.config.provider == "google":
                return self._search_google_events(query, limit, filters)
            elif self.config.provider in ("ical", "mock"):
                return self._search_local_events(query, limit, filters)
            else:
                return []
        except Exception as e:
            self._set_error(f"Search failed: {e}")
            return []
    
    def _search_google_events(
        self,
        query: str,
        limit: int,
        filters: Optional[Dict[str, Any]]
    ) -> List[CalendarEvent]:
        """Search Google Calendar events."""
        if not self._service:
            return []
        
        events = []
        
        try:
            # Build time range
            time_min = None
            time_max = None
            
            if filters:
                if 'date_from' in filters:
                    time_min = self._parse_datetime(filters['date_from'])
                if 'date_to' in filters:
                    time_max = self._parse_datetime(filters['date_to'])
            
            # Default to next 30 days if no range specified
            if not time_min:
                time_min = datetime.utcnow()
            if not time_max:
                time_max = time_min + timedelta(days=30)
            
            # Call Calendar API
            events_result = self._service.events().list(
                calendarId=self.config.calendar_id,
                timeMin=time_min.isoformat() + 'Z',
                timeMax=time_max.isoformat() + 'Z',
                maxResults=min(limit, self.config.max_results),
                singleEvents=True,
                orderBy='startTime',
                q=query
            ).execute()
            
            # Parse results
            for item in events_result.get('items', []):
                event = self._parse_google_event(item)
                if event:
                    events.append(event)
        
        except HttpError as e:
            self._set_error(f"Google Calendar API error: {e}")
            return []
        
        return events
    
    def _parse_google_event(self, item: Dict[str, Any]) -> Optional[CalendarEvent]:
        """Parse a Google Calendar event item."""
        try:
            # Extract basic properties
            event_id = item.get('id', '')
            summary = item.get('summary', 'Untitled')
            description = item.get('description', '')
            location = item.get('location', '')
            status = item.get('status', 'confirmed')
            
            # Parse start/end times
            start_data = item.get('start', {})
            end_data = item.get('end', {})
            
            is_all_day = 'date' in start_data
            
            if is_all_day:
                start_time = datetime.strptime(start_data['date'], '%Y-%m-%d')
                end_time = datetime.strptime(end_data['date'], '%Y-%m-%d')
            else:
                start_time = datetime.fromisoformat(start_data['dateTime'].replace('Z', '+00:00'))
                end_time = datetime.fromisoformat(end_data['dateTime'].replace('Z', '+00:00'))
            
            # Extract attendees
            attendees = []
            for attendee in item.get('attendees', []):
                email = attendee.get('email', '')
                if email:
                    attendees.append(email)
            
            # Extract organizer
            organizer = ""
            if 'organizer' in item:
                organizer = item['organizer'].get('email', '')
            
            # Extract recurrence
            recurrence = ""
            if 'recurrence' in item and item['recurrence']:
                recurrence = item['recurrence'][0]  # Take first rule
            
            # Extract reminders
            reminders = []
            if 'reminders' in item and 'overrides' in item['reminders']:
                for reminder in item['reminders']['overrides']:
                    reminders.append({
                        'method': reminder.get('method', 'popup'),
                        'minutes': reminder.get('minutes', 0)
                    })
            
            return CalendarEvent(
                id=event_id,
                title=summary,
                description=description,
                location=location,
                start_time=start_time,
                end_time=end_time,
                is_all_day=is_all_day,
                attendees=attendees,
                organizer=organizer,
                status=status,
                recurrence=recurrence,
                reminders=reminders,
                metadata=item  # Store full item for reference
            )
        except Exception as e:
            logger.warning(f"Failed to parse Google event: {e}")
            return None
    
    def _search_local_events(
        self,
        query: str,
        limit: int,
        filters: Optional[Dict[str, Any]]
    ) -> List[CalendarEvent]:
        """Search local events (iCal or mock)."""
        query_lower = query.lower()
        matching_events = []
        
        for event in self._events_cache:
            # Check if query matches title, description, or location
            # If query is empty, match all events
            if query_lower == "" or (
                query_lower in event.title.lower() or
                query_lower in event.description.lower() or
                query_lower in event.location.lower()
            ):
                # Apply filters
                if filters and not self._matches_filters(event, filters):
                    continue
                
                matching_events.append(event)
        
        # Sort by start time
        matching_events.sort(key=lambda e: e.start_time or datetime.max)
        
        return matching_events[:limit]
    
    def _matches_filters(self, event: CalendarEvent, filters: Dict[str, Any]) -> bool:
        """Check if event matches all filters."""
        # Date range filter
        if 'date_from' in filters:
            date_from = self._parse_datetime(filters['date_from'])
            if date_from and event.start_time and event.start_time < date_from:
                return False
        
        if 'date_to' in filters:
            date_to = self._parse_datetime(filters['date_to'])
            if date_to and event.start_time and event.start_time > date_to:
                return False
        
        # Location filter
        if 'location' in filters:
            if filters['location'].lower() not in event.location.lower():
                return False
        
        # Attendee filter
        if 'attendee' in filters:
            if filters['attendee'] not in event.attendees:
                return False
        
        return True
    
    def _parse_datetime(self, value: Any) -> Optional[datetime]:
        """Parse datetime from various formats."""
        if isinstance(value, datetime):
            return value
        
        if isinstance(value, str):
            # Try ISO format
            try:
                return datetime.fromisoformat(value.replace('Z', '+00:00'))
            except:
                pass
            
            # Try YYYY-MM-DD format
            try:
                return datetime.strptime(value, '%Y-%m-%d')
            except:
                pass
        
        return None
    
    def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific event by its ID.
        
        Args:
            id: Event identifier
        
        Returns:
            Dict containing event details, or None if not found
        """
        if not self.is_connected():
            self._set_error("Not connected to calendar provider")
            return None
        
        self._clear_error()
        
        try:
            if self.config.provider == "google":
                return self._get_google_event_by_id(id)
            elif self.config.provider in ("ical", "mock"):
                return self._get_local_event_by_id(id)
            else:
                return None
        except Exception as e:
            self._set_error(f"Failed to retrieve event: {e}")
            return None
    
    def _get_google_event_by_id(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Get a Google Calendar event by ID."""
        if not self._service:
            return None
        
        try:
            event_data = self._service.events().get(
                calendarId=self.config.calendar_id,
                eventId=event_id
            ).execute()
            
            event = self._parse_google_event(event_data)
            if event:
                return {
                    'id': event.id,
                    'title': event.title,
                    'description': event.description,
                    'location': event.location,
                    'start_time': event.start_time.isoformat() if event.start_time else None,
                    'end_time': event.end_time.isoformat() if event.end_time else None,
                    'is_all_day': event.is_all_day,
                    'attendees': event.attendees,
                    'organizer': event.organizer,
                    'status': event.status,
                    'recurrence': event.recurrence,
                    'reminders': event.reminders,
                    'provider': 'google'
                }
        except HttpError as e:
            if e.resp.status == 404:
                return None
            self._set_error(f"Google Calendar API error: {e}")
        
        return None
    
    def _get_local_event_by_id(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Get a local event by ID."""
        for event in self._events_cache:
            if event.id == event_id:
                return {
                    'id': event.id,
                    'title': event.title,
                    'description': event.description,
                    'location': event.location,
                    'start_time': event.start_time.isoformat() if event.start_time else None,
                    'end_time': event.end_time.isoformat() if event.end_time else None,
                    'is_all_day': event.is_all_day,
                    'attendees': event.attendees,
                    'organizer': event.organizer,
                    'status': event.status,
                    'recurrence': event.recurrence,
                    'reminders': event.reminders,
                    'provider': self.config.provider
                }
        
        return None
    
    def get_upcoming_events(
        self,
        days: int = 7,
        limit: int = 10
    ) -> List[CalendarEvent]:
        """
        Get upcoming events for the next N days.
        
        Args:
            days: Number of days to look ahead (default: 7)
            limit: Maximum number of events to return
        
        Returns:
            List of CalendarEvent objects
        """
        now = datetime.now()
        date_to = now + timedelta(days=days)
        
        # Search with empty query to get all events in range
        events = self.search_events(
            "",
            limit=limit,
            filters={
                'date_from': now.strftime('%Y-%m-%d'),
                'date_to': date_to.strftime('%Y-%m-%d')
            }
        )
        
        return events
    
    def get_events_by_date(
        self,
        date: datetime,
        limit: int = 50
    ) -> List[CalendarEvent]:
        """
        Get all events for a specific date.
        
        Args:
            date: The date to get events for
            limit: Maximum number of events
        
        Returns:
            List of CalendarEvent objects
        """
        date_start = datetime.combine(date.date(), datetime.min.time())
        date_end = datetime.combine(date.date(), datetime.max.time())
        
        events = self.search_events(
            "",
            limit=limit,
            filters={
                'date_from': date_start.strftime('%Y-%m-%d %H:%M:%S'),
                'date_to': date_end.strftime('%Y-%m-%d %H:%M:%S')
            }
        )
        
        return events
