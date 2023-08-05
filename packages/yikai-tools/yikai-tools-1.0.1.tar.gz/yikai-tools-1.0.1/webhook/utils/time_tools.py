#!/usr/bin/env python
# encoding: utf-8
"""
# @Software: PyCharm
# @Author : 王世锋
# @Email：785707939@qq.com
# @Time：2018/12/29 14:30
# @File : time_tools.py
"""
from datetime import datetime

import pytz as pytz


def utc_to_local(utc_time_str, utc_format='%Y-%m-%d %H:%M:%S UTC'):
    # 将得到的UTC时间转化成北京时间：（假设获得的时间格式为：2018-08-02T14:17:39+00:00）
    local_tz = pytz.timezone('Asia/Shanghai')
    local_format = "%Y-%m-%d %H:%M:%S"
    utc_dt = datetime.strptime(utc_time_str, utc_format)
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    # print(local_dt)
    time_str = local_dt.strftime(local_format)
    return time_str


def str_to_date(timestamp):
    # 2018-08-26T19:26:04+08:00
    # timestamp = "2018-08-26T19:26:04+08:00"
    try:
        date = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S+08:00').strftime("%Y-%m-%d %H:%M:%S")
    except Exception, e:
        return timestamp
    return date
