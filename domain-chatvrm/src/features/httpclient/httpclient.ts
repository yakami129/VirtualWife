// 导入axios库
import axios from "axios";

// 获取当前环境变量，假设为PRODUCT_ENV
const environment = process.env.NODE_ENV;

// 定义基础URL
let baseUrl = "";

if (environment === "development") {
  baseUrl = "http://localhost:8000";
} else if (environment === "production") {
  baseUrl = "/api/chatbot";
} else {
  throw new Error("未知环境变量");
}

// 定义一个发送POST请求的函数
export async function postRequest(endpoint: string, headers: Record<string, string>, data: object): Promise<any> {
    const response = await axios.post(`${baseUrl}${endpoint}`, data, { headers });
    return response.data; // 返回解析后的数据
}

export async function postRequestArraybuffer(endpoint: string, headers: Record<string, string>, data: object): Promise<any> {
  const response = await axios.post(`${baseUrl}${endpoint}`, data, {
    responseType: 'arraybuffer',
    headers: headers,
  });
  return response.data; // 返回解析后的数据
}

// 定义一个发送Get请求的函数
export async function getRequest(endpoint: string, headers: Record<string, string>) {
    const response = await axios.get(`${baseUrl}${endpoint}`, { headers });
    return response; // 返回响应对象
}