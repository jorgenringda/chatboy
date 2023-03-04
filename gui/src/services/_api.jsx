import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

export const get = async (url) => {
  try {
    const response = await api.get(url);
    return await response.data;
  } catch (err) {
    console.log(err);
  }
};

export const post = async (url, content) => {
  try {
    const response = await api.post(url, content);
    return await response.data;
  } catch (err) {
    console.log(err);
  }
};

export const put = async (url, content) => {
  try {
    const response = await api.put(url, content);
    return await response.data;
  } catch (err) {
    console.log(err);
  }
};

export const del = async (url, sessID) => {
  try {
    const response = await api.delete(url + sessID);
    return await response.data;
  } catch (err) {
    console.log(err);
  }
};
