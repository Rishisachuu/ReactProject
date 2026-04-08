import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_URL
});

// Add token to headers
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth Services
export const authService = {
  register: (email, password, name) => {
    return api.post('/auth/register', { email, password, name });
  },
  login: (email, password) => {
    return api.post('/auth/login', { email, password });
  }
};

// Profile Services
export const profileService = {
  getProfile: (userId) => {
    return api.get(`/users/${userId}`);
  },
  updateProfile: (userId, data) => {
    return api.put(`/users/${userId}`, data);
  },
  uploadAvatar: (userId, file) => {
    const formData = new FormData();
    formData.append('avatar', file);
    return api.post(`/users/${userId}/upload-avatar`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },
  changePassword: (userId, currentPassword, newPassword) => {
    return api.put(`/users/${userId}/change-password`, {
      current_password: currentPassword,
      new_password: newPassword
    });
  },
  updatePrivacy: (userId, privacy) => {
    return api.put(`/users/${userId}/privacy`, { privacy });
  }
};

export default api;
