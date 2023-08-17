import { getRequest } from "../httpclient/httpclient";

export async function customroleList() {

    const headers: Record<string, string> = {
        "Content-Type": "application/json"
    };

    const chatRes = await getRequest("/chatbot/customrole/list", headers);
    if (chatRes.code !== '200') {
        throw new Error("Something went wrong");
    }

    return chatRes.response;
}

export async function vrmModelList() {

    const headers: Record<string, string> = {
        "Content-Type": "application/json"
    };

    const chatRes = await getRequest("/chatbot/customrole/vrmmodel/list", headers);
    if (chatRes.code !== '200') {
        throw new Error("Something went wrong");
    }

    return chatRes.response;
}