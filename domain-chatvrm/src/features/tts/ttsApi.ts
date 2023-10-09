import { buildUrl } from "@/utils/buildUrl";
import { getRequest, postRequest, buildMediaUrl } from "../httpclient/httpclient";


export const voiceData = {
    id: "",
    name: ""
}
export type Voice = typeof voiceData;

export async function getVoices(tts_type: string) {
    const headers: Record<string, string> = {
        "Content-Type": "application/json"
    };

    const body = {
        "type": tts_type
    }

    const chatRes = await postRequest("/speech/tts/voices",headers,body);
    if (chatRes.code !== '200') {
        throw new Error("Something went wrong");
    }
    return chatRes.response;
}
