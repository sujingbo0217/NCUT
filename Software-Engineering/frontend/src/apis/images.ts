import request from "../utils/request.ts";

export function uploadImage(params: FormData) {
  return request({
    method: 'POST',
    headers: {
      "Content-Type": "multipart/form-data"
    },
    url: `/api/v1/upload/`,
    data: params,
  })
}

export function displayImage() {
  return request({
    method: 'POST',
    url: `/api/v1/display/`,
  })
}

export function deleteImage(id: string) {
  return request({
    method: 'POST',
    url: `/api/v1/delete/`,
    params: {
      id,
    }
  })
}
