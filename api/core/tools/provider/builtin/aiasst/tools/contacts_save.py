from typing import Any, Union

from core.tools.entities.tool_entities import ToolInvokeMessage
from core.tools.provider.builtin.aiasst.tools import asst_utils
from core.tools.tool.builtin_tool import BuiltinTool


class AsstContactsSaveTool(BuiltinTool):
    def _invoke(self,
                user_id: str,
                tool_parameters: dict[str, Any],
                ) -> Union[ToolInvokeMessage, list[ToolInvokeMessage]]:
        """
            invoke tools
        """
        api_url = '/ai/chat/contacts/save'
        return asst_utils.invokeApi(api_url, tool_parameters)
