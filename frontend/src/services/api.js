import axios from 'axios';

// Force HTTPS for API calls
const getBackendUrl = () => {
  if (process.env.REACT_APP_BACKEND_URL) {
    return process.env.REACT_APP_BACKEND_URL;
  }
  // Fallback: ensure HTTPS
  const origin = window.location.origin;
  return origin.replace('http:', 'https:');
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
  sign: (measureId) => api.post('/measures/sign', { measure_id: measureId }),
  cancel: (measureId, reason) => api.post('/measures/cancel', { measure_id: measureId, reason }),
};

export const auditApi = {
  getLogs: (limit = 100) => api.get(`/audit/logs?limit=${limit}`),
};

export default api;
