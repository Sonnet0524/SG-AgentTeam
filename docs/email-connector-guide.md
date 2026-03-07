# Email Connector Guide

This guide explains how to use the Email Connector to search and retrieve emails via IMAP.

## Overview

The Email Connector provides a standardized interface for connecting to email servers and searching emails. It's designed to work with any IMAP-compatible email service (Gmail, Outlook, Yahoo, etc.).

## Installation

No additional packages are required. The connector uses Python's built-in `imaplib` and `email` modules.

## Quick Start

### Basic Usage

```python
from scripts.connectors.email import EmailConnector, EmailConfig

# Configure the connector
config = EmailConfig(
    server="imap.gmail.com",
    port=993,
    username="your_email@gmail.com",
    password="your_app_password"  # Use app password for Gmail
)

# Create and connect
connector = EmailConnector(config=config)

if connector.connect():
    # Search for emails
    results = connector.search("project budget", limit=5)
    
    for result in results:
        print(f"Subject: {result.title}")
        print(f"From: {result.metadata['sender']}")
        print(f"Snippet: {result.snippet}")
        print("---")
    
    # Disconnect when done
    connector.disconnect()
```

### Using Context Manager

```python
from scripts.connectors.email import EmailConnector, EmailConfig

config = EmailConfig(
    server="imap.gmail.com",
    username="your_email@gmail.com",
    password="your_app_password"
)

# Automatically connects and disconnects
with EmailConnector(config=config) as connector:
    results = connector.search("important")
    # ... process results
# Auto-disconnects here
```

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| server | str | "" | IMAP server hostname |
| port | int | 993 | IMAP port (993 for SSL) |
| username | str | "" | Email address/username |
| password | str | "" | Password or app password |
| default_folder | str | "INBOX" | Default folder to search |
| max_search_results | int | 50 | Maximum search results |
| snippet_length | int | 200 | Snippet preview length |
| use_ssl | bool | True | Use SSL connection |
| timeout | int | 30 | Connection timeout (seconds) |

## Common Email Providers

### Gmail

```python
config = EmailConfig(
    server="imap.gmail.com",
    port=993,
    username="your_email@gmail.com",
    password="your_app_password"  # Requires App Password
)
```

**Note**: Gmail requires App Passwords for IMAP access. Enable 2FA and create an App Password at https://myaccount.google.com/apppasswords

### Outlook/Office 365

```python
config = EmailConfig(
    server="outlook.office365.com",
    port=993,
    username="your_email@outlook.com",
    password="your_password"
)
```

### Yahoo

```python
config = EmailConfig(
    server="imap.mail.yahoo.com",
    port=993,
    username="your_email@yahoo.com",
    password="your_app_password"
)
```

## Search Features

### Basic Search

```python
results = connector.search("budget report")
```

### Search with Filters

```python
results = connector.search(
    "project update",
    limit=10,
    filters={
        'date_from': '2024-01-01',
        'date_to': '2024-12-31',
        'sender': 'boss@company.com',
        'unread_only': True
    }
)
```

### Search Multiple Folders

```python
results = connector.search(
    "important",
    folders=["INBOX", "Sent", "Archive"]
)
```

## Retrieve Full Email

```python
# Get full email content by ID
email_data = connector.get_by_id("123")

if email_data:
    print(f"Subject: {email_data['subject']}")
    print(f"From: {email_data['sender']}")
    print(f"To: {email_data['recipients']}")
    print(f"Body:\n{email_data['body_text']}")
    print(f"Attachments: {len(email_data['attachments'])}")
```

## Get Recent Emails

```python
# Get the 10 most recent emails
recent = connector.get_recent_emails(folder="INBOX", count=10)

for email in recent:
    print(f"{email.date}: {email.subject}")
```

## List Folders

```python
folders = connector.list_folders()
print("Available folders:", folders)
```

## Error Handling

```python
connector = EmailConnector(config=config)

if not connector.connect():
    error = connector.get_last_error()
    print(f"Connection failed: {error}")
    return

results = connector.search("query")

if not results:
    error = connector.get_last_error()
    if error:
        print(f"Search failed: {error}")
```

## Integration with opencode

The Email Connector is designed to integrate with opencode through the Skill system:

```python
# In opencode's skill implementation
from scripts.connectors.email import EmailConnector

def search_emails(query: str) -> list:
    """
    Skill function for opencode to search emails.
    
    Args:
        query: Search query from user
        
    Returns:
        List of email results for opencode to display
    """
    config = EmailConfig(
        server=get_config('email.server'),
        username=get_config('email.username'),
        password=get_config('email.password')
    )
    
    with EmailConnector(config=config) as connector:
        results = connector.search(query)
        
        # Return structured data for opencode
        return [
            {
                'type': 'email_result',
                'id': r.id,
                'title': r.title,
                'snippet': r.snippet,
                'metadata': r.metadata
            }
            for r in results
        ]
```

## Security Best Practices

1. **Use App Passwords**: Never use your main email password. Use app-specific passwords.

2. **Environment Variables**: Store credentials securely:
   ```python
   import os
   
   config = EmailConfig(
       server=os.environ.get('EMAIL_SERVER'),
       username=os.environ.get('EMAIL_USERNAME'),
       password=os.environ.get('EMAIL_PASSWORD')
   )
   ```

3. **OAuth2 (Future)**: For production, consider implementing OAuth2 authentication instead of passwords.

4. **Connection Timeout**: Set appropriate timeout to prevent hanging:
   ```python
   config = EmailConfig(
       ...,
       timeout=30  # seconds
   )
   ```

## Performance Notes

- **Search Speed**: Typical search completes in 1-3 seconds
- **Batch Operations**: Fetching multiple emails is more efficient than single fetches
- **Connection Reuse**: Keep connection open for multiple operations

## Troubleshooting

### Connection Failed

1. Verify IMAP is enabled in your email account settings
2. Check server address and port
3. For Gmail, ensure App Password is used (not regular password)
4. Check firewall/network restrictions

### Search Returns No Results

1. Try simpler search terms
2. Check folder name is correct
3. Verify emails exist in the searched folder

### Authentication Errors

1. Double-check username and password
2. For Gmail: Ensure 2FA is enabled and App Password is created
3. For Office 365: May require modern authentication (OAuth2)

## API Reference

### EmailConnector Methods

| Method | Description |
|--------|-------------|
| `connect()` | Establish connection to IMAP server |
| `disconnect()` | Close the connection |
| `is_connected()` | Check connection status |
| `search(query, limit, filters, folders)` | Search for emails |
| `get_by_id(id)` | Retrieve full email by ID |
| `list_folders()` | List available folders |
| `get_recent_emails(folder, count)` | Get recent emails |
| `get_last_error()` | Get last error message |

### SearchResult Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | str | Email message ID |
| `title` | str | Email subject |
| `snippet` | str | Content preview |
| `source` | str | Always "email" |
| `metadata` | dict | Additional info (sender, folder, etc.) |
| `timestamp` | datetime | Email date |

---

**Author**: Integration Team  
**Version**: 1.0  
**Last Updated**: 2026-03-07
