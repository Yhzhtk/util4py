#coding=utf-8
'''
Created on 2014年7月22日

@author: gudh
'''

import statist_parse
from statist_mode import key_statist,position_statist

def get_key_modes(host, date, keymap):
    keys = keymap.keys()
    keys.sort()
    keymodes = []
    for key in keys:
        try:
            mode = key_statist()
            mode.host = host
            mode.keyword = key
            mode.count = keymap[key]
            mode.date = date
            keymodes.append(mode)
        except Exception, e:
            print e
    return keymodes

def get_position_modes(host, date, keymap):
    keys = keymap.keys()
    keys.sort()
    keymodes = []
    for key in keys:
        try:
            keysplit = key.split("_")
            if len(keysplit) != 2:
                continue
            mode = position_statist()
            mode.host = host
            mode.pid = int(keysplit[0])
            mode.adword = int(keysplit[1])
            mode.count = keymap[key]
            mode.date = date
            keymodes.append(mode)
        except Exception, e:
            print e
    return keymodes

def generate_all_sql(host, content):
    print "# start analy content"
    sqls = []
    try:
        res = statist_parse.analy_search(content)
        date = res[0][0].split(" ")[0]
        print "# start generate key sql"
        keymodes = get_key_modes(host, date, res[1])
        for mode in keymodes:
            sql = mode.tosql()
            sqls.append(sql)
            print sql
        
        print "# start generate position sql"
        positionmodes = get_position_modes(host, date, res[2])
        for mode in positionmodes:
            sql = mode.tosql()
            sqls.append(sql)
            print sql
    except Exception,e:
        print "# Error: may not any search info", e
    return sqls

