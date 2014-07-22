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
        mode = key_statist()
        mode.host = host
        mode.keyword = key
        mode.count = keymap[key]
        mode.date = date
        keymodes.append(mode)
    return keymodes

def get_position_modes(host, date, keymap):
    keys = keymap.keys()
    keys.sort()
    keymodes = []
    for key in keys:
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
    return keymodes

if __name__ == '__main__':
    res = statist_parse.analy_search_file("d:/s01.txt")
    date = res[0][0].split(" ")[0]
    host = "l1"
    keymodes = get_key_modes(host, date, res[1])
    for mode in keymodes:
        print mode.tosql()
    
    keymodes = get_position_modes(host, date, res[2])
    for mode in keymodes:
        print mode.tosql()
    