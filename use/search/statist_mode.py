#coding=utf-8
'''
Created on 2014年7月22日

@author: gudh
'''

import time

class key_statist(object):
    '''
    关键字统计数据库映射
    '''
    sql_template = '''insert into key_statist (`host`, `keyword`, `count`, `date`) values ("%s", "%s", %d, "%s");'''
    
    def __init__(self):
        self.id = None
        self.host = "h0"
        self.keyword = ""
        self.count = 0
        self.date = time.strftime("%Y-%m-%d")
    
    def tosql(self):
        sql = key_statist.sql_template % (self.host, self.keyword, self.count, self.date)
        return sql

class position_statist(object):
    '''
    职位统计数据库映射
    '''
    sql_template = '''insert into position_statist (`host`, `pid`, `adword`, `count`, `date`) values ("%s", %d, %d, %d, "%s");'''

    def __init__(self):
        self.id = None
        self.host = ""
        self.pid = 0
        self.adword = 0
        self.count = 0
        self.date = time.strftime("%Y-%m-%d")
    
    def tosql(self):
        sql = position_statist.sql_template % (self.host, self.pid, self.adword, self.count, self.date)
        return sql
