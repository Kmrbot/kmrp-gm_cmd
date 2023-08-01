import datetime
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message
from nonebot import on_command
from haruka_bot.utils import (
    group_only,
)
from plugins import while_list_handle

work_list = on_command(
    "工作表", aliases={
        "工资表"},
    priority=5,
)
work_list.__doc__ = """工作表"""
work_list.__help_type__ = None

work_list.handle()(while_list_handle("gm_cmd"))
work_list.handle()(group_only)


@work_list.handle()
async def _(
    event: GroupMessageEvent
):
    event_msg_extra_str = {
        "工资表": "书架：不好好切片翻译打轴校对还想要工资？？？\n\n",
    }
    # 一个彩蛋
    pre_str = event_msg_extra_str.get(str(event.message), "")
    msg = Message(pre_str + "docs.qq.com/sheet/DQlNUUmZ2U3FvRkRV?tab=ss_85aacb")
    await work_list.finish(msg)
