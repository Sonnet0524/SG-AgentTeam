/**
 * Knowledge Assistant API Client
 * Version: 1.2.0
 * 
 * Provides a clean interface to interact with the Knowledge Assistant backend API.
 */

// API Configuration
const API_CONFIG = {
  baseUrl: window.location.origin,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
};

/**
 * API Error class for better error handling
 */
class APIError extends Error {
  constructor(message, status, details) {
    super(message);
    this.name = 'APIError';
    this.status = status;
    this.details = details;
  }
}

/**
 * Make an HTTP request with error handling
 */
async function request(endpoint, options = {}) {
  const url = `${API_CONFIG.baseUrl}${endpoint}`;
  
  const config = {
    ...options,
    headers: {
      ...API_CONFIG.headers,
      ...options.headers,
    },
  };
  
  // Add timeout
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), API_CONFIG.timeout);
  config.signal = controller.signal;
  
  try {
    const response = await fetch(url, config);
    clearTimeout(timeoutId);
    
    // Parse response
    let data;
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      data = await response.json();
    } else {
      data = await response.text();
    }
    
    // Check for errors
    if (!response.ok) {
      const error = data.detail || data;
      throw new APIError(
        error.message || 'Request failed',
        response.status,
        error.details || error
      );
    }
    
    return data;
    
  } catch (error) {
    clearTimeout(timeoutId);
    
    if (error.name === 'AbortError') {
      throw new APIError('Request timeout', 408, { timeout: API_CONFIG.timeout });
    }
    
    if (error instanceof APIError) {
      throw error;
    }
    
    throw new APIError(
      error.message || 'Network error',
      0,
      { originalError: error }
    );
  }
}

/**
 * Search API
 */
const SearchAPI = {
  /**
   * Search documents using semantic search
   * @param {Object} params - Search parameters
   * @param {string} params.q - Search query
   * @param {number} params.limit - Maximum number of results
   * @param {number} params.offset - Number of results to skip
   * @param {string} params.index_path - Path to index directory
   * @param {number} params.threshold - Minimum similarity threshold
   * @returns {Promise<Object>} Search results
   */
  async search(params) {
    const queryParams = new URLSearchParams();
    queryParams.append('q', params.q);
    if (params.limit) queryParams.append('limit', params.limit);
    if (params.offset) queryParams.append('offset', params.offset);
    if (params.index_path) queryParams.append('index_path', params.index_path);
    if (params.threshold !== undefined) queryParams.append('threshold', params.threshold);
    
    return request(`/api/search?${queryParams.toString()}`);
  },
  
  /**
   * Search with POST method (supports filters)
   * @param {Object} body - Search request body
   * @returns {Promise<Object>} Search results
   */
  async searchPost(body) {
    return request('/api/search', {
      method: 'POST',
      body: JSON.stringify(body),
    });
  },
};

/**
 * Documents API
 */
const DocumentsAPI = {
  /**
   * List documents
   * @param {Object} params - List parameters
   * @param {number} params.limit - Maximum number of documents
   * @param {number} params.offset - Number of documents to skip
   * @param {string} params.category - Filter by category
   * @returns {Promise<Object>} Document list
   */
  async list(params = {}) {
    const queryParams = new URLSearchParams();
    if (params.limit) queryParams.append('limit', params.limit);
    if (params.offset) queryParams.append('offset', params.offset);
    if (params.category) queryParams.append('category', params.category);
    
    return request(`/api/documents?${queryParams.toString()}`);
  },
  
  /**
   * Get a single document
   * @param {string} docId - Document ID
   * @returns {Promise<Object>} Document
   */
  async get(docId) {
    return request(`/api/documents/${docId}`);
  },
  
  /**
   * Create a new document
   * @param {Object} doc - Document data
   * @param {string} doc.content - Document content
   * @param {Object} doc.metadata - Document metadata
   * @returns {Promise<Object>} Created document
   */
  async create(doc) {
    return request('/api/documents', {
      method: 'POST',
      body: JSON.stringify(doc),
    });
  },
  
  /**
   * Update a document
   * @param {string} docId - Document ID
   * @param {Object} updates - Update data
   * @param {string} updates.content - Updated content
   * @param {Object} updates.metadata - Updated metadata
   * @returns {Promise<Object>} Updated document
   */
  async update(docId, updates) {
    return request(`/api/documents/${docId}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
  },
  
  /**
   * Delete a document
   * @param {string} docId - Document ID
   * @returns {Promise<void>}
   */
  async delete(docId) {
    return request(`/api/documents/${docId}`, {
      method: 'DELETE',
    });
  },
};

/**
 * Connectors API
 */
const ConnectorsAPI = {
  /**
   * Get status of all connectors
   * @returns {Promise<Object>} Connector statuses
   */
  async getStatus() {
    return request('/api/connectors/status');
  },
  
  /**
   * Get status of a specific connector
   * @param {string} connectorName - Connector name
   * @returns {Promise<Object>} Connector status
   */
  async getConnectorStatus(connectorName) {
    return request(`/api/connectors/${connectorName}/status`);
  },
  
  /**
   * Connect a connector
   * @param {string} connectorName - Connector name
   * @param {Object} config - Connector configuration
   * @returns {Promise<Object>} Connector info
   */
  async connect(connectorName, config) {
    return request('/api/connectors/connect', {
      method: 'POST',
      body: JSON.stringify({
        connector_name: connectorName,
        config: config,
      }),
    });
  },
  
  /**
   * Disconnect a connector
   * @param {string} connectorName - Connector name
   * @returns {Promise<Object>} Connector info
   */
  async disconnect(connectorName) {
    return request(`/api/connectors/disconnect?connector_name=${connectorName}`, {
      method: 'POST',
    });
  },
};

/**
 * Health Check API
 */
const HealthAPI = {
  /**
   * Check API health
   * @returns {Promise<Object>} Health status
   */
  async check() {
    return request('/health');
  },
  
  /**
   * Get API info
   * @returns {Promise<Object>} API info
   */
  async info() {
    return request('/api');
  },
};

// Export for use in other modules
window.KAApi = {
  Search: SearchAPI,
  Documents: DocumentsAPI,
  Connectors: ConnectorsAPI,
  Health: HealthAPI,
  APIError,
};
