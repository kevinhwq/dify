from typing import Any, Union

import httpx

from core.tools.entities.tool_entities import ToolInvokeMessage


def getApiHeaders(app_token: str, tenant_id: str):
    return {
        "Token": app_token,
        "TenantId": tenant_id,
        "ApplicationID": "468939703496814632",
        "Authorization": "bGFtcF93ZWJfcHJvOmxhbXBfd2ViX3Byb19zZWNyZXQ="
    }


def getApiUrl(url: str) -> str:
    # base_url = current_app.config.get("ASST_API_BASE_URL")
    base_url = "http://120.78.174.167/api"
    if url.startswith("/"):
        return base_url + url
    else:
        return base_url + "/" + url


def invokeApi(url: str, tool_parameters: dict[str, Any]) -> Union[
    ToolInvokeMessage, list[ToolInvokeMessage]]:
    """
        create a text message
        :return: the text message
    """

    # 获取参数
    app_token = tool_parameters.get("app_token", "")
    tenant_id = tool_parameters.get("tenant_id", "")
    content = tool_parameters.get('content', '')
    print(f'token: {app_token} \n tenant_id: {tenant_id} \n content: {content}')

    if not app_token:
        return create_text_message('Invalid parameter app_token')
    if not tenant_id:
        return create_text_message('Invalid parameter tenant_id')
    if not content:
        return create_text_message('Invalid parameter content')

    api_url = getApiUrl(url)
    headers = getApiHeaders(app_token, tenant_id)
    data = {
        "data": content
    }

    try:
        res = httpx.post(api_url, headers=headers, data=data)
        print(f'res: {res}')
        if res.is_success:
            return create_text_message(res.text)
        else:
            return create_text_message(
                f"Failed to send the text message, status code: {res.status_code}, response: {res.text}")
    except Exception as e:
        return create_text_message("Failed to send message to group chat bot. {}".format(e))


def create_text_message(text: str, save_as: str = '') -> ToolInvokeMessage:
    return ToolInvokeMessage(type=ToolInvokeMessage.MessageType.TEXT,
                             message=text,
                             save_as=save_as
                             )
