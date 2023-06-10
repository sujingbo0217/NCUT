import axios, {AxiosRequestConfig} from 'axios';

// axios.defaults.xsrfCookieName = 'csrftoken';
// axios.defaults.xsrfHeaderName = 'X-CSRFToken';
// axios.defaults.withCredentials = true;

const request = axios.create({
  baseURL: import.meta.env.VITE_APP_BASE_API,
});

export default <T>(config: AxiosRequestConfig) => {
  return request(config).then(res => {
    return res.data as T;
  });
}
