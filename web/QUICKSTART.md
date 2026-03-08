# Quick Start Guide - Knowledge Assistant Web UI

## 🚀 Start the Application

### Option 1: One-Command Start (Recommended)

```bash
cd web
./start.sh
```

This will:
- Start the API server on port 8000
- Start the Web UI on port 3000
- Open your browser automatically (if supported)

### Option 2: Manual Start

```bash
# Terminal 1: Start API server
python3 scripts/api/main.py

# Terminal 2: Start Web UI
cd web
python3 -m http.server 3000
```

Then open: http://localhost:3000

---

## 📱 Features Overview

### 🔍 Search Tab

1. **Enter Search Query**: Type your question or keywords
2. **Adjust Filters**:
   - Results per page (5, 10, 20, 50)
   - Minimum similarity threshold
3. **View Results**: Click any result for details
4. **Navigate**: Use pagination for more results

**Example Searches**:
- "Python async programming"
- "API documentation"
- "Configuration guide"

### 📄 Documents Tab

1. **View Documents**: Browse all documents in the knowledge base
2. **Filter by Category**: Type category name and press Enter
3. **Create Document**: Click "New Document" button
4. **Edit Document**: Click ✏️ icon on any document
5. **Delete Document**: Click 🗑️ icon (with confirmation)

### 🔌 Connectors Tab

1. **View Status**: See all connector statuses at a glance
2. **Connect Email**: Click "Connect" and enter IMAP settings
3. **View Details**: Click "Details" for connector info
4. **Auto-Refresh**: Status updates every 30 seconds

---

## 📧 Email Connector Setup

To connect your email:

1. Click "Connect" on the Email connector card
2. Enter your IMAP settings:
   - **Server**: `imap.gmail.com` (for Gmail)
   - **Port**: `993`
   - **Username**: Your email address
   - **Password**: Your password or app password
   - **SSL**: Checked (recommended)

3. Click "Connect"

**Note for Gmail**: You may need to use an App Password instead of your regular password.

---

## 🔧 Configuration

### Environment Variables

```bash
# API Server
export KA_API_HOST=0.0.0.0
export KA_API_PORT=8000

# Web UI Server
export KA_WEB_PORT=3000

# Index Path
export KA_INDEX_PATH=.ka-index
```

### Build an Index First

If you see "Index not found" warning:

```bash
# Index your documents
python3 scripts/index/build_index.py --source ./my-docs --index .ka-index

# Then start the servers
cd web
./start.sh
```

---

## 🎨 UI Features

### Responsive Design
- Works on desktop, tablet, and mobile
- Dark mode support (follows system preference)

### Keyboard Shortcuts
- **Enter** in search box: Execute search
- **Enter** in category filter: Apply filter
- **Esc**: Close modals

### Error Handling
- Network errors show retry buttons
- API errors display detailed messages
- Toast notifications for feedback

---

## 🐛 Troubleshooting

### "Failed to connect to API"
- Ensure API server is running on port 8000
- Check console for CORS errors
- Verify `scripts/api/main.py` works

### "Index not found"
- Build an index first: `python3 scripts/index/build_index.py --source <docs>`
- Or set `KA_INDEX_PATH` to your index directory

### "No documents found"
- Create some documents in the Documents tab
- Or index existing documents

### Web UI not loading
- Clear browser cache
- Check browser console for errors
- Ensure JavaScript is enabled

---

## 📊 Browser Support

| Browser | Version |
|---------|---------|
| Chrome | 80+ |
| Firefox | 75+ |
| Safari | 13+ |
| Edge | 80+ |

---

## 🔗 Useful Links

When running locally:
- **Web UI**: http://localhost:3000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## 📝 Tips

1. **Start with a small test index** to verify everything works
2. **Use the API docs** (`/docs`) to understand available endpoints
3. **Check the browser console** (F12) if something isn't working
4. **Documents are stored in** `.ka-documents/metadata.json`

---

**Need help?** Check the main README or create an issue on GitHub.
