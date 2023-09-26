import { getRequest, postRequest } from "../httpclient/httpclient";

// 定义formData初始状态 shape
export const initialFormData = {
	"liveStreamingConfig": {
		"B_STATION_ID": "622909"
	},
	"enableProxy": false,
	"httpProxy": "http://host.docker.internal:23457",
	"httpsProxy": "https://host.docker.internal:23457",
	"socks5Proxy": "socks5://host.docker.internal:23457",
	"languageModelConfig": {
		"openai": {
			"OPENAI_API_KEY": "sk-",
			"OPENAI_BASE_URL": ""
		},
		"textGeneration": {
			"TEXT_GENERATION_API_URL": "http://127.0.0.1:5000",
			"TEXT_GENERATION_WEB_SOCKET_URL": "ws://127.0.0.1:5005/api/v1/stream"
		}
	},
	"characterConfig": {
		"character": 1,
		"yourName": "yuki129",
		"vrmModel": "\u308f\u305f\u3042\u3081_03.vrm"
	},
	"conversationConfig": {
		"conversationType": "default",
		"languageModel": "openai"
	},
	"memoryStorageConfig": {
		"milvusMemory": {
			"host": "127.0.0.1",
			"port": "19530",
			"user": "user",
			"password": "Milvus",
			"dbName": "default"
		},
		"enableLongMemory": false,
		"enableSummary": false,
		"languageModelForSummary": "openai",
		"enableReflection": false,
		"languageModelForReflection": "openai"
	},
	"custom_role_template_type": "zh",
	"role_name": "1",
	"background_id": 1,
	"background_url": ""
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