#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .tpcir import *

def purchaseContract_update(token):
    '''
    采购合同反写入口函数
    :param token: ERP数据库token
    :return:
    '''

    res=sql_update(token)

    return res