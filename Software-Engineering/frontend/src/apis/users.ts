import request from "../utils/request";
import {loginType} from "../types/users";

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
