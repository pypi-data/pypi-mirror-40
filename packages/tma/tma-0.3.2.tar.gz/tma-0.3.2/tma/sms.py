# -*- coding: utf-8 -*-
"""
sms - 预警消息推送模块
====================================================================
"""
import functools
from zb.tools import sms

server_chan_push = sms.server_chan_push
bear_push = sms.bear_push
EmailSender = sms.EmailSender


def send_email(from_, pw, to, subject, content, files=None, service='163'):
    """邮件发送（支持附件），推荐使用163邮箱"""
    se = EmailSender(from_=from_, pw=pw, service=service)
    se.send_email(to=to, subject=subject, content=content, files=files)
    se.quit()


def push2wx(send_key, by="bear"):
    """装饰器：推送消息到微信

    :param send_key: str
        用于发送消息的key
    :param by: str 默认值 bear
        发送消息的方式，默认是bear，
        可选值 ['bear', 'server_chan']
    :return:
    """
    def _wrapper(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            title, content = func(*args, **kw)
            if by == "bear":
                bear_push(title, content, send_key=send_key)
            elif by == "server_chan":
                server_chan_push(title, content, key=send_key)
            else:
                raise ValueError("参数by的可选值为 ['bear', 'server_chan']")
            return title, content
        return wrapper
    return _wrapper
