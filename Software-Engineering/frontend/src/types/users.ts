export interface registerType {
  username: string,
  password: string,
  confirm: string,
}

export interface loginType {
  username: string,
  password: string,
}

export interface responseType {
  result_code: number,
  error?: string,
  content: object,
}
