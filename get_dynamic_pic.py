from typing import Annotated
from nonebot.rule import to_me, Namespace, ArgumentParser
from nonebot.params import ShellCommandArgs
from protocol_adapter.adapter_type import AdapterMessageEvent
from protocol_adapter.protocol_adapter import ProtocolAdapter
from nonebot import on_shell_command
from utils.permission import white_list_handle
from kmrbot.painter.dynamic_painter.dynamic_painter import DynamicPainter
from utils.permission import only_me


parser = ArgumentParser()
parser.add_argument("--dynamic_id", "--id")
get_dynamic_pic = on_shell_command(
    "get_dynamic",
    aliases={"dynamic_get"},
    rule=to_me(),
    parser=parser,
    priority=5)

get_dynamic_pic.handle()(white_list_handle("gm_cmd"))
get_dynamic_pic.handle()(only_me)


@get_dynamic_pic.handle()
async def _(
    event: AdapterMessageEvent,
    params: Annotated[Namespace, ShellCommandArgs()]
):
    msg = ProtocolAdapter.MS.reply(event)
    params = vars(params)
    dynamic_id = params.get("dynamic_id") or params.get("id")
    if dynamic_id is None or not dynamic_id.isdecimal():
        msg += ProtocolAdapter.MS.text("Invalid Dynamic_id!")
        await get_dynamic_pic.finish(msg)
    dynamic_id = int(dynamic_id)
    image = await DynamicPainter.generate_dynamic_pic(dynamic_id)
    if image is None:
        msg += ProtocolAdapter.MS.text(f"Dynamic_id {dynamic_id} is not exist!")
        await get_dynamic_pic.finish(msg)
    msg += ProtocolAdapter.MS.text(f"Dynamic_id {dynamic_id}\n")
    msg += ProtocolAdapter.MS.image(image)
    await get_dynamic_pic.finish(msg)
