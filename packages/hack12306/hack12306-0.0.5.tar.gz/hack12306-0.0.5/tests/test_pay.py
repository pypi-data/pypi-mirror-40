# encoding: utf8

"""
支付
"""

import json
import copy
from hack12306.api import TrainApi
from hack12306.utils import tomorrow, JSONEncoder
from hack12306 import constants

from config import COOKIES, PUBLIC_IP_ADDR, ORDER_SEQUENCE_NO


def test_pay():
    train_api = TrainApi()

    # 1.支付未完成订单
    pay_no_complete_order_result = train_api.pay_no_complete_order(ORDER_SEQUENCE_NO, cookies=COOKIES)
    print 'pay no complete order result. %s' % json.dumps(pay_no_complete_order_result, ensure_ascii=False,)
    if pay_no_complete_order_result['existError'] != 'N':
        print '未找到未完成的订单'
        return

    # 2.支付初始化
    train_api.pay_init(cookies=COOKIES)

    # 3.发起支付
    pay_check_new_result = train_api.pay_check_new(cookies=COOKIES)
    print 'pay check new result. %s' % json.dumps(pay_check_new_result, ensure_ascii=False)

    # 4.交易
    pay_business_result = train_api.pay_web_business(
        pay_check_new_result['payForm']['tranData'],
        pay_check_new_result['payForm']['merSignMsg'],
        pay_check_new_result['payForm']['transType'],
        PUBLIC_IP_ADDR, pay_check_new_result['payForm']['tranDataParsed']['order_timeout_date'],
        constants.BANK_ID_WX, cookies=COOKIES)
    print 'pay business result. %s' % json.dumps(pay_business_result, ensure_ascii=False)

    # 5.跳转第三方支付
    pay_business_third_pay_resp = train_api.submit(
        pay_business_result['url'],
        pay_business_result['params'],
        method=pay_business_result['method'],
        parse_resp=False, cookies=COOKIES)
    print 'pay third resp status code. %s' % pay_business_third_pay_resp.status_code
    print 'pay third resp. %s' % pay_business_third_pay_resp.content


if __name__ == '__main__':
    test_pay()
