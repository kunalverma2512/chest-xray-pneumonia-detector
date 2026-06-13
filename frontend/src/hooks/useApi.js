import { useState, useCallback } from 'react';
import axiosClient from '../utils/axiosClient.js';

/**
 * Generic hook for API calls.
 * @param {Function} apiFn - async function that returns data
 */
export function useApi() {
 const [state, setState] = useState({ data: null, loading: false, error: null });

 const execute = useCallback(async (apiFn) => {
 setState({ data: null, loading: true, error: null });
 try {
 const data = await apiFn();
 setState({ data, loading: false, error: null });
 return data;
 } catch (err) {
 setState({ data: null, loading: false, error: err.message });
 throw err;
 }
 }, []);

 const reset = useCallback(() => {
 setState({ data: null, loading: false, error: null });
 }, []);

 return { ...state, execute, reset };
}
