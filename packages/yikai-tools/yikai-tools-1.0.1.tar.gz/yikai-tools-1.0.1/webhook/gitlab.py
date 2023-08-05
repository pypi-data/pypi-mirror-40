#!/usr/bin/env python
# encoding: utf-8
"""
# @Author : 王世锋
# @Email : 785707939@qq.com
# @Time : 2018/12/29 14:27
# @File : gitlab.py
"""
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from webhook.utils.time_tools import utc_to_local, str_to_date


def push(data, user_dict):
    """
    处理push消息
    :param data: gitlab push 操作获取的 webhook 数据
    :param user_dict: 系统的用户信息，json or dict格式
    :return: 比如：
wsf 推送代码到 分支 master
系统：yikai_tools
内容：
6f03b08e72: 1. 推送的消息内容 【2018-12-29 11:36:39】 【wsf】
    """
    commit_message_lists = []
    before = data["before"][0:10]
    after = data["after"][0:10]
    push_event = u"推送代码到"
    if before == "0000000000":
        push_event = u"创建"
    if after == "0000000000":
        push_event = u"删除"
    repository_name = data["repository"]["name"]

    commits_list = data["commits"]
    ref = str(data["ref"]).replace("refs/heads/", "")
    i = 0
    for commit in commits_list:
        i += 1
        message = commit["message"]
        timestamp = commit["timestamp"]
        try:
            author_name = user_dict[commit["author"]["name"]]
        except KeyError:
            author_name = commit["author"]["name"]
        id = commit["id"][0:10]
        url = commit["url"]
        commit_message_lists.append(u"[%s](%s): [%s.](%s) %s 【%s】\n【%s】\n\n" %
                                    (id, url, i, url, message,
                                     utc_to_local(str_to_date(timestamp), "%Y-%m-%dT%H:%M:%SZ"),
                                     author_name))
    title = u"%s %s 分支 %s\n" % (author_name, push_event, ref)
    message = u"# %s\n ## 系统：%s\n ## 内容：\n\n %s" % \
              (title, repository_name, "".join(commit_message_lists))
    return title, message


def merge_request(data, user_dict):
    """
    处理merge_request消息
    :param data: gitlab merge_request 操作获取的 webhook 数据
    :param user_dict: 系统的用户信息，json or dict格式
    :return: 比如：
    wsf 合并分支dev 到 test
系统：yikai_tools
操作时间: 2018-12-28 14:35:30 完成时间: 2018-12-28 14:35:34
状态: 可以合并,已经合并
标题: 修改代码
内容: 修改代码 【2018-12-28 14:19:05】 【wsf】
    """
    repository_name = data["repository"]["name"]
    try:
        author_name = user_dict[data["user"]["name"]]
    except KeyError:
        author_name = data["user"]["name"]

    object_attributes = data["object_attributes"]
    source_branch = object_attributes["source_branch"]
    target_branch = object_attributes["target_branch"]
    created_at = utc_to_local(object_attributes["created_at"])
    updated_at = utc_to_local(object_attributes["updated_at"])
    commit_title = object_attributes["title"]

    last_commit = object_attributes["last_commit"]
    action_message = last_commit["message"]
    action_time = last_commit["timestamp"]
    last_author = last_commit["author"]["name"]

    merge_status = object_attributes["merge_status"]
    state = object_attributes["state"]
    if merge_status == "unchecked" and state == "opened":
        merge_message = u"申请合并提交"
    elif merge_status == "can_be_merged" and state == "merged":
        merge_message = u"可以合并,已经合并"
    else:
        merge_message = u"不能合并"
    url = last_commit["url"]
    title = u"%s 合并分支%s 到 %s\n" % (author_name, source_branch, target_branch)
    message = u"# %s 系统：%s\n\n" \
              u"\n操作时间: %s\n完成时间: %s\n\n" \
              u"状态: %s\n\n" \
              u"[标题](%s): %s\n\n" \
              u"[内容](%s): %s 【%s】 【%s】" % \
              (title, repository_name, created_at, updated_at, merge_message,
               url, commit_title, url,
               action_message, utc_to_local(str_to_date(action_time), "%Y-%m-%dT%H:%M:%SZ"), last_author)
    return title, message
