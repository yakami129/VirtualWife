import { buildUrl } from "@/utils/buildUrl";
import { getRequest, postRequest, buildMediaUrl } from "../httpclient/httpclient";


export const backgroundModelData = {
    id: -1,
    original_name: "",
    image: ""
}
export type BackgroundModel = typeof backgroundModelData;

export const vrmModelData = {
    id: -1,
    type: "",
    original_name: "",
    vrm: ""
}
export type VrmModel = typeof vrmModelData;

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

export async function deleteVrmModel(id: number) {
    const headers: Record<string, string> = {
        "Content-Type": "application/json"
    };
    const chatRes = await postRequest("/chatbot/config/vrm/delete/" + id, headers, {});
    if (chatRes.code !== '200') {
        throw new Error("Something went wrong");
    }
    return chatRes.response;
}

export async function uploadVrmModel(formData: FormData) {
    const headers: Record<string, string> = {
        "Content-Type": "multipart/form-data"
    };
    const chatRes = await postRequest("/chatbot/config/vrm/upload", headers, formData);
    if (chatRes.code !== '200') {
        throw new Error("Something went wrong");
    }
    return chatRes.response;
}

export async function uploadRolePackage(formData: FormData) {
    const headers: Record<string, string> = {
        "Content-Type": "multipart/form-data"
    };
    const chatRes = await postRequest("/chatbot/rolepackage/upload", headers, formData);
    if (chatRes.code !== '200') {
        throw new Error("Something went wrong");
    }
    return chatRes.response;
}

export async function queryUserVrmModels() {
    const headers: Record<string, string> = {
        "Content-Type": "application/json"
    };
    const chatRes = await getRequest("/chatbot/config/vrm/user/show", headers);
    if (chatRes.code !== '200') {
        throw new Error("Something went wrong");
    }
    return chatRes.response;
}

export async function querySystemVrmModels() {
    const headers: Record<string, string> = {
        "Content-Type": "application/json"
    };
    const chatRes = await getRequest("/chatbot/config/vrm/system/show", headers);
    if (chatRes.code !== '200') {
        throw new Error("Something went wrong");
    }
    return chatRes.response;
}


export function generateMediaUrl(url: string) {
    return buildMediaUrl(url)
}

export function buildVrmModelUrl(url: string, type: string) {
    let vrm_url = ""
    if (type === "user") {
        vrm_url = generateMediaUrl(url);
    } else {
        vrm_url = buildUrl(url);
    }
    return vrm_url
}
