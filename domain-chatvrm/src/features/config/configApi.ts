import { getRequest, postRequest } from "../httpclient/httpclient";

// 定义formData初始状态 shape
export const initialFormData = {
    "liveStreamingConfig": {
        "B_STATION_ID": "27892212"
    },
    "enableProxy": false,
    "httpProxy": "http://127.0.0.1:7890",
    "httpsProxy": "https://127.0.0.1:7890",
    "socks5Proxy": "socks5://127.0.0.1:7890",
    "languageModelConfig": {
        "openai": {
            "OPENAI_API_KEY": "sk-",
            "OPENAI_BASE_URL": ""
        },
        "textGeneration": {
            "TEXT_GENERATION_API_URL": "http://127.0.0.1:5000"
        }
    },
    "characterConfig": {
        "character": "爱莉",
        "yourName": "alan",
        "vrmModel": "xxx"
    },
    "conversationConfig": {
        "conversationType": "default",
        "languageModel": "text_generation"
    },
    "memoryStorageConfig": {
        "localMemory": {
            "maxMemoryLoads": 5
        },
        "milvusMemory": {
            "host": "127.0.0.1",
            "port": "19530",
            "user": "user",
            "password": "Milvus",
            "dbName": "default"
        },
        "longTermMemoryType": "local",
        "enableSummary": false,
        "languageModelForSummary": "text_generation",
        "enableReflection": false,
        "languageModelForReflection": "text_generation"
    }
}

// 定义类型别名
export type FormDataType = typeof initialFormData;

export async function getConfig() {

    const headers: Record<string, string> = {
        "Content-Type": "application/json"
    };

    const chatRes = await getRequest("/chatbot/config/get", headers);
    if (chatRes.code !== '200') {
        throw new Error("Something went wrong");
    }

    return chatRes.response;
}

export async function saveConfig(
    config: Object
) {

    const headers: Record<string, string> = {
        "Content-Type": "application/json"
    };

    const body = {
        "config": config
    };

    const chatRes = await postRequest("/chatbot/config/save", headers, body);
    if (chatRes.code !== '200') {
        throw new Error("Something went wrong");
    }

    return chatRes.response;
}