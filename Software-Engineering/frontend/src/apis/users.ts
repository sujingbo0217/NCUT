import request from "../utils/request";
import {loginType, uploadType} from "../types/users";

// Register
export function register(params: loginType) {
  return request({
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    url: `/api/v1/register/`,
    params: params,
  })
}

// Login
export function login(params: loginType) {
  return request({
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    url: `/api/v1/login/`,
    params: params,
  })
}

export function logout() {
  return request({
    method: 'POST',
    url: `/api/v1/logout/`,
    withCredentials: true,
  })
}

export function upload(params: uploadType) {
  return request({
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    url: `/api/v1/upload/`,
    params: params,
  })
}
