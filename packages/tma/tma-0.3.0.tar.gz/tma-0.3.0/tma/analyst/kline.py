# -*- coding: UTF-8 -*-

"""
analyst.kline - K线分析
====================================================================
"""

from tma.collector.ts import get_klines

kls1 = get_klines('600165', freq='D', start_date='2018-01-01')
kls2 = get_klines('600682', freq='D', start_date='2018-01-01')


class KlineSimilarity(object):
    pass


class KlineAnalyst:
    """K线技术分析

    输入样例（api: pro.daily）：
         ts_code trade_date  open  high   low  close  pct_change         vol
    0  600122.SH   20181112  4.56  4.83  4.55   4.79      5.7395   885379.38
    1  600122.SH   20181109  4.56  4.62  4.52   4.53     -2.9979   607091.75
    2  600122.SH   20181108  4.61  4.75  4.52   4.67     -3.7113  1420418.02

    """
    def __init__(self, kline, kind='1D'):
        self.kline = self.raw_kline = kline
        self.kind = kind

    def ma(self, col, n=5):
        col_out = col + "_ma_" + str(n)
        col_series = self.kline[col]
        col_series.sort_index(ascending=False, inplace=True)
        self.kline[col_out] = col_series.rolling(n).mean()
