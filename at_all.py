from nonebot.rule import to_me
from nonebot import on_command
from protocol_adapter.adapter_type import AdapterGroupMessageEvent
from protocol_adapter.protocol_adapter import ProtocolAdapter
from utils.permission import only_me, white_list_handle


at_all = on_command("at_all",
                    rule=to_me(),
                    priority=5)

at_all.handle()(white_list_handle("gm_cmd"))
at_all.handle()(only_me)


@at_all.handle()
async def _(event: AdapterGroupMessageEvent):
    user_id = int(event.get_user_id())
    await at_all.finish(ProtocolAdapter.MS.at_all() + ProtocolAdapter.MS.text(" at_all response."))
