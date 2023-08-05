# -*- coding: UTF-8 -*-
import os
from pathlib import Path
import shutil

# 元信息
# --------------------------------------------------------------------
__name__ = 'tma'
__version__ = "0.3.1"
__author__ = "zengbin"


# 设置用户文件夹
# --------------------------------------------------------------------
data_path = os.path.join(os.path.expanduser('~'), ".tma")
cache_path = os.path.join(data_path, "cache")
Path(cache_path).mkdir(parents=True, exist_ok=True)


def clean_cache():
    shutil.rmtree(cache_path)
    Path(cache_path).mkdir(parents=True, exist_ok=True)


# 基本参数配置
# --------------------------------------------------------------------
DEBUG = False

# 全局日志记录器
from zb.utils import create_logger

log_file = os.path.join(data_path, "tma.log")
logger = create_logger(log_file, name='tma', cmd=True)

# API - 列表
# --------------------------------------------------------------------
from tma.pool import StockPool
from tma import monitor
from tma import analyst
from tma import indicator
from tma.sms import push2wx, send_email
from tma.utils import OrderedAttrDict
from tma.utils import Calendar
from tma.analyst.rank import TfidfDocRank

# module介绍
# --------------------------------------------------------------------

__doc__ = """
TMA - Tools for Market A - A股工具集
"""
