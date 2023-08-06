#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-8-22 18:40:03
# @Author  : datachain

import json
from enum import Enum

from bravado.client import SwaggerClient, SwaggerFormat
from bravado.requests_client import RequestsClient

from qbase.bitmex.apiKeyAuthenticator import APIKeyAuthenticator
from qbase.common import configer as cf

class BitMexSide(Enum):
    """
    bitmex委托类型买卖枚举
    """
    OpenLong = "Buy"        # 做多
    OpenShort = "Sell"      # 做空
    CloseLong = "Sell"      # 平多
    CloseShort = "Buy"      # 平空
    Buy = "Buy"             # 买入/做多/平空
    Sell = "Sell"           # 卖出/做空/平多

class BitmexService(object):
    """
    bitmex rest service
    """

    def __init__(self, apiKey, apiSecret):
        self.__apiKey = apiKey
        self.__apiSecret = apiSecret

        # 自定义json format，否则日志会警告
        my_json_format = SwaggerFormat(
            format='JSON',
            to_wire=lambda b: b if isinstance(b, str) else str(b),
            to_python=lambda s: s if isinstance(s, str) else str(s),
            validate=lambda x: x,  # jsonschema validates string
            description='Converts [wire]string:byte <=> python byte'
        )
        my_guid_format = SwaggerFormat(
            format="guid",
            to_wire=lambda b: b if isinstance(b, str) else str(b),
            to_python=lambda s: s if isinstance(s, str) else str(s),
            validate=lambda x: x,  # jsonschema validates string
            description='Converts [wire]string:byte <=> python byte'
        )
        # swagger client 配置
        config = {
            # Don't use models (Python classes) instead of dicts for #/definitions/{models}
            'use_models': False,
            # bravado has some issues with nullable fields
            'validate_responses': False,
            # Returns response in 2-tuple of (body, response); if False, will only return body
            'also_return_response': True,
            # List of user-defined formats
            'formats': [my_json_format, my_guid_format],
        }
        request_client = RequestsClient()

        configer = cf.configer()
        port = int(configer.getValueByKey('proxy', 'port'))
        if port > 0:
            # 设置代理
            proxies = {
                'http': 'http://127.0.0.1:' + str(port),
                'https': 'http://127.0.0.1:' + str(port),
            }
            request_client.session.trust_env = False
            request_client.session.proxies.update(proxies)

        host = configer.getValueByKey('bitmex', 'host')
        request_client.authenticator = APIKeyAuthenticator(host, self.__apiKey, self.__apiSecret)

        url = host + "/api/explorer/swagger.json"
        self.__client = SwaggerClient.from_url(url, config=config, http_client=request_client)

    def getClient(self):
        """
        可以获取client直接按swagger api格式调用接口
            see: https://www.bitmex.com/api/explorer/
            see: https://www.bitmex.com/api/explorer/swagger.json
        :return: swagger client
        """
        return self.__client

    def getOrders(self, symbol=None, orderID = None, clOrdID = None):
        """
        获取订单列表
        :param symbol: 合约类型，eg. XBTUSD
                       可以加上时间区间, e.g. XBU:monthly. 时间区间可以是 daily, weekly, monthly, quarterly, and biquarterly.
        :param orderID: bitmex订单id，可选，用来进行筛选订单
        :param clOrdID: 自定义订单id，可选，用来进行筛选订单
        :return:
        """
        filter = None
        if orderID or clOrdID:
            filterDict = {}
            if orderID:
                filterDict['orderID'] = orderID
            if clOrdID:
                filterDict['clOrdID'] = clOrdID
            filter = json.dumps(filterDict)
        resp = self.__client.Order.Order_getOrders(symbol=symbol, filter=filter).response()
        return resp.result

    def createOrder(self, symbol, side, orderQty=None, clOrdID = None, simpleOrderQty=None):
        """
        提交市价委托订单

            createOrder("XBTUSD", BitMexSide.Short, orderQty=1, clOrdID=str(uuid.uuid1()))

        :param symbol: 合约类型
        :param side: 委托类型 BitmexSide枚举
        :param orderQty: 合约张数
        :param clOrdID: 自定义订单id，需保证每个账户中所有订单中的自定义订单id唯一
        :param simpleOrderQty: 交易数量，与合约张数二选一
        :return:
        """

        if not isinstance(side, BitMexSide):
            raise TypeError('bad side type, should be BitMexSide Enum')

        parameters = {
            "symbol": symbol,
            "side": side.value,
            "orderQty": orderQty,
            "simpleOrderQty": simpleOrderQty,
            "clOrdID": clOrdID,
        }
        resp = self.__client.Order.Order_new(**parameters).response()
        return resp.result

    def closePosition(self, symbol, side, orderQty=None, clOrdID = None, simpleOrderQty=None):
        """
        市价平仓

            closePosition("XBTUSD", BitMexSide.CloseShort, orderQty=1, clOrdID=str(uuid.uuid1()))

        :param symbol: 合约类型
        :param side: 委托类型 BitmexSide枚举
        :param orderQty: 合约张数
        :param clOrdID: 自定义订单id，需保证每个账户中所有订单中的自定义订单id唯一
        :param simpleOrderQty: 交易数量，与合约张数二选一
        :return: 
        """
        if not isinstance(side, BitMexSide):
            raise TypeError('bad side type, should be BitMexSide Enum')

        parameters = {
            "symbol": symbol,
            "side": side.value,
            "orderQty": orderQty,
            "simpleOrderQty": simpleOrderQty,
            "clOrdID": clOrdID,
            "execInst": "Close",
            "price": "0.00007040"
        }
        resp = self.__client.Order.Order_new(**parameters).response()
        return resp.result
