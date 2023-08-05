#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : jeffzhang
# @Time    : 2018/12/25
# @File    : poc.py
# @Desc    : ""

from alioth.lib.core.data import SCAN_RESULT
from alioth.lib.utils.log import logger


class BasePoc:
    """
    PoC 插件父类 PoC 插件必须继承于 BasePoc
    """
    id = None
    name = None
    author = None
    app = None
    type = None
    desc = None
    date = None

    def __init__(self, target, mode='verify'):
        self.target = target
        self.mode = mode
        self.success_count = SCAN_RESULT.SUCCESS_COUNT

    def _verify(self, *args, **kwargs):
        pass

    def _attack(self,  *args, **kwargs):
        pass

    def run(self,  **kwargs):
        # 判断插件模式
        if self.mode == 'verify':
            return self._verify(**kwargs)
        elif self.mode == 'attack':
            return self._attack(**kwargs)


class Output(object):
    """
    结果输出
    """
    def __init__(self, poc_info=None):
        self.result = {}
        self.id = ''
        self.name = ''
        self.target = ''
        self.mode = ''
        if poc_info:
            self.id = poc_info.id
            self.name = poc_info.name
            self.target = poc_info.target
            self.mode = poc_info.mode

    def success(self, result):
        self.result = result
        self.result['target'] = self.target,
        self.result['name'] = self.name,
        self.result['status'] = 'success',
        SCAN_RESULT.SUCCESS_COUNT += 1
        SCAN_RESULT.RESULT.append(self.result)
        msg = "{} {} [{}] is vulnerable".format(self.mode.capitalize(), self.target, self.name)
        logger.success(msg)

    def fail(self, error=""):
        self.result['target'] = self.target,
        self.result['name'] = self.name,
        self.result['status'] = 'failed',
        SCAN_RESULT.RESULT.append(self.result)
        msg = "{} {} [{}] failed: {}".format(self.mode.capitalize(), self.target, self.name, error)
        logger.warning(msg)
