#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-8-22 18:40:03
# @Author  : datachain
import threading

import websocket
import time, urllib, hmac, hashlib
import logging
import json

from qbase.common import configer as cf, until as util
from qbase.common.mmaper import Mmaper

klinFormat = {'id': 1234567890, 'open': 9999999999.9999999999, 'close': 9999999999.9999999999, 'low': 9999999999.9999999999, 'high': 9999999999.9999999999, 'amount': 9999999999.9999999999, 'vol': 9999999999.9999999999, 'count': 999999999999}

def createKline():
    """
    "id": K线id,
    "amount": 成交量(张),
    "count": 成交笔数,
    "open": 开盘价,
    "close": 收盘价,当K线为最晚的一根时，是最新成交价
    "low": 最低价,
    "high": 最高价,
    "vol": 成交额(币)
    :return:
    """
    return {'id': 0, 'open': 0, 'close': 0, 'low': 0, 'high': 0, 'amount': 0, 'vol': 0, 'count': 0}

def getKLineDataFrommarket(symbol, interval, dataNum):
    """
    获取k线数据
    :param symbol:
    :param interval:
    :param dataNum:
    :return:
    """
    # 定义日志
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)  # Change this to DEBUG if you want a lot more info
    ch = logging.StreamHandler()
    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    log.addHandler(ch)

    configer = cf.configer()

    mmapSize = klinFormat.__sizeof__() * (dataNum + 1)
    mpW = Mmaper('mmapData/' + symbol + '.dat', mmapSize, 'W')

    currentKline = {'id': 0}    # 当前周期K线数据
    nextWholeTime = 0           # 下一个整点时间
    resultKlines = []

    def __on_message(ws, message):
        log.info(message)
        if message == "pong":
            pass
        else:
            message = json.loads(message)
            if "table" in message and "action" in message and "data" in message:
                if message["table"] == "trade" and message["action"] == "insert":
                    # 处理交易为分钟数据
                    datas = message["data"]

                    nonlocal nextWholeTime, currentKline, resultKlines

                    for data in datas:
                        timestamp = util.parseUTC2TimestampInMinute(data["timestamp"])
                        price = data["price"]
                        size = data["size"]
                        homeNotional = data["homeNotional"]

                        if timestamp >= nextWholeTime:
                            # 新的周期k线
                            nextWholeTime = util.getWholeTime(timestamp, interval)
                            currentKline = createKline()
                            currentKline["id"] = timestamp
                            currentKline["open"] = price
                            currentKline["low"] = price
                            currentKline["high"] = price

                            resultKlines.append(currentKline)
                            while len(resultKlines) > dataNum:
                                resultKlines.pop(0)

                        currentKline["close"] = price
                        currentKline["high"] = max(currentKline["high"], price)
                        currentKline["low"] = min(currentKline["low"], price)
                        currentKline["amount"] += size
                        currentKline["vol"] += homeNotional

                    # 写入mmap
                    mpW.writeDataToMmap(json.dumps(resultKlines).ljust(mmapSize, '\x00').encode())

    def __on_close(ws):
        log.info("websocket close")

    def __on_open(ws):
        log.info("websocket open")
        def run():
            while True:
                time.sleep(30)
                ws.send("ping")
        threading.Thread(target=run).start()

    def __on_error(ws, error):
        log.error("websocket error", error)

    def generate_signature(secret, verb, url, nonce, data):
        """Generate a request signature compatible with BitMEX."""
        # Parse the url so we can remove the base and extract just the path.
        parsedURL = urllib.parse.urlparse(url)
        path = parsedURL.path
        if parsedURL.query:
            path = path + '?' + parsedURL.query

        # print "Computing HMAC: %s" % verb + path + str(nonce) + data
        message = (verb + path + str(nonce) + data).encode('utf-8')

        signature = hmac.new(secret.encode('utf-8'), message, digestmod=hashlib.sha256).hexdigest()
        return signature

    def __get_auth():

        apiKey = configer.getValueByKey("bitmex", "apiKey")
        apiSecret = configer.getValueByKey("bitmex", "apiSecret")

        '''Return auth headers. Will use API Keys if present in settings.'''
        log.info("Authenticating with API Key.")
        # To auth to the WS using an API key, we generate a signature of a nonce and
        # the WS API endpoint.
        nonce = int(round(time.time() * 1000))
        return [
            "api-nonce: " + str(nonce),
            "api-signature: " + generate_signature(apiSecret, 'GET', '/realtime', nonce, ''),
            "api-key:" + apiKey
        ]

    def service():

        url = "wss://www.bitmex.com/realtime?subscribe=trade:" + symbol
        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(url,
                                    on_message=__on_message,
                                    on_close=__on_close,
                                    on_open=__on_open,
                                    on_error=__on_error,
                                    header=__get_auth())
        # 设置代理
        port = int(configer.getValueByKey('proxy', 'port'))
        print(port)
        if port > 0:
            wst = threading.Thread(target=lambda: ws.run_forever(http_proxy_host="127.0.0.1", http_proxy_port=port))
        else:
            wst = threading.Thread(target=lambda: ws.run_forever())
        wst.start()
        log.info("启动：%s" % url)

    service()
