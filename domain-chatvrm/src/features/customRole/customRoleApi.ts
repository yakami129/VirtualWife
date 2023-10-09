import { getRequest, postRequest } from "../httpclient/httpclient";

export const custoRoleFormData = {
    id: 0,
    role_name: "",
    persona: "",
    personality: "",
    scenario: "",
    examples_of_dialogue: "",
    custom_role_template_type: "",
}

export type CustomRoleFormData = typeof custoRoleFormData;

export const vrmModelData = {
    name: ""
}
export type VrmModel = typeof vrmModelData;





export async function customroleDelete(id: number) {
    const headers: Record<string, string> = {
        "Content-Type": "application/json"
    };
    const chatRes = await postRequest("/chatbot/customrole/delete/" + id, headers, custoRoleFormData);
    if (chatRes.code !== '200') {
        throw new Error("Something went wrong");
    }
    return chatRes.response;
}

export async function customroleCreate(custoRoleFormData: CustomRoleFormData) {
    const headers: Record<string, string> = {
        "Content-Type": "application/json"
    };
    const chatRes = await postRequest("/chatbot/customrole/create", headers, custoRoleFormData);
    if (chatRes.code !== '200') {
        throw new Error("Something went wrong");
    }

    return chatRes.response;
}

export async function customrolEdit(id: Number, custoRoleFormData: CustomRoleFormData) {
    const headers: Record<string, string> = {
        "Content-Type": "application/json"
    };
    const chatRes = await postRequest("/chatbot/customrole/edit/" + id, headers, custoRoleFormData);
    if (chatRes.code !== '200') {
        throw new Error("Something went wrong");
    }

    return chatRes.response;
}

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