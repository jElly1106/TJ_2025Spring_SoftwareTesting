import axios from 'axios';
import { message } from 'antd';
import { getToken } from '@/utils/token';

const baseURL = '/api';

// Create an instance of axios
const instance = axios.create({
  baseURL,
  timeout: 10000, // Request timeout
});

// Request interceptor
instance.interceptors.request.use(
  (config) => {
    // Do something before request is sent
    const token = getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    // Do something with request error
    return Promise.reject(error);
  },
);

// Response interceptor
instance.interceptors.response.use(
  (response) => {
    // Do something with response data
    return response.data;
  },
  (error) => {
    // Do something with response error
    message.error(error.response?.data?.message || 'An error occurred');
    return Promise.reject(error);
  },
);

// API methods
export const runUnitTest = async (testCase: any) => {
  const formData = new FormData();

  // Fix plot_details serialization
  if (testCase.plot_details) {
    if (typeof testCase.plot_details === 'string') {
      formData.append('plot_details', testCase.plot_details);
    } else {
      formData.append('plot_details', JSON.stringify(testCase.plot_details));
    }
  }

  // ...existing code...
};