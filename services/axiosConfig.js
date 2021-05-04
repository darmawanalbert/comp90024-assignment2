import axios from "axios";

const api = axios.create({
    baseURL: 'http://127.0.0.1:8080/' // this is the baseURL, to double check with Wildan for development
    // baseURL: 'http://0.0.0.0:8080/: // having this as the baseURL doesn't seem to work???
});

export default api;