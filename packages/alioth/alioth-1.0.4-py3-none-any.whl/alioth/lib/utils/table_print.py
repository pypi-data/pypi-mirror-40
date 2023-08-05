#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : jeffzhang
# @Time    : 2018/12/27
# @File    : table_print.py
# @Desc    : ""

from alioth.lib.utils.prettytable import PrettyTable


def res_table_print(data_list):
    new_table = PrettyTable(["ID", "Target", "PoC", "Result"])
    new_table.align['ID'] = 'l'
    new_table.align['Target'] = 'l'
    new_table.align['PoC'] = 'l'
    new_table.align['Result'] = 'l'
    vid = 0
    for data in data_list:
        vid += 1
        target = data['target'][0]
        name = data['name'][0]
        status = data['status'][0]
        new_table.add_row([vid, target, name, status])
    return new_table
