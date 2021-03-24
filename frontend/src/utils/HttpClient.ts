import axios, {
	AxiosError,
	AxiosInstance,
	AxiosRequestConfig,
	AxiosResponse,
} from 'axios';
//@ts-ignore
import NProgress from 'nprogress';
interface IHttpClient {
	get<T>(url: string, options?: AxiosRequestConfig): Promise<T | void>;
	post<T, K>(
		url: string,
		payload: K,
		options?: AxiosRequestConfig,
	): Promise<T | void>;
	put<T, K>(
		url: string,
		payload: K,
		options?: AxiosRequestConfig,
	): Promise<T | void>;
	delete<T>(url: string, options?: AxiosRequestConfig): Promise<T | void>;
}

interface IHttpClientConfig extends AxiosRequestConfig {
	baseURL: string;
	withCredentials: boolean;
	headers?: object;
}

export class HttpClient implements IHttpClient {
	private instance: AxiosInstance;
	constructor(config: IHttpClientConfig) {
		this.instance = axios.create(config);

		this.instance.interceptors.request.use((config: AxiosRequestConfig) => {
			NProgress.start();
			return config;
		});

		this.instance.interceptors.response.use(
			(response: AxiosResponse) => {
				NProgress.done();
				return Promise.resolve(response);
			},
			(error: AxiosError) => {
				NProgress.done();
				this.handleError(error);
				return Promise.reject(error);
			},
		);
	}

	public setHeaderAuth(token: string): void {
		this.instance.defaults.headers.common[
			'Authorization'
		] = `Bearer ${token}`;
	}
	public removeHeaderAuth(): void {
		this.instance.defaults.headers.common['Authorization'] = null;
	}
	private handleError(error: AxiosError): void {
		switch (error.response?.status) {
			case HttpResponse.BAD_REQUEST: {
				break;
			}
			case HttpResponse.UNAUTHORIZED: {
				break;
			}
			case HttpResponse.FORBIDDEN: {
				break;
			}
			case HttpResponse.NOT_FOUND: {
				break;
			}
			case HttpResponse.UNPROCESSABLE_ENTITY: {
				break;
			}
			case HttpResponse.TOO_MANY_REQUEST: {
				break;
			}
			case HttpResponse.INTERNAL_SERVER_ERROR: {
				break;
			}
		}
	}
	private handleResponse<T>(response: AxiosResponse) {
		if (
			response.status === HttpResponse.OK ||
			response.status === HttpResponse.CREATED
		) {
			return response.data as T;
		}
	}
	public get<T>(
		url: string,
		options?: AxiosRequestConfig,
	): Promise<void | T> {
		return new Promise(resolve => {
			this.instance
				.get(url, options)
				.then((response: AxiosResponse) =>
					resolve(this.handleResponse<T>(response)),
				);
		});
	}
	post<T, K>(
		url: string,
		payload?: K,
		options?: AxiosRequestConfig,
	): Promise<void | T> {
		return new Promise(resolve => {
			this.instance
				.post(url, payload, options)
				.then((response: AxiosResponse) =>
					resolve(this.handleResponse<T>(response)),
				);
		});
	}
	put<T, K>(
		url: string,
		payload: K,
		options?: AxiosRequestConfig,
	): Promise<void | T> {
		return new Promise(resolve => {
			this.instance
				.put(url, payload, options)
				.then((response: AxiosResponse) =>
					resolve(this.handleResponse<T>(response)),
				);
		});
	}
	delete<T>(url: string, options?: AxiosRequestConfig): Promise<void | T> {
		return new Promise(resolve => {
			this.instance
				.delete(url, options)
				.then((response: AxiosResponse) =>
					resolve(this.handleResponse<T>(response)),
				);
		});
	}
}
