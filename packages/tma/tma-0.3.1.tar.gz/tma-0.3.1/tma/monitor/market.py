# -*- coding: UTF-8 -*-
"""

====================================================================
"""

from tma.indicator import MarketDayIndicator
from tma.collector.ts import get_indices
from tma.collector.ths import get_plate_fund_flow


def get_market_status():
    """获取最新的市场状态，非交易时间段则获取最后交易时刻的市场状态"""
    mi = MarketDayIndicator()
    mi.update()

    market_status_template = "### **实时市场状态**\n --- \n" \
                             "* 今日开盘个股总数为{M002}家，上涨个股数量为{M003}家，**赚钱效应{M001}**；" \
                             "其中涨3个点以上个股数量是{M004}家，跌3个点以上个股数量是{M005}家。\n" \
                             "* 换手率前50只个股赚钱效应{M006}，其中涨3个点以上个股数量是{M007}家，" \
                             "跌3个点以上个股数量是{M008}家。\n" \
                             "* 目前两市涨停{M009}家，其中一字板{M010}家；盘中触及涨停后打开家数为" \
                             "{M011}，封板成功率为{M012}；两市跌停{M013}家，其中一字板跌停{M014}" \
                             "家，盘中触及跌停板{M015}家。\n\n"

    i = mi.indicators
    market_status = market_status_template.format(
        M002=i['M002']['value'], M003=i['M003']['value'],
        M001="%.2f" % (i['M001']['value'] * 100) + "%",
        M004=i['M004']['value'], M005=i['M005']['value'],
        M006="%.2f" % (i['M006']['value'] * 100) + "%",
        M007=i['M007']['value'], M008=i['M008']['value'],
        M009=i['M009']['value'], M010=i['M010']['value'],
        M011=i['M011']['value'],
        M012="%.2f" % (i['M012']['value'] * 100) + "%",
        M013=i['M013']['value'], M014=i['M014']['value'],
        M015=i['M015']['value'],
    )

    return market_status


def get_indices_status(selected=None):
    """获取最新指数状态，非交易时间段则获取最后交易时刻的指数状态

    :param selected: list
        选出的主要指数。
        默认值：
            ["上证指数", "创业板指", "深证成指", "中小板指",
            "沪深300", "上证50", "中证500", "上证380"]

    :return: msg_index :class:str
    """
    if selected is None:
        selected = ["上证指数", "创业板指", "深证成指", "中小板指",
                    "沪深300", "上证50", "中证500", "上证380"]
    indices = get_indices()
    msg_index_head = "### **指数走势** \n--- \n" \
                     "|指数名称|涨幅|振幅|\n" \
                     "|:---:|:---:|:---:|\n"
    msg_index_template = """|{0}|{1}|{2}|\n"""

    msg_index = [msg_index_head]

    for s in selected:
        row = indices[indices['name'] == s]
        if len(row) == 1:
            row_dict = dict(row.iloc[0])
            change_rate = str(row_dict['change']) + "%"
            wave_rate = (row_dict['high'] - row_dict['low']) / row_dict['open']
            wave_rate = "%.2f" % (wave_rate * 100) + "%"
            msg_index.append(msg_index_template.format(s, change_rate, wave_rate))

    msg_index = ''.join(msg_index) + '\n'
    return msg_index


def get_top_plate(top=6):
    """获取今天的涨幅靠前的概念板块、行业板块

    :param top: int
    :return: str
    """
    hy = get_plate_fund_flow('hyzjl')
    gn = get_plate_fund_flow('gnzjl')

    # 行业资金流 Top
    hy.sort_values('涨跌幅', ascending=False, inplace=True)
    hy_top = "### **行业板块涨幅前%s名** \n--- \n " \
             "|行业|涨跌幅|资金净额（亿）|股票数量|领涨股|\n" \
             "|:---:|:---:|:---:|:---:|:---:|\n" % top
    for i in range(top):
        row = hy.iloc[i, :]
        row_info = "|%s|%s|%s|%s|%s|\n" % (row['行业'], row['涨跌幅'],
                                           row['净额(亿)'], row['公司家数'], row['领涨股'])
        hy_top += row_info

    # 概念资金流 Top
    gn.sort_values('涨跌幅', ascending=False, inplace=True)
    gn_top = "### **概念板块涨幅前%s名** \n--- \n " \
             "|行业|涨跌幅|资金净额（亿）|股票数量|领涨股|\n" \
             "|:---:|:---:|:---:|:---:|:---:|\n" % top
    for i in range(top):
        row = gn.iloc[i, :]
        row_info = "|%s|%s|%s|%s|%s|\n" % (row['行业'], row['涨跌幅'],
                                           row['净额(亿)'], row['公司家数'], row['领涨股'])
        gn_top += row_info

    return gn_top + hy_top

