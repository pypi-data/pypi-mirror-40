#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019/1/2
# @Author  : beequants-nick


import pandas as pd
from qbase.common import mySql
from qbase.common import configer as cf
import logging

log = logging.getLogger()
conf = cf.configer()
klineRow = "created_date/1000 as created_date, open, high, low, close, volume, currency_volume, symbol"


def get_kline_list(symbol, period, num=None):
    db = mySql.Mysql(conf.getValueByKey("dbData", "ip"), int(conf.getValueByKey("dbData", "port")),
                     conf.getValueByKey("dbData", "userName"), conf.getValueByKey("dbData", "passwd"),
                     conf.getValueByKey("dbData", "dnName"))
    sql = "select " + klineRow + " from okex_futures_kline_%s where symbol = '" % period + symbol + "_usd' "
    sql += " order by created_date desc"
    if num is not None:
        sql += " limit %s" % num
    kline = pd.read_sql(sql, db.getDb())
    db.closeDb()
    return kline

