/**
 * Search Component
 * Version: 1.2.0
 * 
 * Provides semantic search interface with results display and pagination.
 */

class SearchComponent {
  constructor(container) {
    this.container = container;
    this.state = {
      query: '',
      results: [],
      total: 0,
      limit: 10,
      offset: 0,
      queryTime: 0,
      loading: false,
      error: null,
      options: {
        threshold: null,
        index_path: '.ka-index',
      },
    };
    
    this.init();
  }
  
  init() {
    this.render();
    this.attachEventListeners();
  }
  
  render() {
    this.container.innerHTML = `
      <div class="search-container">
        <div class="search-box">
          <div class="search-input-wrapper">
            <span class="search-icon">🔍</span>
            <input 
              type="text" 
              class="search-input" 
              id="searchQueryInput"
              placeholder="Enter your search query..."
              value="${this.state.query}"
              autocomplete="off"
            />
          </div>
          <button class="btn btn-primary search-btn" id="searchBtn">
            Search
          </button>
        </div>
        
        <div class="search-options">
          <div class="search-option">
            <label for="limitInput">Results per page:</label>
            <select class="filter-input" id="limitInput">
              <option value="5" ${this.state.limit === 5 ? 'selected' : ''}>5</option>
              <option value="10" ${this.state.limit === 10 ? 'selected' : ''}>10</option>
              <option value="20" ${this.state.limit === 20 ? 'selected' : ''}>20</option>
              <option value="50" ${this.state.limit === 50 ? 'selected' : ''}>50</option>
            </select>
          </div>
          
          <div class="search-option">
            <label for="thresholdInput">
              Min similarity: <span id="thresholdValue">${this.state.options.threshold || 'Any'}</span>
            </label>
            <input 
              type="range" 
              class="form-input" 
              id="thresholdInput"
              min="0" 
              max="1" 
              step="0.1" 
              value="${this.state.options.threshold || 0}"
              style="width: 120px;"
            />
          </div>
        </div>
      </div>
      
      <div class="search-results" id="searchResults">
        ${this.renderResults()}
      </div>
    `;
  }
  
  renderResults() {
    if (this.state.loading) {
      return `
        <div class="loading">
          <div class="spinner"></div>
          <div class="loading-text">Searching...</div>
        </div>
      `;
    }
    
    if (this.state.error) {
      return `
        <div class="empty-state">
          <div class="empty-icon">⚠️</div>
          <div class="empty-title">Search Error</div>
          <div class="empty-description">${this.escapeHtml(this.state.error)}</div>
          <button class="btn btn-primary mt-lg" onclick="window.searchComponent.clearError()">
            Try Again
          </button>
        </div>
      `;
    }
    
    if (!this.state.query && this.state.results.length === 0) {
      return `
        <div class="empty-state">
          <div class="empty-icon">🔍</div>
          <div class="empty-title">Start Searching</div>
          <div class="empty-description">
            Enter a search query to find documents in your knowledge base.
          </div>
        </div>
      `;
    }
    
    if (this.state.results.length === 0) {
      return `
        <div class="empty-state">
          <div class="empty-icon">📭</div>
          <div class="empty-title">No Results Found</div>
          <div class="empty-description">
            No documents match your search query. Try different keywords or adjust your filters.
          </div>
        </div>
      `;
    }
    
    return `
      <div class="results-header">
        <div class="results-count">
          Found <strong>${this.state.total}</strong> results for 
          "<em>${this.escapeHtml(this.state.query)}</em>"
        </div>
        <div class="results-time">
          ${this.state.queryTime.toFixed(2)}ms
        </div>
      </div>
      
      <div class="results-list">
        ${this.state.results.map((result, index) => this.renderResultItem(result, index)).join('')}
      </div>
      
      ${this.renderPagination()}
    `;
  }
  
  renderResultItem(result, index) {
    const similarityPercent = Math.round(result.similarity * 100);
    const snippet = this.escapeHtml(result.snippet);
    
    // Highlight query terms in snippet (simple implementation)
    const highlightedSnippet = this.highlightTerms(snippet, this.state.query);
    
    return `
      <div class="result-item" onclick="window.searchComponent.showResultDetail(${index})">
        <div class="result-header">
          <div class="result-rank">${result.rank}</div>
          <div class="result-score">
            ${similarityPercent}% match
          </div>
        </div>
        
        <div class="result-content">
          <div class="result-snippet">${highlightedSnippet}</div>
        </div>
        
        <div class="result-metadata">
          ${result.metadata.source ? `
            <span class="metadata-tag">
              📄 ${this.escapeHtml(result.metadata.source)}
            </span>
          ` : ''}
          ${result.metadata.category ? `
            <span class="metadata-tag">
              📁 ${this.escapeHtml(result.metadata.category)}
            </span>
          ` : ''}
          ${result.metadata.author ? `
            <span class="metadata-tag">
              👤 ${this.escapeHtml(result.metadata.author)}
            </span>
          ` : ''}
          <span class="metadata-tag">
            🔢 Chunk ${result.index}
          </span>
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
      <div class="pagination">
        <button 
          class="pagination-btn" 
          onclick="window.searchComponent.previousPage()"
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
              onclick="window.searchComponent.goToPage(${page})"
            >
              ${page}
            </button>
          `;
        }).join('')}
        
        <button 
          class="pagination-btn" 
          onclick="window.searchComponent.nextPage()"
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
    const searchInput = this.container.querySelector('#searchQueryInput');
    const searchBtn = this.container.querySelector('#searchBtn');
    const limitInput = this.container.querySelector('#limitInput');
    const thresholdInput = this.container.querySelector('#thresholdInput');
    const thresholdValue = this.container.querySelector('#thresholdValue');
    
    // Search on Enter key
    searchInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        this.handleSearch();
      }
    });
    
    // Search button click
    searchBtn.addEventListener('click', () => this.handleSearch());
    
    // Limit change
    limitInput.addEventListener('change', (e) => {
      this.state.limit = parseInt(e.target.value);
      if (this.state.query) {
        this.handleSearch();
      }
    });
    
    // Threshold change
    thresholdInput.addEventListener('input', (e) => {
      const value = parseFloat(e.target.value);
      this.state.options.threshold = value > 0 ? value : null;
      thresholdValue.textContent = this.state.options.threshold 
        ? `${Math.round(this.state.options.threshold * 100)}%` 
        : 'Any';
    });
  }
  
  async handleSearch() {
    const query = this.container.querySelector('#searchQueryInput').value.trim();
    
    if (!query) {
      this.showError('Please enter a search query');
      return;
    }
    
    this.state.query = query;
    this.state.offset = 0;
    this.state.loading = true;
    this.state.error = null;
    this.updateResults();
    
    try {
      const response = await window.KAApi.Search.search({
        q: query,
        limit: this.state.limit,
        offset: this.state.offset,
        threshold: this.state.options.threshold,
        index_path: this.state.options.index_path,
      });
      
      this.state.results = response.results;
      this.state.total = response.total;
      this.state.queryTime = response.query_time_ms;
      
    } catch (error) {
      console.error('Search failed:', error);
      this.showError(error.message || 'Search failed. Please try again.');
    } finally {
      this.state.loading = false;
      this.updateResults();
    }
  }
  
  async goToPage(page) {
    this.state.offset = (page - 1) * this.state.limit;
    await this.handleSearch();
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
  
  updateResults() {
    const resultsContainer = this.container.querySelector('#searchResults');
    if (resultsContainer) {
      resultsContainer.innerHTML = this.renderResults();
    }
  }
  
  showError(message) {
    this.state.error = message;
    this.updateResults();
  }
  
  clearError() {
    this.state.error = null;
    this.updateResults();
  }
  
  showResultDetail(index) {
    const result = this.state.results[index];
    if (!result) return;
    
    // Create modal to show full result details
    const modal = document.createElement('div');
    modal.className = 'document-editor';
    modal.innerHTML = `
      <div class="editor-modal" style="max-width: 600px;">
        <div class="editor-header">
          <h3 class="editor-title">Search Result #${result.rank}</h3>
          <button class="editor-close" onclick="this.closest('.document-editor').remove()">
            ✕
          </button>
        </div>
        <div class="editor-body">
          <div class="mb-md">
            <div class="text-sm text-muted mb-sm">Similarity Score</div>
            <div class="text-lg text-success">${Math.round(result.similarity * 100)}%</div>
          </div>
          
          <div class="mb-md">
            <div class="text-sm text-muted mb-sm">Snippet</div>
            <div class="result-snippet">${this.escapeHtml(result.snippet)}</div>
          </div>
          
          <div class="mb-md">
            <div class="text-sm text-muted mb-sm">Metadata</div>
            <pre style="background: var(--color-bg-secondary); padding: var(--spacing-md); border-radius: var(--radius-sm); overflow-x: auto; font-size: var(--font-sm);">
${JSON.stringify(result.metadata, null, 2)}
            </pre>
          </div>
          
          <div>
            <div class="text-sm text-muted mb-sm">Chunk Index</div>
            <div>${result.index}</div>
          </div>
        </div>
        <div class="editor-footer">
          <button class="btn btn-secondary" onclick="this.closest('.document-editor').remove()">
            Close
          </button>
        </div>
      </div>
    `;
    
    document.body.appendChild(modal);
    
    // Close on backdrop click
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        modal.remove();
      }
    });
  }
  
  highlightTerms(text, query) {
    if (!query) return text;
    
    const terms = query.toLowerCase().split(/\s+/);
    let result = text;
    
    terms.forEach(term => {
      if (term.length > 2) {
        const regex = new RegExp(`(${this.escapeRegex(term)})`, 'gi');
        result = result.replace(regex, '<mark style="background: #fef08a; padding: 0 2px; border-radius: 2px;">$1</mark>');
      }
    });
    
    return result;
  }
  
  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
  
  escapeRegex(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }
}

// Export globally
window.SearchComponent = SearchComponent;
