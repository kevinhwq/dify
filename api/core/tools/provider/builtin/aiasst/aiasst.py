from core.tools.provider.builtin.aiasst.tools.contacts_query import AsstContactsQueryTool
from core.tools.provider.builtin.aiasst.tools.contacts_save import AsstContactsSaveTool
from core.tools.provider.builtin_tool_provider import BuiltinToolProviderController


class AIAsstProvider(BuiltinToolProviderController):
    def _validate_credentials(self, credentials: dict) -> None:
        AsstContactsQueryTool()
        AsstContactsSaveTool()
        pass
