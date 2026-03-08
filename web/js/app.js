/**
 * Knowledge Assistant Web Application
 * Version: 1.2.0
 * 
 * Main application entry point that orchestrates all components.
 */

class App {
  constructor() {
    this.currentTab = 'search';
    this.components = {};
    this.toasts = [];
    
    this.init();
  }
  
  init() {
    // Check API health
    this.checkHealth();
    
    // Initialize components
    this.initComponents();
    
    // Attach navigation listeners
    this.attachNavigationListeners();
    
    // Show default tab
    this.showTab('search');
  }
  
  async checkHealth() {
    try {
      const health = await window.KAApi.Health.check();
      console.log('API Health:', health);
      
      if (health.status === 'degraded') {
        this.showToast('Warning: Index not found. Build an index first.', 'warning');
      }
    } catch (error) {
      console.error('Health check failed:', error);
      this.showToast('Failed to connect to API server', 'error');
    }
  }
  
  initComponents() {
    // Components will be initialized when tabs are shown
  }
  
  attachNavigationListeners() {
    const navBtns = document.querySelectorAll('.nav-btn');
    
    navBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const tab = btn.dataset.tab;
        if (tab) {
          this.showTab(tab);
        }
      });
    });
  }
  
  showTab(tabName) {
    // Update navigation
    const navBtns = document.querySelectorAll('.nav-btn');
    navBtns.forEach(btn => {
      if (btn.dataset.tab === tabName) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });
    
    // Update content
    const mainContent = document.getElementById('mainContent');
    if (!mainContent) return;
    
    // Destroy old component if exists
    if (this.components[this.currentTab]) {
      if (this.components[this.currentTab].destroy) {
        this.components[this.currentTab].destroy();
      }
    }
    
    // Show new tab
    this.currentTab = tabName;
    
    switch (tabName) {
      case 'search':
        mainContent.innerHTML = '<div id="searchComponent"></div>';
        this.components.search = new window.SearchComponent(
          document.getElementById('searchComponent')
        );
        window.searchComponent = this.components.search;
        break;
        
      case 'documents':
        mainContent.innerHTML = '<div id="documentsComponent"></div>';
        this.components.documents = new window.DocumentsComponent(
          document.getElementById('documentsComponent')
        );
        window.documentsComponent = this.components.documents;
        break;
        
      case 'connectors':
        mainContent.innerHTML = '<div id="connectorsComponent"></div>';
        this.components.connectors = new window.ConnectorsComponent(
          document.getElementById('connectorsComponent')
        );
        window.connectorsComponent = this.components.connectors;
        break;
        
      default:
        mainContent.innerHTML = `
          <div class="empty-state">
            <div class="empty-icon">🤷</div>
            <div class="empty-title">Unknown Tab</div>
            <div class="empty-description">Tab "${tabName}" not found.</div>
          </div>
        `;
    }
  }
  
  showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;
    
    const icons = {
      success: '✓',
      error: '✗',
      warning: '⚠',
      info: 'ℹ',
    };
    
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
      <span class="toast-icon">${icons[type]}</span>
      <span class="toast-message">${this.escapeHtml(message)}</span>
      <button class="toast-close" onclick="this.parentElement.remove()">✕</button>
    `;
    
    container.appendChild(toast);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
      if (toast.parentElement) {
        toast.remove();
      }
    }, 5000);
  }
  
  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.app = new App();
  window.showToast = (message, type) => window.app.showToast(message, type);
});
