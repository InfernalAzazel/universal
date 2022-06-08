import axios, { AxiosRequestConfig } from "axios";
import router from "./router";
import store from "./store";

axios.defaults.timeout = 8000;

// set global authorization token
axios.interceptors.request.use(
  (config:any) => {
    let token = store.getters.token;
    if (token) {
      config.headers.Authorization = "Token " + token;
      console.log(config.headers)
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

axios.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
      try {
          if (error.response.status === 401) {
              store.commit("clearToken");
              router.push({ path: "/login" });
          } else if (error.response.status === 403) {
              router.push({ path: "/home" });
          }
      } catch (_){}

    return Promise.reject(error);
  }
);

export default axios;
