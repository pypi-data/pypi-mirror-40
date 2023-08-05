#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : jeffzhang
# @Time    : 2018/12/26
# @File    : target_parse.py
# @Desc    : ""

import re
import ipaddress
from alioth.lib.utils.log import logger


def target_parse(target_list):
    new_target_list = []
    for target in target_list:
        if target in new_target_list:
            continue
        target = target.strip()
        re_ip = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
        re_ips = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$')
        re_url = re.compile('[^\s]*.[a-zA-Z]')
        re_ip_port = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$')
        re_url_port = re.compile('[^\s]*.[a-zA-Z]:\d{1,5}')

        if re_ip.match(target):
            new_target_list.append(target)

        # 如果是网络段 转换成IP
        elif re_ips.match(target):
            try:
                ip_list = ipaddress.ip_network(target)
                for ip in ip_list.hosts():
                    new_target_list.append(str(ip))
            except Exception as e:
                logger.error("IP address is not standardized: " + str(e))
                logger.error("Example: 192.168.111.0/24")

        elif re_url.match(target):
            new_target_list.append(url_parse(target))

        elif re_ip_port.match(target):
            new_target_list.append(target)

        elif re_url_port.match(target):
            new_target_list.append(target)
    return new_target_list


def url_parse(url):
    if "http" != url[0:4]:
        url = "http://" + url
    return url
