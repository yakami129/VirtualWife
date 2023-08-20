import { postRequest } from "../httpclient/httpclient";

export async function translation(
    text: string,
    target_language: string
) {

    const headers: Record<string, string> = {
        "Content-Type": "application/json"
    };

    const body = {
        "text": text,
        "target_language": target_language
    };
    // const chatRes = await postRequest("/speech/translation", headers, body);
    // if (chatRes.code !== '200') {
    //     throw new Error("Something went wrong");
    // }

    // return chatRes.response;
    return text;
}