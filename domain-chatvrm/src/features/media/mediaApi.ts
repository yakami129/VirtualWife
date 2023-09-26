import { getRequest, postRequest,buildMediaUrl } from "../httpclient/httpclient";


export const backgroundModelData = {
    id: -1,
    original_name: "",
    image: ""
}
export type BackgroundModel = typeof backgroundModelData;

export async function deleteBackground(id: number) {
    const headers: Record<string, string> = {
        "Content-Type": "application/json"
    };
    const chatRes = await postRequest("/chatbot/config/background/delete/" + id, headers, {});
    if (chatRes.code !== '200') {
        throw new Error("Something went wrong");
    }
    return chatRes.response;
}

export async function uploadBackground(formData: FormData) {
    const headers: Record<string, string> = {
        "Content-Type": "multipart/form-data"
    };
    const chatRes = await postRequest("/chatbot/config/background/upload", headers, formData);
    if (chatRes.code !== '200') {
        throw new Error("Something went wrong");
    }
    return chatRes.response;
}

export async function queryBackground() {
    const headers: Record<string, string> = {
        "Content-Type": "application/json"
    };
    const chatRes = await getRequest("/chatbot/config/background/show", headers);
    if (chatRes.code !== '200') {
        throw new Error("Something went wrong");
    }
    return chatRes.response;
}

export function buildBackgroundUrl(imageUrl: string) {
    return buildMediaUrl(imageUrl)
}
