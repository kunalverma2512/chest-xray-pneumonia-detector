import { useState, useCallback } from 'react';
import axiosClient from '../utils/axiosClient.js';
import { API_ROUTES } from '../utils/apiRoutes.js';

/**
 * Upload an X-ray image and get a prediction from the backend.
 *
 * Returns:
 * upload(file) — call this with a File object
 * data — prediction response or null
 * loading — boolean
 * error — string or null
 * reset — clears state
 */
export function useUploadXray() {
 const [data, setData] = useState(null);
 const [loading, setLoading] = useState(false);
 const [error, setError] = useState(null);

 const upload = useCallback(async (file) => {
 if (!file) return;
 setLoading(true);
 setData(null);
 setError(null);

 const formData = new FormData();
 formData.append('file', file);

 try {
 const res = await axiosClient.post(API_ROUTES.PREDICT, formData, {
 headers: { 'Content-Type': 'multipart/form-data' },
 });
 setData(res.data);
 } catch (err) {
 setError(err.message || 'Prediction failed. Please try again.');
 } finally {
 setLoading(false);
 }
 }, []);

 const reset = useCallback(() => {
 setData(null);
 setLoading(false);
 setError(null);
 }, []);

 return { upload, data, loading, error, reset };
}
