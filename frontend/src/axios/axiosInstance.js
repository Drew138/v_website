import axios from "axios";
import localStorageService from "./localStorageService";
import { history } from "../history"
import { REFRESH_JWT_ENDPOINT, LOGIN_WITH_JWT_ENDPOINT } from "../config"
// https://medium.com/swlh/handling-access-and-refresh-tokens-using-axios-interceptors-3970b601a5da
// LocalstorageService


// Add a request interceptor
export const requestInterceptor = axios.interceptors.request.use(
    config => {
        const token = localStorageService.getAccessToken();
        // console.log(token)
        if (token) {
            config.headers['Authorization'] = 'Bearer ' + token;
        }
        // config.headers['Content-Type'] = 'application/json';
        return config;
    },
    error => {
        Promise.reject(error)
    });

//Add a response interceptor
export const responseInterceptor = axios.interceptors.response.use((response) => {
    return response
}, async function (error) {
    const originalRequest = error.config;
    if (error.response.status === 401 && (originalRequest.url.endsWith(
        REFRESH_JWT_ENDPOINT) || originalRequest.url.endsWith(LOGIN_WITH_JWT_ENDPOINT))) {
        history.push('/pages/login');
        localStorageService.clearToken();
        localStorageService.clearUserValues();
        return Promise.reject(error);
    }

    if (error.response.status === 401 && !originalRequest._retry) {

        originalRequest._retry = true;
        const refreshToken = localStorageService.getRefreshToken();
        const res = await axios.post(REFRESH_JWT_ENDPOINT,
            {
                "refresh": refreshToken
            })
        if (res.status === 200) {
            localStorageService.setToken(res.data);
            axios.defaults.headers.common['Authorization'] = 'Bearer ' + localStorageService.getAccessToken();
            return axios(originalRequest);
        }
        return
    }
    return Promise.reject(error);
});

