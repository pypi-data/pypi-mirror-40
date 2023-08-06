# encoding: utf8
"""
run.py
@author Meng.yangyang
@description Booking entry point
@created Tue Jan 08 2019 19:38:32 GMT+0800 (CST)
@last-modified Thu Jan 10 2019 15:54:35 GMT+0800 (CST)
"""

import os
import re
import time
import json
import logging
import platform
import logging.config
from hack12306.constants import (BANK_ID_WX, BANK_ID_MAP, SEAT_TYPE_CODE_MAP,)
from hack12306.exceptions import TrainUserNotLogin, TrainBaseException

from . import settings
from . import exceptions
from .pay import pay_order
from .auth import auth_qr, auth_is_login
from .user import user_passengers
from .order import order_submit, order_check_no_complete
from .query import query_left_tickets, query_station_code_map

_logger = logging.getLogger('booking')


BOOKING_STATUS_QUERY_LEFT_TICKET = 2
BOOKING_STATUS_ORDER_SUBMIT = 3
BOOKING_STATUS_PAY_ORDER = 4

BOOKING_STATUS_MAP = [
    (BOOKING_STATUS_QUERY_LEFT_TICKET, '查询余票'),
    (BOOKING_STATUS_ORDER_SUBMIT, '提交订单'),
    (BOOKING_STATUS_PAY_ORDER, '支付订单'),
]


def initialize():
    """
    Initialization.
    """
    if settings.INIT_DONE:
        return

    settings.STATION_CODE_MAP = query_station_code_map()
    logging.config.dictConfig(settings.LOGGING)

    if platform.system() == "Windows":
        settings.CHROME_APP_OPEN_CMD = settings.CHROME_APP_OPEN_CMD_WINDOWS
    elif platform.system() == 'Linux':
        settings.CHROME_APP_OPEN_CMD = settings.CHROME_APP_OPEN_CMD_LINUX
    elif platform.mac_ver()[0]:
        settings.CHROME_APP_OPEN_CMD = settings.CHROME_APP_OPEN_CMD_MacOS
    else:
        settings.CHROME_APP_OPEN_CMD = settings.CHROME_APP_OPEN_CMD_MacOS

    settings.INIT_DONE = True


def _query_left_ticket_counter_get():
    if not os.path.exists(settings.QUERY_LEFT_TICKET_COUNTER_FILE):
        return 0

    with open(settings.QUERY_LEFT_TICKET_COUNTER_FILE) as f:
        counter = f.read() or '0'
        return int(counter)


def _query_left_ticket_counter_set(counter):
    if not os.path.exists(settings.QUERY_LEFT_TICKET_COUNTER_FILE):
        os.makedirs(os.path.dirname(settings.QUERY_LEFT_TICKET_COUNTER_FILE))

    with open(settings.QUERY_LEFT_TICKET_COUNTER_FILE, 'w') as f:
        f.write(str(counter))


def run(train_date, train_name, seat_types, from_station, to_station, pay_channel=BANK_ID_WX, passengers=None, **kwargs):
    """
    Booking entry point.
    """
    initialize()
    assert settings.INIT_DONE is True, 'No Initialization'

    date_patten = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    assert date_patten.match(train_date), 'Invalid train_date param. %s' % train_date

    assert isinstance(seat_types, (list, tuple)), u'Invalid seat_types param. %s' % seat_types
    assert frozenset(seat_types) <= frozenset(dict(SEAT_TYPE_CODE_MAP).keys()
                                              ), u'Invalid seat_types param. %s' % seat_types

    assert from_station in settings.STATION_CODE_MAP.values(), 'Invalid from_station param. %s' % from_station
    assert to_station in settings.STATION_CODE_MAP.values(), 'Invalid to_station param. %s' % to_station
    assert pay_channel in dict(BANK_ID_MAP).keys(), 'Invalid pay_channel param. %s' % pay_channel

    train_info = {}
    order_no = None
    check_passengers = False
    passenger_id_nos = []
    booking_status = BOOKING_STATUS_QUERY_LEFT_TICKET
    left_ticket_counter = _query_left_ticket_counter_get()

    while True:
        try:
            # auth
            if not settings.COOKIES or not auth_is_login(settings.COOKIES):
                cookies = auth_qr()
                settings.COOKIES = cookies

            # check passengers
            if not check_passengers:
                passenger_infos = user_passengers()
                if passengers:
                    passenger_name_id_map = {}
                    for passenger_info in passenger_infos:
                        passenger_name_id_map[passenger_info['passenger_name']] = passenger_info['passenger_id_no']

                    assert frozenset(passengers) <= frozenset(passenger_name_id_map.keys()), u'无效的乘客. %s' % json.dumps(
                        list(frozenset(passengers) - frozenset(passenger_name_id_map.keys())), ensure_ascii=False)

                    for passenger in passengers:
                        _logger.info(u'订票乘客信息。姓名：%s 身份证号:%s' % (passenger, passenger_name_id_map[passenger]))
                        passenger_id_nos.append(passenger_name_id_map[passenger])
                else:
                    passenger_id_nos = [passenger_infos[0]['passenger_id_no']]
                    _logger.info(
                        u'订票乘客信息。姓名:%s 身份证号:%s' %
                        (passenger_infos[0]['passenger_name'],
                         passenger_info['passenger_id_no']))

                check_passengers = True

            # order not complete
            if order_check_no_complete():
                booking_status = BOOKING_STATUS_PAY_ORDER

            _logger.debug('booking status. %s' % dict(BOOKING_STATUS_MAP).get(booking_status, '未知状态'))

            # query left tickets
            if booking_status == BOOKING_STATUS_QUERY_LEFT_TICKET:
                left_ticket_counter += 1
                if left_ticket_counter % 10 == 0:
                    _query_left_ticket_counter_set(left_ticket_counter)

                _logger.info('查询余票, 已查询%s次!' % left_ticket_counter)
                train_info = query_left_tickets(train_date, from_station, to_station, seat_types, train_name)
                booking_status = BOOKING_STATUS_ORDER_SUBMIT

            # subit order
            elif booking_status == BOOKING_STATUS_ORDER_SUBMIT:
                try:
                    _logger.info('提交订单')
                    order_no = order_submit(passenger_id_nos, **train_info)
                except (TrainBaseException, exceptions.BookingBaseException) as e:
                    _logger.info('提交订单失败')
                    booking_status = BOOKING_STATUS_QUERY_LEFT_TICKET
                    _logger.exception(e)
                    continue
                else:
                    # submit order successfully
                    if order_no:
                        _logger.info('提交订单成功')
                        booking_status = BOOKING_STATUS_PAY_ORDER

            # pay
            elif booking_status == BOOKING_STATUS_PAY_ORDER:
                _logger.info('支付订单')
                pay_order(pay_channel)
                # pay success and exit
                return
            else:
                assert 'Unkown booking status. %s' % booking_status

        except TrainUserNotLogin:
            _logger.warn('用户未登录，请重新扫码登录')
            continue

        except TrainBaseException as e:
            _logger.error(e)
            _logger.exception(e)

        except Exception as e:
            if isinstance(e, AssertionError):
                _logger.exception(e)
                _logger.error('系统内部运行异常，请重新执行程序！')
                os._exit(-1)
            elif isinstance(e, exceptions.BookingOrderCancelExceedLimit):
                _logger.exception(e)
                _logger.error('用户今日订单取消次数超限，请明天再重新抢票！')
                os._exit(-2)
            else:
                _logger.exception(e)

        time.sleep(settings.SLEEP_INTERVAL)
