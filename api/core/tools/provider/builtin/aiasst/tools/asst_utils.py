from typing import Any, Union

import httpx
from flask import current_app

from core.tools.entities.tool_entities import ToolInvokeMessage


def get_api_headers(app_token: str, tenant_id: str):
    app_id = current_app.config.get("ASST_API_APPID", "468939703496814632")
    app_auth = current_app.config.get("ASST_API_AUTH", "bGFtcF93ZWJfcHJvOmxhbXBfd2ViX3Byb19zZWNyZXQ=")
    return {
        "Token": app_token,
        "TenantId": tenant_id,
        "ApplicationID": app_id,
        "Authorization": app_auth
    }


def get_api_url(url: str) -> str:
    base_url = current_app.config.get("ASST_API_BASE_URL", "http://120.78.174.167/api")
    if url.startswith("/"):
        return base_url + url
    else:
        return base_url + "/" + url


def invoke_api(url: str, tool_parameters: dict[str, Any]) -> Union[
    ToolInvokeMessage, list[ToolInvokeMessage]]:
    """
        create a text message
        :return: the text message
    """

    # 获取参数
    app_token = tool_parameters.get("app_token", "")
    app_tenant_id = tool_parameters.get("app_tenant_id", "")
    content = tool_parameters.get('content', '')
    print(f'app_token: {app_token} \n app_tenant_id: {app_tenant_id} \n content: {content}')

    if not app_token:
        return create_text_message('parameter app_token can not be empty')
    if not app_tenant_id:
        return create_text_message('parameter tenant_id can not be empty')
    if not content:
        return create_text_message('parameter content can not be empty')

    api_url = get_api_url(url)
    headers = get_api_headers(app_token, app_tenant_id)
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
