#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : jeffzhang
# @Time    : 2018/12/26
# @File    : utils.py
# @Desc    : ""

import os
import random
import string
from alioth.lib.controller.controller import start
from alioth.lib.utils.target_parse import target_parse
from alioth.lib.utils.log import logger


class AliothScanner:
    def __init__(self, target, poc):
        self.target = target
        self.poc_name = poc['name']
        self.pocstring = poc['pocstring']
        self.mode = poc['mode']
        self.thread = poc['thread']
        self.poc_file = ''

    def run(self):
        if type(self.target) == str:
            self.target = [self.target]
        self.target = target_parse(self.target)
        if self._save_poc():
            options = (self.target, [self.poc_file], self.thread)
            start(options)

    def _save_poc(self):
        try:
            with open(self._tmp_poc_filename(), 'w') as poc_input:
                poc_input.write(self.pocstring)
                return True
        except Exception as e:
            logger.error("Save poc error: " + str(e))
            return False

    def _tmp_poc_filename(self):
        tmp_path = os.environ.get('TMPDIR')
        tmp_name = ''.join(random.sample(string.ascii_lowercase, 5))
        self.poc_file = "{}_{}{}.py".format(self.poc_name, tmp_path, tmp_name)
        return self.poc_file
