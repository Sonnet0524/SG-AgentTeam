"""
Notes connector implementation supporting Apple Notes and Notion.

Provides functionality to connect to note-taking applications, search notes,
and retrieve note content.

Implements TASK-C3: Notes Connector (Issue #39)
"""

import json
import subprocess
import platform
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path
import logging
import re

from .base import BaseConnector, ConnectorConfig, SearchResult
from .config import BaseConnectorConfig

logger = logging.getLogger(__name__)

# Type checking imports
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    logger.debug("requests not installed, Notion API support disabled")


@dataclass
class NotesConfig(BaseConnectorConfig):
    """Configuration for notes connector.
    
    Attributes:
        provider: Notes provider ('apple', 'notion', or 'mock')
        notion_token: Notion API integration token
        notion_database_id: Notion database ID to search
        apple_notes_account: Apple Notes account name (optional)
        max_results: Maximum number of notes to return
    """
    
    provider: str = "mock"
    notion_token: str = ""
    notion_database_id: str = ""
    apple_notes_account: str = ""
    max_results: int = 50


@dataclass
class Note:
    """Represents a note.
    
    Attributes:
        id: Unique note identifier
        title: Note title
        content: Note content/text
        folder: Folder/collection the note belongs to
        tags: List of tags
        created_time: Note creation time
        modified_time: Note last modification time
        source: Source application
        url: URL to open the note (if applicable)
        metadata: Additional provider-specific metadata
    """
    
    id: str
    title: str
    content: str = ""
    folder: str = ""
    tags: List[str] = field(default_factory=list)
    created_time: Optional[datetime] = None
    modified_time: Optional[datetime] = None
    source: str = ""
    url: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


class NotesConnector(BaseConnector):
    """
    Notes connector supporting multiple providers.
    
    Provides a unified interface for accessing notes from:
    - Apple Notes (macOS only, via AppleScript)
    - Notion (via Notion API)
    - Mock notes (for testing)
    
    Attributes:
        config: NotesConfig instance
        _notes_cache: Cache for loaded notes
    
    Example:
        >>> # Notion
        >>> config = NotesConfig(
        ...     provider="notion",
        ...     notion_token="secret_xxx",
        ...     notion_database_id="xxx"
        ... )
        >>> connector = NotesConnector(config=config)
        >>> 
        >>> with NotesConnector(config=config) as conn:
        ...     notes = connector.search_notes("project", limit=10)
        ...     for note in notes:
        ...         print(f"{note.title}: {note.content[:100]}")
        >>> 
        >>> # Apple Notes
        >>> config = NotesConfig(provider="apple")
        >>> connector = NotesConnector(config=config)
        >>> if connector.connect():
        ...     notes = connector.search_notes("meeting")
        ...     connector.disconnect()
    """
    
    def __init__(self, config: Optional[NotesConfig] = None):
        """
        Initialize the notes connector.
        
        Args:
            config: NotesConfig instance
        """
        if config is None:
            config = NotesConfig()
        super().__init__(config)
        self.config: NotesConfig = config
        self._notes_cache: List[Note] = []
    
    def connect(self) -> bool:
        """
        Establish connection to the notes provider.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        self._clear_error()
        
        try:
            if self.config.provider == "apple":
                return self._connect_apple()
            elif self.config.provider == "notion":
                return self._connect_notion()
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
        self._notes_cache = []
        self._on_disconnect()
        return True
    
    def is_connected(self) -> bool:
        """
        Check if the connection is active.
        
        Returns:
            bool: True if connected
        """
        if self.config.provider == "apple":
            return platform.system() == "Darwin"  # macOS
        elif self.config.provider == "notion":
            return len(self._notes_cache) > 0 or bool(self.config.notion_token)
        elif self.config.provider == "mock":
            return self._connected
        return False
    
    def _connect_apple(self) -> bool:
        """Connect to Apple Notes via AppleScript."""
        if platform.system() != "Darwin":
            self._set_error("Apple Notes is only available on macOS")
            return False
        
        # Test if we can access Apple Notes
        try:
            result = subprocess.run(
                ['osascript', '-e', 'tell application "Notes" to get name of every note'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                self._set_error(f"Failed to access Apple Notes: {result.stderr}")
                return False
            
            self._on_connect_success()
            return True
        except subprocess.TimeoutExpired:
            self._set_error("Apple Notes access timeout")
            return False
        except Exception as e:
            self._set_error(f"Apple Notes connection failed: {e}")
            return False
    
    def _connect_notion(self) -> bool:
        """Connect to Notion API."""
        if not HAS_REQUESTS:
            self._set_error("requests library not installed. Install with: pip install requests")
            return False
        
        if not self.config.notion_token:
            self._set_error("Notion API token not specified")
            return False
        
        # Test connection by fetching database
        if self.config.notion_database_id:
            try:
                headers = {
                    "Authorization": f"Bearer {self.config.notion_token}",
                    "Notion-Version": "2022-06-28",
                    "Content-Type": "application/json"
                }
                
                response = requests.post(
                    f"https://api.notion.com/v1/databases/{self.config.notion_database_id}/query",
                    headers=headers,
                    json={"page_size": 1},
                    timeout=10
                )
                
                if response.status_code == 200:
                    self._on_connect_success()
                    return True
                elif response.status_code == 401:
                    self._set_error("Invalid Notion API token")
                    return False
                elif response.status_code == 404:
                    self._set_error("Notion database not found")
                    return False
                else:
                    self._set_error(f"Notion API error: {response.status_code}")
                    return False
            except Exception as e:
                self._set_error(f"Notion connection failed: {e}")
                return False
        else:
            # No database ID, but token is valid
            self._on_connect_success()
            return True
    
    def _connect_mock(self) -> bool:
        """Connect to mock notes (for testing)."""
        # Create some mock notes
        self._notes_cache = [
            Note(
                id="mock_1",
                title="Project Planning",
                content="This is a comprehensive project planning document.\n\nKey milestones:\n- Phase 1: Research\n- Phase 2: Development\n- Phase 3: Testing\n\nBudget: $50,000",
                folder="Work",
                tags=["project", "planning", "important"],
                created_time=datetime.now() - timedelta(days=7),
                modified_time=datetime.now() - timedelta(days=1)
            ),
            Note(
                id="mock_2",
                title="Meeting Notes - Q1 Review",
                content="Quarterly review meeting notes.\n\nAttendees: Alice, Bob, Charlie\n\nDiscussion points:\n1. Revenue exceeded targets\n2. Customer satisfaction up 15%\n3. New product launch planned for Q2",
                folder="Meetings",
                tags=["meeting", "review", "quarterly"],
                created_time=datetime.now() - timedelta(days=3),
                modified_time=datetime.now() - timedelta(days=3)
            ),
            Note(
                id="mock_3",
                title="Personal Goals 2026",
                content="My personal goals for 2026:\n\n1. Learn a new programming language\n2. Exercise 3 times a week\n3. Read 24 books\n4. Travel to 2 new countries\n5. Save 20% of income",
                folder="Personal",
                tags=["goals", "personal", "2026"],
                created_time=datetime.now() - timedelta(days=30),
                modified_time=datetime.now() - timedelta(days=5)
            ),
            Note(
                id="mock_4",
                title="Recipe: Homemade Pasta",
                content="Simple homemade pasta recipe:\n\nIngredients:\n- 2 cups flour\n- 3 eggs\n- 1 tsp salt\n\nInstructions:\n1. Mix flour and salt\n2. Add eggs and knead\n3. Rest for 30 minutes\n4. Roll and cut\n5. Cook for 2-3 minutes",
                folder="Recipes",
                tags=["cooking", "recipe", "pasta"],
                created_time=datetime.now() - timedelta(days=14),
                modified_time=datetime.now() - timedelta(days=14)
            ),
            Note(
                id="mock_5",
                title="Book Notes: Atomic Habits",
                content="Key takeaways from 'Atomic Habits' by James Clear:\n\n1. Habits are the compound interest of self-improvement\n2. Focus on systems, not goals\n3. Make it obvious, attractive, easy, and satisfying\n4. The 4 Laws of Behavior Change\n5. Identity-based habits",
                folder="Books",
                tags=["books", "habits", "self-improvement"],
                created_time=datetime.now() - timedelta(days=60),
                modified_time=datetime.now() - timedelta(days=10)
            )
        ]
        self._on_connect_success()
        return True
    
    def search(
        self,
        query: str,
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> List[SearchResult]:
        """
        Search for notes matching the query.
        
        Args:
            query: Search query (keywords)
            limit: Maximum number of results
            filters: Optional filters:
                - folder: Filter by folder name
                - tag: Filter by tag
                - modified_after: Filter by modification date
            **kwargs: Additional parameters
        
        Returns:
            List of SearchResult objects
        """
        # Use search_notes method for backward compatibility
        notes = self.search_notes(query, limit=limit, filters=filters, **kwargs)
        
        # Convert to SearchResult
        results = []
        for note in notes:
            result = SearchResult(
                id=note.id,
                title=note.title,
                snippet=note.content[:200] if note.content else "",
                source='notes',
                metadata={
                    'folder': note.folder,
                    'tags': note.tags,
                    'created_time': note.created_time.isoformat() if note.created_time else None,
                    'modified_time': note.modified_time.isoformat() if note.modified_time else None,
                    'source_app': note.source,
                    'url': note.url,
                    'provider': self.config.provider
                },
                timestamp=note.modified_time or note.created_time
            )
            results.append(result)
        
        return results
    
    def search_notes(
        self,
        query: str,
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> List[Note]:
        """
        Search for notes matching the query.
        
        Args:
            query: Search query (keywords)
            limit: Maximum number of results
            filters: Optional filters
            **kwargs: Additional parameters
        
        Returns:
            List of Note objects
        
        Example:
            >>> notes = connector.search_notes("project", limit=5)
        """
        if not self.is_connected():
            self._set_error("Not connected to notes provider")
            return []
        
        self._clear_error()
        
        try:
            if self.config.provider == "apple":
                return self._search_apple_notes(query, limit, filters)
            elif self.config.provider == "notion":
                return self._search_notion_notes(query, limit, filters)
            elif self.config.provider == "mock":
                return self._search_local_notes(query, limit, filters)
            else:
                return []
        except Exception as e:
            self._set_error(f"Search failed: {e}")
            return []
    
    def _search_apple_notes(
        self,
        query: str,
        limit: int,
        filters: Optional[Dict[str, Any]]
    ) -> List[Note]:
        """Search Apple Notes via AppleScript."""
        notes = []
        
        try:
            # Build AppleScript to search notes
            script = f'''
            tell application "Notes"
                set matchingNotes to {{}}
                set allNotes to every note
                repeat with eachNote in allNotes
                    set noteName to name of eachNote
                    set noteBody to body of eachNote
                    if noteName contains "{query}" or noteBody contains "{query}" then
                        set end of matchingNotes to {{noteName, noteBody, id of eachNote, modification date of eachNote, creation date of eachNote}}
                    end if
                end repeat
                return matchingNotes
            end tell
            '''
            
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                logger.warning(f"Apple Notes search failed: {result.stderr}")
                return []
            
            # Parse AppleScript result
            # Format: noteName, noteBody, id, modificationDate, creationDate
            # This is a simplified parser; real implementation needs more robust parsing
            lines = result.stdout.strip().split(', ')
            
            # For now, return empty list as parsing is complex
            # Real implementation would properly parse the AppleScript output
            logger.info(f"Apple Notes search returned data (parsing not implemented)")
            
        except subprocess.TimeoutExpired:
            logger.error("Apple Notes search timeout")
        except Exception as e:
            logger.error(f"Apple Notes search error: {e}")
        
        return notes
    
    def _search_notion_notes(
        self,
        query: str,
        limit: int,
        filters: Optional[Dict[str, Any]]
    ) -> List[Note]:
        """Search Notion pages via API."""
        if not HAS_REQUESTS or not self.config.notion_token:
            return []
        
        notes = []
        
        try:
            headers = {
                "Authorization": f"Bearer {self.config.notion_token}",
                "Notion-Version": "2022-06-28",
                "Content-Type": "application/json"
            }
            
            # Search query
            search_params = {
                "query": query,
                "page_size": min(limit, self.config.max_results)
            }
            
            # If database ID is specified, filter by it
            if self.config.notion_database_id:
                search_params["filter"] = {
                    "property": "object",
                    "value": "page"
                }
            
            response = requests.post(
                "https://api.notion.com/v1/search",
                headers=headers,
                json=search_params,
                timeout=30
            )
            
            if response.status_code != 200:
                logger.error(f"Notion search failed: {response.status_code}")
                return []
            
            data = response.json()
            
            # Parse results
            for item in data.get('results', []):
                note = self._parse_notion_page(item)
                if note:
                    # Apply additional filters
                    if filters and not self._matches_filters(note, filters):
                        continue
                    notes.append(note)
        
        except Exception as e:
            logger.error(f"Notion search error: {e}")
        
        return notes
    
    def _parse_notion_page(self, page: Dict[str, Any]) -> Optional[Note]:
        """Parse a Notion page into a Note object."""
        try:
            page_id = page.get('id', '')
            
            # Extract title from properties
            properties = page.get('properties', {})
            title = "Untitled"
            
            # Try to find title property
            for prop_name, prop_data in properties.items():
                if prop_data.get('type') == 'title':
                    title_list = prop_data.get('title', [])
                    if title_list:
                        title = title_list[0].get('plain_text', 'Untitled')
                    break
            
            # Get content (simplified - would need to fetch blocks for full content)
            content = ""
            
            # Extract timestamps
            created_time = None
            modified_time = None
            
            if 'created_time' in page:
                created_time = datetime.fromisoformat(page['created_time'].replace('Z', '+00:00'))
            
            if 'last_edited_time' in page:
                modified_time = datetime.fromisoformat(page['last_edited_time'].replace('Z', '+00:00'))
            
            # Extract tags/properties
            tags = []
            for prop_name, prop_data in properties.items():
                if prop_data.get('type') == 'multi_select':
                    for option in prop_data.get('multi_select', []):
                        tags.append(option.get('name', ''))
                elif prop_data.get('type') == 'select':
                    if prop_data.get('select'):
                        tags.append(prop_data['select'].get('name', ''))
            
            # Build URL
            url = page.get('url', '')
            
            return Note(
                id=page_id,
                title=title,
                content=content,
                tags=tags,
                created_time=created_time,
                modified_time=modified_time,
                source="Notion",
                url=url,
                metadata=page
            )
        except Exception as e:
            logger.warning(f"Failed to parse Notion page: {e}")
            return None
    
    def _search_local_notes(
        self,
        query: str,
        limit: int,
        filters: Optional[Dict[str, Any]]
    ) -> List[Note]:
        """Search local notes (mock)."""
        query_lower = query.lower()
        matching_notes = []
        
        for note in self._notes_cache:
            # Check if query matches title or content
            if (query_lower in note.title.lower() or
                query_lower in note.content.lower() or
                any(query_lower in tag.lower() for tag in note.tags)):
                
                # Apply filters
                if filters and not self._matches_filters(note, filters):
                    continue
                
                matching_notes.append(note)
        
        # Sort by modification time (newest first)
        matching_notes.sort(
            key=lambda n: n.modified_time or datetime.min,
            reverse=True
        )
        
        return matching_notes[:limit]
    
    def _matches_filters(self, note: Note, filters: Dict[str, Any]) -> bool:
        """Check if note matches all filters."""
        # Folder filter
        if 'folder' in filters:
            if filters['folder'].lower() not in note.folder.lower():
                return False
        
        # Tag filter
        if 'tag' in filters:
            if filters['tag'] not in note.tags:
                return False
        
        # Modified after filter
        if 'modified_after' in filters:
            filter_date = self._parse_datetime(filters['modified_after'])
            if filter_date and note.modified_time:
                if note.modified_time < filter_date:
                    return False
        
        return True
    
    def _parse_datetime(self, value: Any) -> Optional[datetime]:
        """Parse datetime from various formats."""
        if isinstance(value, datetime):
            return value
        
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value.replace('Z', '+00:00'))
            except:
                pass
            
            try:
                return datetime.strptime(value, '%Y-%m-%d')
            except:
                pass
        
        return None
    
    def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific note by its ID.
        
        Args:
            id: Note identifier
        
        Returns:
            Dict containing note details, or None if not found
        """
        if not self.is_connected():
            self._set_error("Not connected to notes provider")
            return None
        
        self._clear_error()
        
        try:
            if self.config.provider == "apple":
                return self._get_apple_note_by_id(id)
            elif self.config.provider == "notion":
                return self._get_notion_note_by_id(id)
            elif self.config.provider == "mock":
                return self._get_local_note_by_id(id)
            else:
                return None
        except Exception as e:
            self._set_error(f"Failed to retrieve note: {e}")
            return None
    
    def _get_apple_note_by_id(self, note_id: str) -> Optional[Dict[str, Any]]:
        """Get an Apple Note by ID."""
        # Implementation would use AppleScript
        logger.warning("Apple Notes get_by_id not fully implemented")
        return None
    
    def _get_notion_note_by_id(self, page_id: str) -> Optional[Dict[str, Any]]:
        """Get a Notion page by ID."""
        if not HAS_REQUESTS or not self.config.notion_token:
            return None
        
        try:
            headers = {
                "Authorization": f"Bearer {self.config.notion_token}",
                "Notion-Version": "2022-06-28",
                "Content-Type": "application/json"
            }
            
            # Get page
            response = requests.get(
                f"https://api.notion.com/v1/pages/{page_id}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                page = response.json()
                note = self._parse_notion_page(page)
                
                if note:
                    # Fetch content blocks
                    blocks_response = requests.get(
                        f"https://api.notion.com/v1/blocks/{page_id}/children",
                        headers=headers,
                        timeout=10
                    )
                    
                    if blocks_response.status_code == 200:
                        blocks = blocks_response.json().get('results', [])
                        content_parts = []
                        
                        for block in blocks:
                            block_type = block.get('type', '')
                            if block_type in block:
                                text_content = block[block_type]
                                if isinstance(text_content, dict) and 'rich_text' in text_content:
                                    for text_item in text_content['rich_text']:
                                        content_parts.append(text_item.get('plain_text', ''))
                        
                        note.content = '\n'.join(content_parts)
                    
                    return {
                        'id': note.id,
                        'title': note.title,
                        'content': note.content,
                        'folder': note.folder,
                        'tags': note.tags,
                        'created_time': note.created_time.isoformat() if note.created_time else None,
                        'modified_time': note.modified_time.isoformat() if note.modified_time else None,
                        'source': note.source,
                        'url': note.url,
                        'provider': 'notion'
                    }
            elif response.status_code == 404:
                return None
            else:
                self._set_error(f"Notion API error: {response.status_code}")
        
        except Exception as e:
            self._set_error(f"Notion API error: {e}")
        
        return None
    
    def _get_local_note_by_id(self, note_id: str) -> Optional[Dict[str, Any]]:
        """Get a local note by ID."""
        for note in self._notes_cache:
            if note.id == note_id:
                return {
                    'id': note.id,
                    'title': note.title,
                    'content': note.content,
                    'folder': note.folder,
                    'tags': note.tags,
                    'created_time': note.created_time.isoformat() if note.created_time else None,
                    'modified_time': note.modified_time.isoformat() if note.modified_time else None,
                    'source': note.source,
                    'url': note.url,
                    'provider': self.config.provider
                }
        
        return None
    
    def get_recent_notes(
        self,
        days: int = 7,
        limit: int = 10
    ) -> List[Note]:
        """
        Get recently modified notes.
        
        Args:
            days: Number of days to look back (default: 7)
            limit: Maximum number of notes to return
        
        Returns:
            List of Note objects
        """
        cutoff = datetime.now() - timedelta(days=days)
        
        notes = self.search_notes(
            "",
            limit=limit,
            filters={'modified_after': cutoff.strftime('%Y-%m-%d')}
        )
        
        return notes
    
    def get_notes_by_tag(
        self,
        tag: str,
        limit: int = 50
    ) -> List[Note]:
        """
        Get all notes with a specific tag.
        
        Args:
            tag: Tag to search for
            limit: Maximum number of notes
        
        Returns:
            List of Note objects
        """
        notes = self.search_notes(
            "",
            limit=limit,
            filters={'tag': tag}
        )
        
        return notes


# Import timedelta at module level
from datetime import timedelta
