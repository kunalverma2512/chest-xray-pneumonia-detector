import axios from 'axios';

const axiosClient = axios.create({
 baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
 timeout: 30000,
 headers: { 'Accept': 'application/json' },
});

axiosClient.interceptors.response.use(
 (res) => res,
 (err) => {
 const message =
 err.response?.data?.detail ||
 err.response?.data?.message ||
 err.message ||
 'An unexpected error occurred.';
 return Promise.reject(new Error(message));
 }
);

export default axiosClient;
