/**
 * Documents Component
 * Version: 1.2.0
 * 
 * Provides document management interface with CRUD operations.
 */

class DocumentsComponent {
  constructor(container) {
    this.container = container;
    this.state = {
      documents: [],
      total: 0,
      limit: 20,
      offset: 0,
      category: '',
      loading: false,
      error: null,
      editingDoc: null,
    };
    
    this.init();
  }
  
  init() {
    this.render();
    this.attachEventListeners();
    this.loadDocuments();
  }
  
  render() {
    this.container.innerHTML = `
      <div class="documents-container">
        <div class="documents-toolbar">
          <div class="documents-filters">
            <input 
              type="text" 
              class="filter-input" 
              id="categoryFilter"
              placeholder="Filter by category..."
              value="${this.state.category}"
            />
            <select class="filter-input" id="limitFilter">
              <option value="10" ${this.state.limit === 10 ? 'selected' : ''}>10 per page</option>
              <option value="20" ${this.state.limit === 20 ? 'selected' : ''}>20 per page</option>
              <option value="50" ${this.state.limit === 50 ? 'selected' : ''}>50 per page</option>
              <option value="100" ${this.state.limit === 100 ? 'selected' : ''}>100 per page</option>
            </select>
          </div>
          
          <button class="btn btn-primary" id="createDocBtn">
            ✚ New Document
          </button>
        </div>
        
        <div class="documents-list" id="documentsList">
          ${this.renderDocumentsList()}
        </div>
        
        ${this.renderPagination()}
      </div>
    `;
  }
  
  renderDocumentsList() {
    if (this.state.loading) {
      return `
        <div class="loading">
          <div class="spinner"></div>
          <div class="loading-text">Loading documents...</div>
        </div>
      `;
    }
    
    if (this.state.error) {
      return `
        <div class="empty-state">
          <div class="empty-icon">⚠️</div>
          <div class="empty-title">Error Loading Documents</div>
          <div class="empty-description">${this.escapeHtml(this.state.error)}</div>
          <button class="btn btn-primary mt-lg" onclick="window.documentsComponent.loadDocuments()">
            Retry
          </button>
        </div>
      `;
    }
    
    if (this.state.documents.length === 0) {
      return `
        <div class="empty-state">
          <div class="empty-icon">📄</div>
          <div class="empty-title">No Documents Yet</div>
          <div class="empty-description">
            Create your first document to start building your knowledge base.
          </div>
          <button class="btn btn-primary mt-lg" onclick="window.documentsComponent.openEditor()">
            Create Document
          </button>
        </div>
      `;
    }
    
    return this.state.documents.map(doc => this.renderDocumentCard(doc)).join('');
  }
  
  renderDocumentCard(doc) {
    const createdDate = new Date(doc.created_at).toLocaleString();
    const updatedDate = doc.updated_at ? new Date(doc.updated_at).toLocaleString() : null;
    const contentPreview = doc.content.length > 300 
      ? doc.content.substring(0, 300) + '...' 
      : doc.content;
    
    return `
      <div class="document-card" data-doc-id="${doc.id}">
        <div class="document-header">
          <span class="document-id">${doc.id}</span>
          <div class="document-actions">
            <button 
              class="btn btn-ghost btn-sm" 
              onclick="window.documentsComponent.editDocument('${doc.id}')"
              title="Edit"
            >
              ✏️
            </button>
            <button 
              class="btn btn-ghost btn-sm" 
              onclick="window.documentsComponent.viewDocument('${doc.id}')"
              title="View"
            >
              👁️
            </button>
            <button 
              class="btn btn-ghost btn-sm text-error" 
              onclick="window.documentsComponent.confirmDelete('${doc.id}')"
              title="Delete"
            >
              🗑️
            </button>
          </div>
        </div>
        
        <div class="document-content">
          ${this.escapeHtml(contentPreview)}
        </div>
        
        <div class="document-meta">
          <div class="meta-item">
            📅 Created: ${createdDate}
          </div>
          ${updatedDate ? `
            <div class="meta-item">
              ✏️ Updated: ${updatedDate}
            </div>
          ` : ''}
          ${doc.metadata.category ? `
            <div class="meta-item">
              📁 ${this.escapeHtml(doc.metadata.category)}
            </div>
          ` : ''}
          ${doc.metadata.source ? `
            <div class="meta-item">
              📄 ${this.escapeHtml(doc.metadata.source)}
            </div>
          ` : ''}
          <div class="meta-item">
            📊 Chunks: ${doc.chunk_count}
          </div>
        </div>
      </div>
    `;
  }
  
  renderPagination() {
    const totalPages = Math.ceil(this.state.total / this.state.limit);
    const currentPage = Math.floor(this.state.offset / this.state.limit) + 1;
    
    if (totalPages <= 1) {
      return '';
    }
    
    const pages = this.getVisiblePages(currentPage, totalPages);
    
    return `
      <div class="pagination" id="documentsPagination">
        <button 
          class="pagination-btn" 
          onclick="window.documentsComponent.previousPage()"
          ${currentPage === 1 ? 'disabled' : ''}
        >
          ← Prev
        </button>
        
        ${pages.map(page => {
          if (page === '...') {
            return '<span class="pagination-ellipsis">...</span>';
          }
          return `
            <button 
              class="pagination-btn ${page === currentPage ? 'active' : ''}"
              onclick="window.documentsComponent.goToPage(${page})"
            >
              ${page}
            </button>
          `;
        }).join('')}
        
        <button 
          class="pagination-btn" 
          onclick="window.documentsComponent.nextPage()"
          ${currentPage === totalPages ? 'disabled' : ''}
        >
          Next →
        </button>
      </div>
    `;
  }
  
  getVisiblePages(current, total) {
    if (total <= 7) {
      return Array.from({ length: total }, (_, i) => i + 1);
    }
    
    if (current <= 3) {
      return [1, 2, 3, 4, 5, '...', total];
    }
    
    if (current >= total - 2) {
      return [1, '...', total - 4, total - 3, total - 2, total - 1, total];
    }
    
    return [1, '...', current - 1, current, current + 1, '...', total];
  }
  
  attachEventListeners() {
    const createBtn = this.container.querySelector('#createDocBtn');
    const categoryFilter = this.container.querySelector('#categoryFilter');
    const limitFilter = this.container.querySelector('#limitFilter');
    
    createBtn.addEventListener('click', () => this.openEditor());
    
    categoryFilter.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        this.state.category = e.target.value.trim();
        this.state.offset = 0;
        this.loadDocuments();
      }
    });
    
    limitFilter.addEventListener('change', (e) => {
      this.state.limit = parseInt(e.target.value);
      this.state.offset = 0;
      this.loadDocuments();
    });
  }
  
  async loadDocuments() {
    this.state.loading = true;
    this.state.error = null;
    this.updateDocumentsList();
    
    try {
      const response = await window.KAApi.Documents.list({
        limit: this.state.limit,
        offset: this.state.offset,
        category: this.state.category || undefined,
      });
      
      this.state.documents = response.documents;
      this.state.total = response.total;
      
    } catch (error) {
      console.error('Failed to load documents:', error);
      this.state.error = error.message || 'Failed to load documents';
    } finally {
      this.state.loading = false;
      this.updateDocumentsList();
    }
  }
  
  updateDocumentsList() {
    const listContainer = this.container.querySelector('#documentsList');
    if (listContainer) {
      listContainer.innerHTML = this.renderDocumentsList();
    }
    
    // Update pagination
    const paginationContainer = this.container.querySelector('#documentsPagination');
    if (paginationContainer) {
      paginationContainer.outerHTML = this.renderPagination();
    }
  }
  
  async goToPage(page) {
    this.state.offset = (page - 1) * this.state.limit;
    await this.loadDocuments();
  }
  
  async previousPage() {
    const currentPage = Math.floor(this.state.offset / this.state.limit) + 1;
    if (currentPage > 1) {
      await this.goToPage(currentPage - 1);
    }
  }
  
  async nextPage() {
    const currentPage = Math.floor(this.state.offset / this.state.limit) + 1;
    const totalPages = Math.ceil(this.state.total / this.state.limit);
    if (currentPage < totalPages) {
      await this.goToPage(currentPage + 1);
    }
  }
  
  openEditor(doc = null) {
    this.state.editingDoc = doc;
    
    const modal = document.createElement('div');
    modal.className = 'document-editor';
    modal.id = 'documentEditorModal';
    
    const isEdit = !!doc;
    const title = isEdit ? `Edit Document: ${doc.id}` : 'Create New Document';
    const content = doc ? doc.content : '';
    const category = doc && doc.metadata.category ? doc.metadata.category : '';
    const source = doc && doc.metadata.source ? doc.metadata.source : '';
    const author = doc && doc.metadata.author ? doc.metadata.author : '';
    
    modal.innerHTML = `
      <div class="editor-modal">
        <div class="editor-header">
          <h3 class="editor-title">${title}</h3>
          <button class="editor-close" onclick="window.documentsComponent.closeEditor()">
            ✕
          </button>
        </div>
        
        <div class="editor-body">
          <div class="form-group">
            <label class="form-label">Content *</label>
            <textarea 
              class="form-input" 
              id="docContent" 
              rows="10"
              placeholder="Enter document content..."
            >${this.escapeHtml(content)}</textarea>
          </div>
          
          <div class="form-group">
            <label class="form-label">Category</label>
            <input 
              type="text" 
              class="form-input" 
              id="docCategory"
              placeholder="e.g., programming, documentation, notes"
              value="${this.escapeHtml(category)}"
            />
          </div>
          
          <div class="form-group">
            <label class="form-label">Source</label>
            <input 
              type="text" 
              class="form-input" 
              id="docSource"
              placeholder="e.g., manual.md, guide.txt"
              value="${this.escapeHtml(source)}"
            />
          </div>
          
          <div class="form-group">
            <label class="form-label">Author</label>
            <input 
              type="text" 
              class="form-input" 
              id="docAuthor"
              placeholder="e.g., AI Team"
              value="${this.escapeHtml(author)}"
            />
          </div>
        </div>
        
        <div class="editor-footer">
          <button class="btn btn-secondary" onclick="window.documentsComponent.closeEditor()">
            Cancel
          </button>
          <button class="btn btn-primary" onclick="window.documentsComponent.saveDocument()">
            ${isEdit ? 'Update' : 'Create'}
          </button>
        </div>
      </div>
    `;
    
    document.body.appendChild(modal);
    
    // Close on backdrop click
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        this.closeEditor();
      }
    });
  }
  
  closeEditor() {
    const modal = document.getElementById('documentEditorModal');
    if (modal) {
      modal.remove();
    }
    this.state.editingDoc = null;
  }
  
  async saveDocument() {
    const content = document.getElementById('docContent').value.trim();
    const category = document.getElementById('docCategory').value.trim();
    const source = document.getElementById('docSource').value.trim();
    const author = document.getElementById('docAuthor').value.trim();
    
    if (!content) {
      this.showToast('Content is required', 'error');
      return;
    }
    
    const metadata = {};
    if (category) metadata.category = category;
    if (source) metadata.source = source;
    if (author) metadata.author = author;
    
    try {
      if (this.state.editingDoc) {
        // Update existing document
        await window.KAApi.Documents.update(this.state.editingDoc.id, {
          content,
          metadata: Object.keys(metadata).length > 0 ? metadata : undefined,
        });
        this.showToast('Document updated successfully', 'success');
      } else {
        // Create new document
        await window.KAApi.Documents.create({
          content,
          metadata,
        });
        this.showToast('Document created successfully', 'success');
      }
      
      this.closeEditor();
      await this.loadDocuments();
      
    } catch (error) {
      console.error('Failed to save document:', error);
      this.showToast(error.message || 'Failed to save document', 'error');
    }
  }
  
  async viewDocument(docId) {
    try {
      const doc = await window.KAApi.Documents.get(docId);
      this.openEditor(doc);
      
      // Make read-only
      setTimeout(() => {
        const contentInput = document.getElementById('docContent');
        if (contentInput) {
          contentInput.readOnly = true;
        }
      }, 0);
      
    } catch (error) {
      console.error('Failed to view document:', error);
      this.showToast(error.message || 'Failed to load document', 'error');
    }
  }
  
  async editDocument(docId) {
    try {
      const doc = await window.KAApi.Documents.get(docId);
      this.openEditor(doc);
    } catch (error) {
      console.error('Failed to edit document:', error);
      this.showToast(error.message || 'Failed to load document', 'error');
    }
  }
  
  confirmDelete(docId) {
    const modal = document.createElement('div');
    modal.className = 'document-editor';
    modal.innerHTML = `
      <div class="editor-modal" style="max-width: 500px;">
        <div class="editor-header">
          <h3 class="editor-title">Confirm Delete</h3>
          <button class="editor-close" onclick="this.closest('.document-editor').remove()">
            ✕
          </button>
        </div>
        
        <div class="editor-body">
          <p>Are you sure you want to delete document <strong>${docId}</strong>?</p>
          <p class="text-sm text-muted mt-md">This action cannot be undone. The document will be removed from the knowledge base.</p>
        </div>
        
        <div class="editor-footer">
          <button class="btn btn-secondary" onclick="this.closest('.document-editor').remove()">
            Cancel
          </button>
          <button class="btn btn-danger" onclick="window.documentsComponent.deleteDocument('${docId}')">
            Delete
          </button>
        </div>
      </div>
    `;
    
    document.body.appendChild(modal);
    
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        modal.remove();
      }
    });
  }
  
  async deleteDocument(docId) {
    try {
      await window.KAApi.Documents.delete(docId);
      this.showToast('Document deleted successfully', 'success');
      
      // Close confirmation modal
      const modals = document.querySelectorAll('.document-editor');
      modals.forEach(modal => modal.remove());
      
      await this.loadDocuments();
      
    } catch (error) {
      console.error('Failed to delete document:', error);
      this.showToast(error.message || 'Failed to delete document', 'error');
    }
  }
  
  showToast(message, type = 'info') {
    // Use global toast function if available
    if (window.showToast) {
      window.showToast(message, type);
    } else {
      alert(message);
    }
  }
  
  escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
}

// Export globally
window.DocumentsComponent = DocumentsComponent;
