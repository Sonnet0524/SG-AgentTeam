# Knowledge Assistant Web UI

A modern, responsive web interface for the Knowledge Assistant application.

## Features

### 🔍 Semantic Search
- Natural language search queries
- Real-time results with similarity scores
- Result highlighting and pagination
- Filter by similarity threshold

### 📄 Document Management
- Create, read, update, delete documents
- Document metadata management
- Category filtering
- Pagination support

### 🔌 Connectors Dashboard
- Monitor connector status
- Connect/disconnect connectors
- View connector details
- Auto-refresh status

## Quick Start

### Option 1: Using the startup script (Recommended)

```bash
cd web
./start.sh
```

This will start both the API server and the web UI server.

### Option 2: Manual startup

1. Start the API server:
```bash
python3 scripts/api/main.py
```

2. In a new terminal, start the web server:
```bash
cd web
python3 -m http.server 3000
```

3. Open your browser to: `http://localhost:3000`

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `KA_API_HOST` | `0.0.0.0` | API server host |
| `KA_API_PORT` | `8000` | API server port |
| `KA_WEB_PORT` | `3000` | Web UI server port |
| `KA_INDEX_PATH` | `.ka-index` | Path to the index directory |

### API Endpoints

The Web UI interacts with the following API endpoints:

#### Search
- `GET /api/search` - Semantic search
- `POST /api/search` - Advanced search with filters

#### Documents
- `GET /api/documents` - List documents
- `POST /api/documents` - Create document
- `GET /api/documents/{id}` - Get document
- `PUT /api/documents/{id}` - Update document
- `DELETE /api/documents/{id}` - Delete document

#### Connectors
- `GET /api/connectors/status` - Get all connector statuses
- `GET /api/connectors/{name}/status` - Get specific connector status
- `POST /api/connectors/connect` - Connect a connector
- `POST /api/connectors/disconnect` - Disconnect a connector

## Architecture

### Technology Stack
- **Frontend**: Vanilla JavaScript (ES6+)
- **Styling**: Modern CSS with CSS Variables
- **API Client**: Fetch API
- **Backend**: FastAPI (Python)

### File Structure

```
web/
├── index.html          # Main HTML file
├── start.sh            # Startup script
├── css/
│   └── style.css       # Complete stylesheet
├── js/
│   ├── api.js          # API client
│   ├── app.js          # Main application
│   └── components/
│       ├── search.js       # Search component
│       ├── documents.js    # Documents component
│       └── connectors.js   # Connectors component
└── assets/             # Static assets
```

### Design Principles

1. **No Framework Dependencies**: Built with vanilla JavaScript for simplicity and performance
2. **Responsive Design**: Works on desktop, tablet, and mobile
3. **Progressive Enhancement**: Core functionality works without JavaScript
4. **Dark Mode Ready**: CSS variables support dark mode (follows system preference)
5. **Accessible**: Semantic HTML and ARIA attributes

## Browser Support

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## Development

### Making Changes

1. Edit the source files in `web/` directory
2. Refresh browser to see changes (no build step required)

### Debugging

- Open browser developer tools (F12)
- Check the Console tab for errors
- Check the Network tab for API requests

### API Mocking

For development without a backend, you can mock API responses:

```javascript
// In browser console
window.KAApi.Search.search = async () => ({
  results: [
    {
      rank: 1,
      similarity: 0.95,
      snippet: "This is a mock search result",
      metadata: { source: "test.md" },
      index: 0
    }
  ],
  total: 1,
  limit: 10,
  offset: 0,
  query_time_ms: 42
});
```

## Performance

### Optimization Tips

1. **Enable Gzip**: Configure your web server to compress responses
2. **Cache Static Assets**: Use browser caching for CSS and JS files
3. **Lazy Load Components**: Components are only loaded when needed
4. **Minimize API Calls**: Use pagination and filters to reduce data transfer

### Bundle Size

- Total JavaScript: ~50KB (uncompressed)
- Total CSS: ~24KB (uncompressed)
- No external dependencies

## Troubleshooting

### CORS Errors

If you see CORS errors, ensure the API server is running and CORS is configured in `scripts/api/main.py`.

### Index Not Found

If you see "Index not found" warning:
1. Build an index first: `python3 scripts/index/build_index.py --source <your-docs-dir>`
2. Or set `KA_INDEX_PATH` to point to your index directory

### API Connection Failed

If the web UI can't connect to the API:
1. Check if the API server is running: `curl http://localhost:8000/health`
2. Check if the correct port is configured
3. Check browser console for errors

## Future Enhancements

Potential improvements for future versions:

- [ ] Real-time updates with WebSockets
- [ ] Advanced search filters UI
- [ ] Document upload and indexing
- [ ] User authentication
- [ ] Saved searches and bookmarks
- [ ] Export and import functionality
- [ ] Batch operations
- [ ] Keyboard shortcuts
- [ ] Offline support with Service Workers

## License

This project is part of the Knowledge Assistant application.

---

**Version**: 1.2.0  
**Last Updated**: 2026-03-08
