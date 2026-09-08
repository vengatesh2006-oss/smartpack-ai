import axios, { AxiosError } from 'axios';
import { getToken, clearAuth } from './auth';

const API_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = getToken();
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      clearAuth();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Define interfaces for API responses/requests
export interface VerifyRequest {
  image: File;
  pack_id: string;
}

export interface VerifyResponse {
  id: string;
  status: 'Pass' | 'Fail' | 'Review';
  confidence: number;
  results: any[];
}

export const verifyPacking = async (partId: string, image: File): Promise<any> => {
  const formData = new FormData();
  formData.append('file', image);
  
  const response = await api.post(`/verify-packing/verify-packing?part_id=${partId}`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getInspections = async () => {
  const response = await api.get('/inspections');
  return response.data;
};

export const getInspection = async (id: string) => {
  const response = await api.get(`/inspections/${id}`);
  return response.data;
};

export const submitManualDecision = async (id: string, decision: string, reason: string) => {
  const response = await api.post(`/inspections/${id}/manual-decision`, { decision, reason });
  return response.data;
};

export const getParts = async () => {
  const response = await api.get('/parts');
  return response.data;
};

export const syncInspections = async (inspections: any[]) => {
  const response = await api.post('/inspections/sync', { inspections });
  return response.data;
};

export const getDashboardMetrics = async () => {
  const response = await api.get('/dashboard/metrics');
  return response.data;
};

export const login = async (credentials: any) => {
  const response = await api.post('/login', credentials);
  return response.data;
};

export const register = async (userData: any) => {
  const response = await api.post('/register', userData);
  return response.data;
};

export default api;
