export interface imageType {
  id: number;
  url: string;
  result: string,
  description: string;
}


export interface responseType {
  result_code: number;
  error?: string;
  content: {
    record: imageInfoType[],
  };
}

export interface imageInfoType {
  id: number;
  url: string;
  label: string,
  pred: string,
  prob: string,
  result: boolean,
}
