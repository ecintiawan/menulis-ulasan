import { HttpClient } from '../utils/HttpClient';

export const api = new HttpClient({
	baseURL: import.meta.env.VITE_API_URL as string,
	withCredentials: true,
});
