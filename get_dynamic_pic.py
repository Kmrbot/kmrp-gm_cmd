from typing import Annotated
from nonebot.log import logger
from nonebot.rule import to_me, Namespace, ArgumentParser
from nonebot.params import ShellCommandArgs
from protocol_adapter.adapter_type import AdapterMessageEvent
from protocol_adapter.protocol_adapter import ProtocolAdapter
from nonebot import on_shell_command
from utils.permission import white_list_handle
from kmrbot.render_service.client import DynamicRenderClient, DynamicRenderErrorKind
from utils.permission import only_me
from utils.bili.http_request import BiliHttpRequest


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
    dynamic_data = await BiliHttpRequest.get("https://api.bilibili.com/x/polymer/web-dynamic/v1/detail", {
        "timezone_offset": -480,
        "id": dynamic_id,
        "features": "itemOpusStyle,listOnlyfans,opusBigCover,onlyfansVote,decorationCard,onlyfansAssetsV2,"
                    "forwardListHidden,ugcDelete,onlyfansQaCard,commentsNewVersion"
    })
    if dynamic_data is None or dynamic_data.get("item") is None:
        logger.error("dynamic data is None !")
        await get_dynamic_pic.finish()
    dynamic_data = dynamic_data["item"]
    result = await DynamicRenderClient.render_dynamic(dynamic_data)
    if not result.ok:
        if result.error_kind == DynamicRenderErrorKind.SERVICE:
            msg += ProtocolAdapter.MS.text(
                f"绘制服务异常，请稍后重试。（{result.message}）"
            )
        elif result.error_kind == DynamicRenderErrorKind.RENDER:
            msg += ProtocolAdapter.MS.text(
                f"动态绘制失败。（{result.message}）"
            )
        else:
            msg += ProtocolAdapter.MS.text(f"DynamicID {dynamic_id} 绘制失败。")
        await get_dynamic_pic.finish(msg)
    msg += ProtocolAdapter.MS.text(f"DynamicID {dynamic_id}\n")
    msg += ProtocolAdapter.MS.image(result.image)
    await get_dynamic_pic.finish(msg)
