# -*- coding: UTF-8 -*-

"""
analyst.kline - K线分析
====================================================================
"""
import talib
import json
import os
import time
import pickle
from tqdm import tqdm

from tma.collector.ts import pro as ts_pro
from tma.utils import OrderedAttrDict
from tma import cache_path


class KlineAnalyst:
    """K线技术分析

    K线类别：
    1min, 5min, 15min, 30min, 60min, D, W, M

    tushare_pro K线数据接口：
    mins - ts_pro.mins(ts_code='000001.SH', start_time='20181220', end_time='20181222', freq='15min')
    daily - https://tushare.pro/document/2?doc_id=27
    weekly - https://tushare.pro/document/2?doc_id=144
    monthly - https://tushare.pro/document/2?doc_id=145
    """

    def __init__(self, ts_code, start=None, end=None, freq='60min', cache_interval=12*60*60):
        """

        :param ts_code: str
            tushare 股票代码；对于分钟线，也可以是指数代码。
        :param start: str
            开始时间，如 20180101
        :param end: str
            结束时间，如 20181223
        :param freq: str
            K线级别，可选值 [1min, 5min, 15min, 30min, 60min, D, W, M]
        :param cache_interval: int
            数据缓存间隔，单位：秒，默认为 12*60*60
        """
        self.ts_code = ts_code
        self.start = start
        self.end = end
        self.freq = freq

        # 缓存文件
        self.pkl_cache = os.path.join(cache_path, "%s.%s.pkl" % (ts_code, freq))
        if os.path.exists(self.pkl_cache) and \
                time.time() - os.path.getmtime(self.pkl_cache) < cache_interval:
            self.kline, self.results = pickle.load(open(self.pkl_cache, 'rb'))
        else:
            self._get_kline()
            # 分析K线
            self.results = OrderedAttrDict({"ts_code": ts_code, 'freq': freq})
            self.ma_info()
            self.macd_info()
            pickle.dump([self.kline, self.results], open(self.pkl_cache, 'wb'))

    def _get_kline(self):
        if self.freq.endswith('min'):
            k = ts_pro.mins(ts_code=self.ts_code,
                            start_time=self.start,
                            end_time=self.end,
                            freq=self.freq)
        elif self.freq == 'D':
            k = ts_pro.daily(ts_code=self.ts_code,
                             start_date=self.start,
                             end_date=self.end)
        elif self.freq == 'W':
            k = ts_pro.weekly(ts_code=self.ts_code,
                              start_date=self.start,
                              end_date=self.end)
        elif self.freq == 'M':
            k = ts_pro.monthly(ts_code=self.ts_code,
                               start_date=self.start,
                               end_date=self.end)
        else:
            raise ValueError("param 'freq' must one of "
                             "[1min, 5min, 15min, 30min, 60min, D, W, M]")
        k.sort_index(ascending=False, inplace=True)
        k.reset_index(drop=True, inplace=True)
        self.kline = k

    # --------------------------------------------------------------------
    def ma(self, col, n=(5, 10)):
        """计算均线

        :param col: str
            字段名，通常使用 close 计算 MACD 指标
        :param n: int or tuple of int
            均线周期，默认值 5
        :return: None
        """
        if isinstance(n, int):
            n = [n]

        col_series = self.kline[col]
        for i in n:
            col_out = col + "_ma" + str(i)
            self.kline[col_out] = col_series.rolling(i).mean()

    def ma_info(self):
        self.ma('close', (5, 10, 20))
        last_k = self.kline.iloc[-1, :]
        self.results['R001'] = OrderedAttrDict({
            "name": "均线系统",
            "value": dict(last_k[['close', 'close_ma5',
                                  'close_ma10', 'close_ma20']]),
            "explain": "均线分析，重在形态。"
        })

    # --------------------------------------------------------------------
    def macd(self, col):
        """计算 MACD 指标

        :param col: str
            字段名，通常使用 close 计算 MACD 指标
        :return: None
        """
        col_series = self.kline[col]
        macd, signal, hist = talib.MACD(col_series)
        self.kline[col + '_macd'] = macd
        self.kline[col + '_macd_signal'] = signal
        self.kline[col + '_macd_hist'] = hist

    def macd_info(self):
        if "close_macd" not in self.kline.columns:
            self.macd('close')

        last_macd_hist = list(self.kline['close_macd_hist'].iloc[-3:])
        last_macd_hist = ["%.4f" % x for x in last_macd_hist]

        self.results['R101'] = OrderedAttrDict({
            "name": "MACD防狼",
            "value": ", ".join(last_macd_hist),
            "explain": "MACD防狼术：绿柱不买，红柱不卖；更进一步的，"
                       "市场环境不好的情况下，红柱缩短卖出；"
                       "市场环境好的情况下，绿柱缩短买入。"
                       "根据资金量的大小选择合适的K线级别，通常使用60分钟线。"
        })

    def turning(self):
        """分析该级别 K线 的走势，分别对应的是买入（持有），还是卖出（空仓）

        均线买点： ma10*1.02 > ma5 > ma10*0.99
        MACD买点：macd柱子大于等于0
        """
        last_k = self.kline.iloc[-1, :]

        if last_k['close_ma10']*1.02 > last_k['close_ma5'] > last_k['close_ma10']*0.99:
            ma_point = True
        else:
            ma_point = False

        macd_tip = [float(x) for x in self.results.R101.value.split(", ")]
        if last_k['close_macd_hist'] >= 0 and macd_tip[-1] > macd_tip[-2]:
            macd_point = True
        else:
            macd_point = False

        point = ma_point and macd_point
        return point

    def results2json(self):
        return json.loads(json.dumps(self.results, ensure_ascii=False))


def get_ma5_over_ma10_shares(freq, start, end):
    """获取A股市场全部股票在某个K线级别上，MA5位于MA10上方的股票数量

    :param freq: str
        K线级别，可选值 [1min, 5min, 15min, 30min, 60min, D, W, M]
    :param start: str
        开始日期，如 20181201
    :param end: str
        结束日期，如 20181223
    :return: list
    """
    shares = ts_pro.stock_basic(list_status='L', fields='ts_code,name')
    results = []

    for ts_code in tqdm(shares['ts_code'], desc="%s ma5_over_ma10" % freq):
        try:
            ka = KlineAnalyst(ts_code=ts_code, start=start, end=end, freq=freq)
            row = ka.kline.iloc[-1, :]
            if row['close_ma5'] > row['close_ma10']:
                results.append(ts_code)
        except:
            print("fail", ts_code)
    print("在 %s K线级别上，MA5 > MA10 的股票数量共有 %i，占比 %.4f" %
          (freq, len(results), len(results)/len(shares)))
    return results


def get_shares_at_turning(freq, start, end):
    """获取A股市场全部股票在某个K线级别上，MA5位于MA10上方的股票数量

    :param freq: str
        K线级别，可选值 [1min, 5min, 15min, 30min, 60min, D, W, M]
    :param start: str
        开始日期，如 20181201
    :param end: str
        结束日期，如 20181223
    :return: list
    """
    shares = ts_pro.stock_basic(list_status='L', fields='ts_code,name')
    results = []
    for ts_code in tqdm(shares['ts_code'], desc="%s selector" % freq):
        try:
            ka = KlineAnalyst(ts_code=ts_code, start=start, end=end, freq=freq)
            point = ka.turning()
            if point:
                results.append(ts_code)
        except:
            print("fail", ts_code)
    return results



