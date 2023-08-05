#!/usr/bin/env python
# encoding: utf-8
"""
# @Author : 王世锋
# @Email : 785707939@qq.com
# @Time : 2018/12/29 15:09
# @File : tower.py
"""
import sys

from webhook.utils.time_tools import utc_to_local

reload(sys)
sys.setdefaultencoding('utf8')


def _do_data(data, url_cate, action, project_name, project_guid, todos_title):
    """

    :param data:
    :param action:
    :param project_name:
    :param project_guid:
    :param todos_title:
    :return:
    """
    message = u""
    print data
    updated_at = utc_to_local(data["updated_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
    todo_title = data["title"]

    todo_guid = data["guid"]
    url = "https://tower.im/projects/%s/%s/%s/" % (project_guid, url_cate, todo_guid)

    message += u"操作：" + action + u"\n\n"
    message += u"项目：" + project_name + u"\n\n"
    message += u"地址：" + url + u"\n\n"
    message += u"类别：" + todos_title + u"\n\n"
    if data.has_key("comment"):
        comment = data["comment"]
        content = comment["content"]
        message += u"评论：" + content + u"\n\n"
    message += u"更新时间：" + updated_at + u"\n\n"
    message += u"标题：" + todo_title + u"\n\n"

    # 任务独有
    todo_handler = data.get("handler")
    if type(todo_handler) is dict:
        todo_handler_nickname = todo_handler["nickname"]
        message += u"创建人：" + todo_handler_nickname + u"\n\n"

    todo_assignee = data.get("assignee")
    if type(todo_assignee) is dict:
        todo_assignee_nickname = todo_assignee["nickname"]
        message += u"安排人：" + todo_assignee_nickname + u"\n\n"
    return message


def todo(data, title=u"tower 通知"):
    print "tower data is:", data
    action = data["action"]
    data = data["data"]
    project_name = data["project"]["name"]
    project_guid = data["project"]["guid"]

    if data.has_key("todolist"):
        todos_title = u"任务"
        data = data["todo"]
        url_cate = "todos"
    elif data.has_key("document"):
        todos_title = u"文档"
        data = data["document"]
        url_cate = "docs"
    elif data.has_key("attachment"):
        todos_title = u"文件"
        data = data["attachment"]
        url_cate = "uploads"
    elif data.has_key("topic"):
        todos_title = u"讨论"
        data = data["topic"]
        url_cate = "messages"
    message = _do_data(data, url_cate, action, project_name, project_guid, todos_title)
    return title, message
