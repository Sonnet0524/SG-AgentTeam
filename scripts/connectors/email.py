"""
Email connector implementation using IMAP protocol.

Provides functionality to connect to email servers, search emails,
and retrieve email content.

Implements TASK-INT1: Email Connector
"""

import imaplib
import email as email_lib
from email.header import decode_header
from email.utils import parseaddr, parsedate_to_datetime, getaddresses
from email.message import Message
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import logging
import re

from .base import BaseConnector, ConnectorConfig, SearchResult

logger = logging.getLogger(__name__)


@dataclass
class EmailConfig(ConnectorConfig):
    """Configuration for email connector."""
    
    # Server settings
    server: str = ""
    port: int = 993  # IMAP SSL port
    username: str = ""
    password: str = ""
    
    # Email-specific settings
    default_folder: str = "INBOX"
    max_search_results: int = 50
    snippet_length: int = 200
    
    # Security
    use_ssl: bool = True


@dataclass
class EmailSummary:
    """Summary information for an email."""
    
    id: str                           # Email message ID
    subject: str                      # Email subject
    sender: str                       # Sender email address
    sender_name: str = ""             # Sender display name
    date: Optional[datetime] = None   # Date sent
    snippet: str = ""                 # Preview of content
    folder: str = "INBOX"             # Folder containing the email
    is_read: bool = False             # Read status
    has_attachments: bool = False     # Attachment flag
    flags: List[str] = field(default_factory=list)  # IMAP flags


@dataclass
class EmailContent:
    """Full content of an email."""
    
    id: str                           # Email message ID
    subject: str                      # Email subject
    sender: str                       # Sender email
    sender_name: str = ""             # Sender display name
    recipients: List[str] = field(default_factory=list)  # To/Cc recipients
    date: Optional[datetime] = None   # Date sent
    body_text: str = ""               # Plain text body
    body_html: str = ""               # HTML body (if available)
    attachments: List[Dict] = field(default_factory=list)  # Attachment info
    headers: Dict[str, str] = field(default_factory=dict)  # All headers
    folder: str = "INBOX"


class EmailConnector(BaseConnector):
    """
    Email connector using IMAP protocol.
    
    Connects to email servers via IMAP to search and retrieve emails.
    Supports searching by keywords, date ranges, and folders.
    
    Attributes:
        config: EmailConfig instance
        _client: IMAP client connection
    
    Example:
        >>> # Connect and search emails
        >>> config = EmailConfig(
        ...     server="imap.gmail.com",
        ...     username="user@gmail.com",
        ...     password="app_password"
        ... )
        >>> connector = EmailConnector(config=config)
        >>> 
        >>> # Using context manager (auto connect/disconnect)
        >>> with EmailConnector(config=config) as conn:
        ...     results = conn.search("project budget", limit=10)
        ...     for result in results:
        ...         print(f"{result.title} from {result.metadata['sender']}")
        ...         
        >>> # Or manual connection
        >>> if connector.connect():
        ...     results = connector.search("project budget")
        ...     connector.disconnect()
    
    Security Notes:
        - Passwords are not stored; use app-specific passwords when possible
        - SSL/TLS is enabled by default
        - Consider using OAuth2 for production use
    
    Performance:
        - Search typically completes in 1-3 seconds
        - Retrieving full content may take longer for large emails
        - Batch operations are more efficient than single retrievals
    """
    
    def __init__(self, config: Optional[EmailConfig] = None):
        """
        Initialize the email connector.
        
        Args:
            config: EmailConfig instance. Required fields:
                - server: IMAP server hostname
                - username: Email username/address
                - password: Email password or app password
        """
        if config is None:
            config = EmailConfig()
        super().__init__(config)
        self.config: EmailConfig = config
        self._client: Optional[imaplib.IMAP4_SSL] = None
        self._current_folder: Optional[str] = None
    
    def connect(self) -> bool:
        """
        Establish connection to the IMAP server.
        
        Returns:
            bool: True if connection successful, False otherwise
        
        Raises:
            ValueError: If required configuration is missing
        """
        self._clear_error()
        
        # Validate configuration
        if not self.config.server:
            self._set_error("Server address is required")
            return False
        
        if not self.config.username or not self.config.password:
            self._set_error("Username and password are required")
            return False
        
        try:
            logger.info(f"Connecting to {self.config.server}:{self.config.port}")
            
            # Create IMAP connection
            if self.config.use_ssl:
                self._client = imaplib.IMAP4_SSL(
                    self.config.server,
                    self.config.port,
                    timeout=self.config.timeout
                )
            else:
                self._client = imaplib.IMAP4(
                    self.config.server,
                    self.config.port,
                    timeout=self.config.timeout
                )
            
            # Authenticate
            self._client.login(self.config.username, self.config.password)
            self._connected = True
            
            logger.info(f"Successfully connected to {self.config.server}")
            return True
            
        except imaplib.IMAP4.error as e:
            self._set_error(f"IMAP authentication failed: {e}")
            self._connected = False
            return False
        except Exception as e:
            self._set_error(f"Connection failed: {e}")
            self._connected = False
            return False
    
    def disconnect(self) -> bool:
        """
        Close the IMAP connection.
        
        Returns:
            bool: True if disconnection successful
        """
        try:
            if self._client and self._connected:
                # Close selected folder
                try:
                    self._client.close()
                except:
                    pass
                
                # Logout
                self._client.logout()
                logger.info("Disconnected from email server")
            
            self._client = None
            self._connected = False
            self._current_folder = None
            return True
            
        except Exception as e:
            logger.warning(f"Error during disconnect: {e}")
            self._connected = False
            return True  # Still return True to allow cleanup
    
    def is_connected(self) -> bool:
        """
        Check if the IMAP connection is active.
        
        Returns:
            bool: True if connected, False otherwise
        """
        if not self._connected or not self._client:
            return False
        
        try:
            # Try a NOOP command to check connection
            self._client.noop()
            return True
        except:
            self._connected = False
            return False
    
    def _select_folder(self, folder: str) -> bool:
        """
        Select an IMAP folder for operations.
        
        Args:
            folder: Folder name (e.g., "INBOX", "Sent", "Drafts")
        
        Returns:
            bool: True if folder selected successfully
        """
        if not self._connected or not self._client:
            self._set_error("Not connected to server")
            return False
        
        if self._current_folder == folder:
            return True
        
        try:
            status, data = self._client.select(folder)
            if status == 'OK':
                self._current_folder = folder
                return True
            else:
                self._set_error(f"Failed to select folder: {folder}")
                return False
        except Exception as e:
            self._set_error(f"Error selecting folder: {e}")
            return False
    
    def search(
        self,
        query: str,
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        folders: Optional[List[str]] = None,
        **kwargs
    ) -> List[SearchResult]:
        """
        Search for emails matching the query.
        
        Args:
            query: Search query (keywords or phrases)
            limit: Maximum number of results (default: 10)
            filters: Optional filters:
                - date_from: Start date (datetime or str "YYYY-MM-DD")
                - date_to: End date (datetime or str "YYYY-MM-DD")
                - sender: Filter by sender email
                - unread_only: Only return unread emails
            folders: List of folders to search (default: ["INBOX"])
            **kwargs: Additional parameters (ignored)
        
        Returns:
            List of SearchResult objects for matching emails
        
        Example:
            >>> results = connector.search(
            ...     "project budget",
            ...     limit=5,
            ...     filters={'date_from': '2024-01-01'},
            ...     folders=["INBOX", "Sent"]
            ... )
        """
        if not self._connected or not self._client:
            self._set_error("Not connected to server")
            return []
        
        if not query or not query.strip():
            logger.warning("Empty search query")
            return []
        
        self._clear_error()
        folders = folders or [self.config.default_folder]
        all_results = []
        
        for folder in folders:
            if not self._select_folder(folder):
                continue
            
            # Build IMAP search criteria
            criteria = self._build_search_criteria(query, filters)
            
            try:
                # Search for matching messages
                status, message_ids = self._client.search(None, *criteria)
                
                if status != 'OK':
                    logger.warning(f"Search failed in folder {folder}")
                    continue
                
                # Get message IDs
                ids = message_ids[0].split()
                
                # Limit results per folder
                ids = ids[-limit:] if len(ids) > limit else ids
                
                # Fetch summaries for each message
                for msg_id in ids:
                    try:
                        summary = self._fetch_email_summary(msg_id, folder)
                        if summary:
                            all_results.append(self._summary_to_search_result(summary))
                    except Exception as e:
                        logger.warning(f"Error fetching email {msg_id}: {e}")
                
            except Exception as e:
                self._set_error(f"Search error in {folder}: {e}")
                continue
        
        # Sort by date (newest first)
        all_results.sort(
            key=lambda r: r.timestamp or datetime.min,
            reverse=True
        )
        
        return all_results[:limit]
    
    def _build_search_criteria(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """
        Build IMAP search criteria from query and filters.
        
        Args:
            query: Search query
            filters: Optional filters
        
        Returns:
            List of IMAP search criteria strings
        """
        criteria = []
        
        # Add query terms (OR all terms)
        terms = query.split()
        if len(terms) == 1:
            criteria.extend(['SUBJECT', terms[0]])
        else:
            # For multiple terms, search in subject or body
            for term in terms:
                criteria.extend(['OR', 'SUBJECT', term, 'BODY', term])
        
        # Add filters
        if filters:
            # Date range
            if 'date_from' in filters:
                date_from = filters['date_from']
                if isinstance(date_from, datetime):
                    date_str = date_from.strftime('%d-%b-%Y')
                else:
                    date_str = datetime.strptime(date_from, '%Y-%m-%d').strftime('%d-%b-%Y')
                criteria.extend(['SINCE', date_str])
            
            if 'date_to' in filters:
                date_to = filters['date_to']
                if isinstance(date_to, datetime):
                    date_str = date_to.strftime('%d-%b-%Y')
                else:
                    date_str = datetime.strptime(date_to, '%Y-%m-%d').strftime('%d-%b-%Y')
                criteria.extend(['BEFORE', date_str])
            
            # Sender filter
            if 'sender' in filters:
                criteria.extend(['FROM', filters['sender']])
            
            # Unread only
            if filters.get('unread_only'):
                criteria.append('UNSEEN')
        
        # If no criteria, match all
        if not criteria:
            criteria = ['ALL']
        
        return criteria
    
    def _fetch_email_summary(
        self,
        msg_id: bytes,
        folder: str
    ) -> Optional[EmailSummary]:
        """
        Fetch summary information for an email.
        
        Args:
            msg_id: IMAP message ID
            folder: Folder name
        
        Returns:
            EmailSummary or None if fetch fails
        """
        if not self._client:
            return None
        
        try:
            # Fetch headers and flags
            status, data = self._client.fetch(
                msg_id,
                '(FLAGS BODY.PEEK[HEADER])'
            )
            
            if status != 'OK':
                return None
            
            # Parse the response
            response = data[0]
            flags = []
            raw_headers = b''
            
            if isinstance(response, tuple):
                flags_str = response[0].decode()
                raw_headers = response[1]
                # Extract flags
                if '\\Seen' in flags_str:
                    flags.append('seen')
                if '\\Flagged' in flags_str:
                    flags.append('flagged')
                if '\\Answered' in flags_str:
                    flags.append('answered')
            else:
                raw_headers = response
            
            # Parse email headers
            msg = email_lib.message_from_bytes(raw_headers)
            
            # Decode subject
            subject = self._decode_header(msg.get('Subject', '(No Subject)'))
            
            # Parse sender
            sender_name, sender_email = parseaddr(msg.get('From', ''))
            
            # Parse date
            date_str = msg.get('Date', '')
            date = None
            if date_str:
                try:
                    date = parsedate_to_datetime(date_str)
                except:
                    pass
            
            # Check for attachments
            has_attachments = self._check_attachments(msg)
            
            # Fetch snippet from body
            snippet = self._fetch_snippet(msg_id)
            
            return EmailSummary(
                id=msg_id.decode(),
                subject=subject,
                sender=sender_email,
                sender_name=sender_name,
                date=date,
                snippet=snippet[:self.config.snippet_length],
                folder=folder,
                is_read='seen' in flags,
                has_attachments=has_attachments,
                flags=flags
            )
            
        except Exception as e:
            logger.error(f"Error fetching email summary: {e}")
            return None
    
    def _fetch_snippet(self, msg_id: bytes) -> str:
        """
        Fetch a text snippet from the email body.
        
        Args:
            msg_id: IMAP message ID
        
        Returns:
            str: Text snippet
        """
        if not self._client:
            return ""
        
        try:
            status, data = self._client.fetch(
                msg_id,
                '(BODY.PEEK[TEXT])'
            )
            
            if status != 'OK':
                return ""
            
            body = data[0][1] if isinstance(data[0], tuple) else data[0]
            
            # Try to decode
            try:
                text = body.decode('utf-8', errors='ignore')
            except:
                text = body.decode('latin-1', errors='ignore')
            
            # Clean HTML tags if present
            text = re.sub(r'<[^>]+>', '', text)
            # Normalize whitespace
            text = ' '.join(text.split())
            
            return text
            
        except Exception as e:
            logger.warning(f"Error fetching snippet: {e}")
            return ""
    
    def _check_attachments(self, msg: Message) -> bool:
        """Check if email has attachments."""
        for part in msg.walk():
            if part.get_content_disposition() == 'attachment':
                return True
        return False
    
    def _decode_header(self, header: str) -> str:
        """Decode an email header with proper encoding."""
        if not header:
            return ""
        
        decoded_parts = []
        for part, charset in decode_header(header):
            if isinstance(part, bytes):
                charset = charset or 'utf-8'
                try:
                    decoded_parts.append(part.decode(charset, errors='ignore'))
                except:
                    decoded_parts.append(part.decode('utf-8', errors='ignore'))
            else:
                decoded_parts.append(str(part))
        
        return ' '.join(decoded_parts)
    
    def _summary_to_search_result(self, summary: EmailSummary) -> SearchResult:
        """Convert EmailSummary to SearchResult."""
        return SearchResult(
            id=summary.id,
            title=summary.subject,
            snippet=summary.snippet,
            source='email',
            metadata={
                'sender': summary.sender,
                'sender_name': summary.sender_name,
                'folder': summary.folder,
                'is_read': summary.is_read,
                'has_attachments': summary.has_attachments,
                'flags': summary.flags
            },
            timestamp=summary.date
        )
    
    def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve the full content of an email by its ID.
        
        Args:
            id: Email message ID
        
        Returns:
            Dict containing the full email content, or None if not found
        
        Example:
            >>> email = connector.get_by_id("123")
            >>> if email:
            ...     print(f"Subject: {email['subject']}")
            ...     print(f"Body: {email['body_text'][:100]}...")
        """
        if not self._connected or not self._client:
            self._set_error("Not connected to server")
            return None
        
        self._clear_error()
        
        try:
            # Fetch the full email
            status, data = self._client.fetch(id.encode(), '(RFC822)')
            
            if status != 'OK':
                self._set_error(f"Failed to fetch email {id}")
                return None
            
            # Parse the email
            raw_email = data[0][1] if isinstance(data[0], tuple) else data[0]
            msg = email_lib.message_from_bytes(raw_email)
            
            # Extract body text and HTML
            body_text = ""
            body_html = ""
            attachments = []
            
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get('Content-Disposition', ''))
                
                if 'attachment' in content_disposition:
                    # Handle attachment
                    filename = part.get_filename()
                    if filename:
                        attachments.append({
                            'filename': self._decode_header(filename),
                            'content_type': content_type,
                            'size': len(part.get_payload(decode=True) or b'')
                        })
                elif content_type == 'text/plain' and not body_text:
                    payload = part.get_payload(decode=True)
                    if payload:
                        charset = part.get_content_charset() or 'utf-8'
                        body_text = payload.decode(charset, errors='ignore')
                elif content_type == 'text/html' and not body_html:
                    payload = part.get_payload(decode=True)
                    if payload:
                        charset = part.get_content_charset() or 'utf-8'
                        body_html = payload.decode(charset, errors='ignore')
            
            # Extract recipients
            recipients = []
            for header in ['To', 'Cc', 'Bcc']:
                value = msg.get(header, '')
                if value:
                    for name, addr in getaddresses([value]):
                        if addr:
                            recipients.append(addr)
            
            # Extract headers
            headers = {}
            for key in msg.keys():
                headers[key] = self._decode_header(msg.get(key, ''))
            
            # Parse date
            date_str = msg.get('Date', '')
            date = None
            if date_str:
                try:
                    date = parsedate_to_datetime(date_str)
                except:
                    pass
            
            return {
                'id': id,
                'subject': self._decode_header(msg.get('Subject', '')),
                'sender': parseaddr(msg.get('From', ''))[1],
                'sender_name': parseaddr(msg.get('From', ''))[0],
                'recipients': recipients,
                'date': date,
                'body_text': body_text,
                'body_html': body_html,
                'attachments': attachments,
                'headers': headers,
                'folder': self._current_folder or 'INBOX'
            }
            
        except Exception as e:
            self._set_error(f"Error retrieving email: {e}")
            return None
    
    def list_folders(self) -> List[str]:
        """
        List all available folders/mailboxes.
        
        Returns:
            List of folder names
        """
        if not self._connected or not self._client:
            self._set_error("Not connected to server")
            return []
        
        try:
            status, folders = self._client.list()
            if status != 'OK':
                return []
            
            folder_names = []
            for folder in folders:
                if folder:
                    # Parse folder name from IMAP LIST response
                    parts = folder.decode().split('"')
                    if len(parts) >= 3:
                        folder_names.append(parts[-2])
            
            return folder_names
            
        except Exception as e:
            self._set_error(f"Error listing folders: {e}")
            return []
    
    def get_recent_emails(
        self,
        folder: str = "INBOX",
        count: int = 10
    ) -> List[EmailSummary]:
        """
        Get the most recent emails from a folder.
        
        Args:
            folder: Folder name (default: "INBOX")
            count: Number of recent emails to retrieve
        
        Returns:
            List of EmailSummary objects
        """
        if not self._connected or not self._client:
            self._set_error("Not connected to server")
            return []
        
        if not self._select_folder(folder):
            return []
        
        try:
            # Search for all messages
            status, message_ids = self._client.search(None, 'ALL')
            
            if status != 'OK':
                return []
            
            ids = message_ids[0].split()
            # Get the most recent ones
            ids = ids[-count:] if len(ids) > count else ids
            
            summaries = []
            for msg_id in reversed(ids):  # Newest first
                summary = self._fetch_email_summary(msg_id, folder)
                if summary:
                    summaries.append(summary)
            
            return summaries
            
        except Exception as e:
            self._set_error(f"Error getting recent emails: {e}")
            return []
