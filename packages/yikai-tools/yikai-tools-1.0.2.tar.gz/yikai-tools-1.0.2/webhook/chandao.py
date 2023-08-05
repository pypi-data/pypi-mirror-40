#!/usr/bin/env python
# encoding: utf-8
"""
# @Author : 王世锋
# @Email : 785707939@qq.com
# @Time : 2018/12/29 14:58
# @File : chandao.py
"""


def action(data, user_dict, title):
    """
    禅道消息处理
    :param data:
    :param user_dict:
    :param title: 消息标题
    :return:
    """
    message = u"# %s通知\n\n" % title
    print user_dict
    at_list = []
    comment = data["comment"]
    phone_user = ""
    for user in user_dict:
        phone = user_dict[user]
        if user in comment or phone in comment:
            at_list.append(phone)
            phone_user += "@%s" % phone
    data["comment"] = u"%s %s" % (comment, phone_user)
    for item in data:
        k = item
        v = data[item]
        message = u"%s - %s : %s\n\n" % (message, k, v)
    return title, message, at_list
