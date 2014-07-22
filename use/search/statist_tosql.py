#coding=utf-8
'''
Created on 2014年7月22日

@author: gudh
'''

import statist_parse,statist_mode
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

def generate_sql_single(modes):
    sqls = []
    for mode in modes:
        sql = mode.tosql()
        sqls.append(sql)
        print sql
    return sqls

def generate_sql_multi(modes):
    sqls = []
    psize = 10
    length = len(modes)
    page = (length - 1) / psize + 1
    for i in xrange(page):
        start = i * psize
        end = start + psize
        if end > length:
            end = length
        tmodes = modes[start:end]
        sql = statist_mode.generate_batch_sql(tmodes)
        sqls.append(sql)
        print sql
    return sqls

def generate_sql(modes):
    return generate_sql_multi(modes)

def generate_all_sql(host, content):
    print "# start analy content"
    sqls = []
    try:
        res = statist_parse.analy_search(content)
        date = res[0][1].split(" ")[0]
        print "# start generate key sql"
        keymodes = get_key_modes(host, date, res[1])
        sqls.extend(generate_sql(keymodes))
        
        print "# start generate position sql"
        positionmodes = get_position_modes(host, date, res[2])
        sqls.extend(generate_sql(positionmodes))
        
    except Exception,e:
        print "# Error: may not any search info | ", e
    return sqls

