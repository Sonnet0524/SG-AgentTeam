/**
 * Connectors Dashboard Component
 * Version: 1.2.0
 * 
 * Provides connector status monitoring and management interface.
 */

class ConnectorsComponent {
  constructor(container) {
    this.container = container;
    this.state = {
      connectors: [],
      loading: false,
      error: null,
      refreshInterval: null,
    };
    
    this.init();
  }
  
  init() {
    this.render();
    this.loadConnectors();
    // Auto-refresh every 30 seconds
    this.startAutoRefresh();
  }
  
  render() {
    this.container.innerHTML = `
      <div class="connectors-container">
        <div class="card-header" style="background: var(--color-bg-primary); border-radius: var(--radius-lg); border: 1px solid var(--color-border); margin-bottom: var(--spacing-lg);">
          <h2 class="card-title">Connectors Dashboard</h2>
          <div class="flex gap-sm">
            <button class="btn btn-secondary" id="refreshConnectorsBtn">
              🔄 Refresh
            </button>
          </div>
        </div>
        
        <div class="connectors-grid" id="connectorsGrid">
          ${this.renderConnectors()}
        </div>
      </div>
    `;
    
    this.attachEventListeners();
  }
  
  renderConnectors() {
    if (this.state.loading) {
      return `
        <div class="loading" style="grid-column: 1 / -1;">
          <div class="spinner"></div>
          <div class="loading-text">Loading connector status...</div>
        </div>
      `;
    }
    
    if (this.state.error) {
      return `
        <div class="empty-state" style="grid-column: 1 / -1;">
          <div class="empty-icon">⚠️</div>
          <div class="empty-title">Error Loading Connectors</div>
          <div class="empty-description">${this.escapeHtml(this.state.error)}</div>
          <button class="btn btn-primary mt-lg" onclick="window.connectorsComponent.loadConnectors()">
            Retry
          </button>
        </div>
      `;
    }
    
    if (this.state.connectors.length === 0) {
      return `
        <div class="empty-state" style="grid-column: 1 / -1;">
          <div class="empty-icon">🔌</div>
          <div class="empty-title">No Connectors</div>
          <div class="empty-description">
            No connectors are configured yet.
          </div>
        </div>
      `;
    }
    
    return this.state.connectors.map(connector => this.renderConnectorCard(connector)).join('');
  }
  
  renderConnectorCard(connector) {
    const statusIcon = this.getStatusIcon(connector.status);
    const statusClass = `status-${connector.status}`;
    const lastSync = connector.last_sync 
      ? new Date(connector.last_sync).toLocaleString() 
      : 'Never';
    
    return `
      <div class="connector-card">
        <div class="connector-header">
          <div class="connector-name">
            <span class="connector-icon">${this.getConnectorIcon(connector.name)}</span>
            ${this.formatConnectorName(connector.name)}
          </div>
          <div class="connector-status ${statusClass}">
            ${statusIcon} ${connector.status.replace('_', ' ')}
          </div>
        </div>
        
        <div class="connector-info">
          <div class="info-row">
            <span class="info-label">Last Sync</span>
            <span class="info-value">${lastSync}</span>
          </div>
          
          ${connector.config ? `
            <div class="info-row">
              <span class="info-label">Server</span>
              <span class="info-value">${this.escapeHtml(connector.config.server || 'N/A')}</span>
            </div>
            ${connector.config.username ? `
              <div class="info-row">
                <span class="info-label">Username</span>
                <span class="info-value">${this.escapeHtml(connector.config.username)}</span>
              </div>
            ` : ''}
          ` : ''}
        </div>
        
        ${connector.error ? `
          <div class="connector-error">
            <strong>Error:</strong> ${this.escapeHtml(connector.error)}
          </div>
        ` : ''}
        
        <div class="connector-actions">
          ${this.getConnectorActions(connector)}
        </div>
      </div>
    `;
  }
  
  getConnectorIcon(name) {
    const icons = {
      email: '📧',
      calendar: '📅',
      cloud_storage: '☁️',
    };
    return icons[name] || '🔌';
  }
  
  getStatusIcon(status) {
    const icons = {
      connected: '✓',
      disconnected: '○',
      error: '✗',
      not_configured: '?',
    };
    return icons[status] || '○';
  }
  
  formatConnectorName(name) {
    return name
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  }
  
  getConnectorActions(connector) {
    const actions = [];
    
    if (connector.status === 'connected') {
      actions.push(`
        <button 
          class="btn btn-secondary btn-sm" 
          onclick="window.connectorsComponent.disconnectConnector('${connector.name}')"
        >
          Disconnect
        </button>
      `);
    } else if (connector.status === 'disconnected' || connector.status === 'error') {
      actions.push(`
        <button 
          class="btn btn-primary btn-sm" 
          onclick="window.connectorsComponent.showConnectModal('${connector.name}')"
        >
          Connect
        </button>
      `);
    } else if (connector.status === 'not_configured') {
      actions.push(`
        <button 
          class="btn btn-secondary btn-sm" 
          onclick="window.connectorsComponent.showConnectModal('${connector.name}')"
        >
          Configure
        </button>
      `);
    }
    
    actions.push(`
      <button 
        class="btn btn-ghost btn-sm" 
        onclick="window.connectorsComponent.viewDetails('${connector.name}')"
      >
        Details
      </button>
    `);
    
    return actions.join('');
  }
  
  attachEventListeners() {
    const refreshBtn = this.container.querySelector('#refreshConnectorsBtn');
    if (refreshBtn) {
      refreshBtn.addEventListener('click', () => this.loadConnectors());
    }
  }
  
  async loadConnectors() {
    this.state.loading = true;
    this.state.error = null;
    this.updateConnectors();
    
    try {
      const response = await window.KAApi.Connectors.getStatus();
      this.state.connectors = response.connectors;
      
    } catch (error) {
      console.error('Failed to load connectors:', error);
      this.state.error = error.message || 'Failed to load connector status';
    } finally {
      this.state.loading = false;
      this.updateConnectors();
    }
  }
  
  updateConnectors() {
    const grid = this.container.querySelector('#connectorsGrid');
    if (grid) {
      grid.innerHTML = this.renderConnectors();
    }
  }
  
  showConnectModal(connectorName) {
    const modal = document.createElement('div');
    modal.className = 'config-modal';
    modal.id = 'connectorConfigModal';
    
    let configFields = '';
    
    if (connectorName === 'email') {
      configFields = `
        <div class="form-group">
          <label class="form-label">IMAP Server *</label>
          <input 
            type="text" 
            class="form-input" 
            id="configServer"
            placeholder="e.g., imap.gmail.com"
            required
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">Port</label>
          <input 
            type="number" 
            class="form-input" 
            id="configPort"
            placeholder="993"
            value="993"
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">Username *</label>
          <input 
            type="text" 
            class="form-input" 
            id="configUsername"
            placeholder="your@email.com"
            required
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">Password *</label>
          <input 
            type="password" 
            class="form-input" 
            id="configPassword"
            placeholder="Your password or app password"
            required
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">
            <input type="checkbox" id="configUseSSL" checked>
            Use SSL
          </label>
        </div>
      `;
    } else {
      configFields = `
        <div class="empty-state">
          <div class="empty-icon">🔧</div>
          <div class="empty-title">Not Implemented</div>
          <div class="empty-description">
            The ${this.formatConnectorName(connectorName)} connector is not yet implemented.
          </div>
        </div>
      `;
    }
    
    modal.innerHTML = `
      <div class="config-form">
        <div class="config-header">
          <h3 class="editor-title">Connect ${this.formatConnectorName(connectorName)}</h3>
          <button class="editor-close" onclick="window.connectorsComponent.closeConfigModal()">
            ✕
          </button>
        </div>
        
        <div class="config-body">
          ${configFields}
        </div>
        
        <div class="config-footer">
          <button class="btn btn-secondary" onclick="window.connectorsComponent.closeConfigModal()">
            Cancel
          </button>
          ${connectorName === 'email' ? `
            <button class="btn btn-primary" onclick="window.connectorsComponent.connectConnector('${connectorName}')">
              Connect
            </button>
          ` : ''}
        </div>
      </div>
    `;
    
    document.body.appendChild(modal);
    
    // Close on backdrop click
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        this.closeConfigModal();
      }
    });
  }
  
  closeConfigModal() {
    const modal = document.getElementById('connectorConfigModal');
    if (modal) {
      modal.remove();
    }
  }
  
  async connectConnector(connectorName) {
    if (connectorName === 'email') {
      const server = document.getElementById('configServer').value.trim();
      const port = parseInt(document.getElementById('configPort').value) || 993;
      const username = document.getElementById('configUsername').value.trim();
      const password = document.getElementById('configPassword').value;
      const use_ssl = document.getElementById('configUseSSL').checked;
      
      if (!server || !username || !password) {
        this.showToast('Please fill in all required fields', 'error');
        return;
      }
      
      const config = {
        server,
        port,
        username,
        password,
        use_ssl,
      };
      
      try {
        const result = await window.KAApi.Connectors.connect(connectorName, config);
        this.showToast(`${this.formatConnectorName(connectorName)} connected successfully`, 'success');
        this.closeConfigModal();
        await this.loadConnectors();
        
      } catch (error) {
        console.error('Failed to connect:', error);
        this.showToast(error.message || 'Failed to connect', 'error');
      }
    }
  }
  
  async disconnectConnector(connectorName) {
    try {
      await window.KAApi.Connectors.disconnect(connectorName);
      this.showToast(`${this.formatConnectorName(connectorName)} disconnected`, 'success');
      await this.loadConnectors();
      
    } catch (error) {
      console.error('Failed to disconnect:', error);
      this.showToast(error.message || 'Failed to disconnect', 'error');
    }
  }
  
  async viewDetails(connectorName) {
    try {
      const connector = await window.KAApi.Connectors.getConnectorStatus(connectorName);
      
      const modal = document.createElement('div');
      modal.className = 'document-editor';
      modal.innerHTML = `
        <div class="editor-modal" style="max-width: 600px;">
          <div class="editor-header">
            <h3 class="editor-title">${this.formatConnectorName(connectorName)} Details</h3>
            <button class="editor-close" onclick="this.closest('.document-editor').remove()">
              ✕
            </button>
          </div>
          
          <div class="editor-body">
            <div class="mb-md">
              <div class="text-sm text-muted mb-sm">Status</div>
              <div class="connector-status status-${connector.status}">
                ${this.getStatusIcon(connector.status)} ${connector.status.replace('_', ' ')}
              </div>
            </div>
            
            <div class="mb-md">
              <div class="text-sm text-muted mb-sm">Last Sync</div>
              <div>${connector.last_sync ? new Date(connector.last_sync).toLocaleString() : 'Never'}</div>
            </div>
            
            ${connector.config ? `
              <div class="mb-md">
                <div class="text-sm text-muted mb-sm">Configuration</div>
                <pre style="background: var(--color-bg-secondary); padding: var(--spacing-md); border-radius: var(--radius-sm); overflow-x: auto; font-size: var(--font-sm);">
${JSON.stringify(connector.config, null, 2)}
                </pre>
              </div>
            ` : ''}
            
            ${connector.error ? `
              <div class="mb-md">
                <div class="text-sm text-muted mb-sm">Error</div>
                <div class="connector-error">${this.escapeHtml(connector.error)}</div>
              </div>
            ` : ''}
          </div>
          
          <div class="editor-footer">
            <button class="btn btn-secondary" onclick="this.closest('.document-editor').remove()">
              Close
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
      
    } catch (error) {
      console.error('Failed to get connector details:', error);
      this.showToast(error.message || 'Failed to load connector details', 'error');
    }
  }
  
  startAutoRefresh() {
    // Clear existing interval
    if (this.state.refreshInterval) {
      clearInterval(this.state.refreshInterval);
    }
    
    // Refresh every 30 seconds
    this.state.refreshInterval = setInterval(() => {
      this.loadConnectors();
    }, 30000);
  }
  
  destroy() {
    if (this.state.refreshInterval) {
      clearInterval(this.state.refreshInterval);
    }
  }
  
  showToast(message, type = 'info') {
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
window.ConnectorsComponent = ConnectorsComponent;
