import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Attach JWT token to outgoing requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for auth expiration handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Clear token if expired or invalid
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      if (window.location.pathname !== '/login' && window.location.pathname !== '/register') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// Auth Services
export const authService = {
  login: async (credentials) => {
    const response = await api.post('/api/auth/login', credentials);
    return response.data;
  },
  register: async (userData) => {
    const response = await api.post('/api/auth/register', userData);
    return response.data;
  },
  getMe: async () => {
    const response = await api.get('/api/auth/me');
    return response.data;
  },
};

// Student Feedback Services
export const feedbackService = {
  getDepartments: async () => {
    const response = await api.get('/api/feedback/departments');
    return response.data;
  },
  getCourses: async (department = '') => {
    const params = department ? { department } : {};
    const response = await api.get('/api/feedback/courses', { params });
    return response.data;
  },
  getFaculty: async (department = '') => {
    const params = department ? { department } : {};
    const response = await api.get('/api/feedback/faculty', { params });
    return response.data;
  },
  submitFeedback: async (feedbackData) => {
    const response = await api.post('/api/feedback/', feedbackData);
    return response.data;
  },
  getMyFeedback: async () => {
    const response = await api.get('/api/feedback/my');
    return response.data;
  },
  getFeedbackById: async (id) => {
    const response = await api.get(`/api/feedback/${id}`);
    return response.data;
  },
};

// Admin Analytics & Management Services
export const adminService = {
  getDashboardStats: async () => {
    const response = await api.get('/api/admin/dashboard');
    return response.data;
  },
  getFeedbackList: async (filters = {}) => {
    const response = await api.get('/api/admin/feedback', { params: filters });
    return response.data;
  },
  getAnalytics: async () => {
    const response = await api.get('/api/admin/analytics');
    return response.data;
  },
  getAlerts: async () => {
    const response = await api.get('/api/admin/alerts');
    return response.data;
  },
  getInsights: async () => {
    const response = await api.get('/api/admin/insights');
    return response.data;
  },
  getCategories: async () => {
    const response = await api.get('/api/admin/categories');
    return response.data;
  },
  getTrends: async () => {
    const response = await api.get('/api/admin/trends');
    return response.data;
  },
};

export default api;
