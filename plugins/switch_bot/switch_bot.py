# encoding:utf-8

import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from channel.chat_message import ChatMessage
from common.log import logger
from plugins import *
from .user_db import crud
from decimal import Decimal


@plugins.register(
    name="SwitchBot",
    desire_priority=998,
    hidden=True,
    desc="用户开关机器人",
    version="0.1",
    author="https://github.com/Brandon-lz",
)
class SwitchBot(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info("[SwitchBot] inited")

    def on_handle_context(self, e_context: EventContext):
        if e_context["context"].type not in [
            ContextType.TEXT,
        ]:
            return

        msg: ChatMessage = e_context["context"]["msg"]

        print("debug debug debug:", msg)

        db_user, is_init = crud.init_user(user_name=msg.from_user_nickname, user_id = msg.from_user_id)
        content = e_context["context"].content
        logger.debug("[SwitchBot] on_handle_context. content: %s" % content)
        if msg.ctype == ContextType.ACCEPT_FRIEND:
            reply = Reply()
            reply.type = ReplyType.TEXT
            reply.content = f"初次见面，请发送 开启机器人 激活AI"
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑
            return
        if content == "开启机器人":
            crud.switch_bot_status_user(user_id=msg.from_user_id, status=True)
            reply = Reply()
            reply.type = ReplyType.TEXT
            reply.content = f"机器人已开启"
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑
            return

        elif content == "关闭机器人":
            crud.switch_bot_status_user(user_id=msg.from_user_id, status=False)
            reply = Reply()
            reply.type = ReplyType.TEXT
            reply.content = f"机器人已关闭，重新打开机器人请发送 [开启机器人]"
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑
            return
        elif content == ".余额查询" or content==".查询余额":
            banlance = db_user.get_banlance()
            reply = Reply()
            reply.type = ReplyType.TEXT
            reply.content = str(banlance)
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑
            return
        # elif content=="用户id":
        #     reply = Reply()
        #     reply.type = ReplyType.TEXT
        #     reply.content = 
        #     e_context["reply"] = reply
        #     e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑
        #     return
            

        # if not crud.check_bot_status_user(userid=msg.from_user_nickname):
        if not db_user.bot_on:
            e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑
            logger.info("switch_bot off, skip!")
            return
        if db_user.account_balance<=Decimal(0.0):
            reply = Reply()
            reply.type = ReplyType.TEXT
            reply.content = "您的余额不足，可以的话请发送5元红包续费，谢谢！（服务器维护成本，请小哥哥小姐姐理解一下~）"
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑
            return
        crud.cost(user_id=db_user.user_id)

        #文件助手 from_user_id=@4fcd554a96846624789fb5156e8dd4699af0abf0151dae2c2724f39d9878dffb

    def get_help_text(self, **kwargs):
        help_text = "输入[开启机器人] [关闭机器人] 启用或关闭机器人\n"
        return help_text
