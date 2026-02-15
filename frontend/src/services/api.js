import axios from 'axios';

// Force HTTPS for API calls - HARDCODED FIX FOR MIXED CONTENT
const getBackendUrl = () => {
  // Always use HTTPS URL to prevent Mixed Content errors
  return 'https://medidas-tracker.preview.emergentagent.com';
};

const BACKEND_URL = getBackendUrl();
const API = `${BACKEND_URL}/api`;

console.log('[API Config] Backend URL:', BACKEND_URL);
console.log('[API Config] API Base URL:', API);

const api = axios.create({
  baseURL: API,
});

// Force HTTPS in all requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  
  // Force HTTPS
  if (config.url && config.url.startsWith('http:')) {
    config.url = config.url.replace('http:', 'https:');
  }
  if (config.baseURL && config.baseURL.startsWith('http:')) {
    config.baseURL = config.baseURL.replace('http:', 'https:');
  }
  
  console.log('[API Request]', config.method?.toUpperCase(), config.url || config.baseURL);
  
  return config;
});

export const employeeApi = {
  getAll: () => api.get('/employees'),
  getById: (id) => api.get(`/employees/${id}`),
  create: (data) => api.post('/employees', data),
  update: (id, data) => api.patch(`/employees/${id}`, data),
};

export const measureApi = {
  getAll: () => api.get('/measures'),
  getByEmployee: (employeeId) => api.get(`/measures/employee/${employeeId}`),
  getDashboardStats: () => api.get('/measures/dashboard/stats'),
  create: (data) => api.post('/measures', data),
  acknowledge: (measureId) => api.post('/measures/acknowledge', { measure_id: measureId }),
  acknowledgeWithWitnesses: (data) => api.post('/measures/acknowledge-witnesses', data),
  sign: (measureId) => api.post('/measures/sign', { measure_id: measureId }),
  cancel: (measureId, reason) => api.post('/measures/cancel', { measure_id: measureId, reason }),
};

export const auditApi = {
  getLogs: (limit = 100) => api.get(`/audit/logs?limit=${limit}`),
};

export const teamApi = {
  getAll: () => api.get('/teams'),
  create: (data) => api.post('/teams', data),
  migrateEmployee: (data) => api.post('/teams/migrate-employee', data),
};

export const userApi = {
  getAll: () => api.get('/users'),
  create: (data) => api.post('/users', data),
  getHierarchy: () => api.get('/users/hierarchy'),
};

export const documentApi = {
  uploadTemplate: (file, measureType) => {
    const formData = new FormData();
    formData.append('file', file);
    if (measureType) formData.append('measure_type', measureType);
    return api.post('/documents/templates/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },
  getTemplates: () => api.get('/documents/templates'),
  downloadTemplate: (templateId) => {
    return api.get(`/documents/templates/download/${templateId}`, {
      responseType: 'blob'
    });
  },
};

export default api;
