import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const api = axios.create({
  baseURL: API,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
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
