#coding=utf-8
import re

def regex_one(regex, content, group=1):
    '''正则查找第一个匹配返回指定分组'''
    pattern = re.compile(regex, re.DOTALL)
    match = pattern.search(content)
    return match.group(group)

def regex_all(regex, content, group=1):
    '''正则查找所有匹配返回指定分组'''
    pattern = re.compile(regex, re.DOTALL)
    matchs = pattern.finditer(content)
    return [match.group(group) for match in matchs if match]

def parse_time(content):
    start_reg = "统计开始时间:</strong>(.*?)<"
    update_reg = "统计更新时间:</strong>(.*?)<"
    gen_reg = "统计生成时间:</strong>(.*?)<"
    itime = ["", "", ""]
    itime[0] = regex_one(start_reg, content)
    itime[1] = regex_one(update_reg, content)
    itime[2] = regex_one(gen_reg, content)
    return itime

def parse_kt_map(content):
    area_reg = "职位搜索统计.*?</tr>(.*?)</table>"
    tr_reg = "<tr>(.*?)</tr>"
    td_reg = "<td>(.*?)</td>"
    kt_map = {}
    area = regex_one(area_reg, content)
    tr_list = regex_all(tr_reg, area)
    for tr in tr_list:
        td_list = regex_all(td_reg, tr)
        tlen = len(td_list) / 2
        for i in xrange(tlen):
            k = td_list[i * 2 + 1]
            v = int(td_list[i * 2 + 2])
            kt_map[k] = v
    return kt_map
    
def parse_po_map(content):
    area_reg = "职位ID展现次数.*?</tr>(.*?)</table>"
    tr_reg = "<tr>(.*?)</tr>"
    td_reg = "<td>(.*?)</td>"
    a_reg = "<a id='ad(\\-?\d)'>(\d*)</a>"
    kt_map = {}
    area = regex_one(area_reg, content)
    tr_list = regex_all(tr_reg, area)
    for tr in tr_list:
        td_list = regex_all(td_reg, tr)
        tlen = len(td_list) / 2
        for i in xrange(tlen):
            atag = td_list[i * 2 + 1]
            k1 = regex_one(a_reg, atag, 2)
            k2 = regex_one(a_reg, atag, 1)
            k = "%s_%s" % (k1, k2)
            v = int(td_list[i * 2 + 2])
            kt_map[k] = v
    return kt_map

def merge_map(map1, map2):
    imap = {}
    for k in map1.keys():
        imap[k] = map1[k]
    for k in map2.keys():
        if imap.get(k):
            imap[k] += map2[k]
        else:
            imap[k] = map2[k]
    return imap

def write_map(fname, imap):
    ifile = open(fname, "w")
    keys = imap.keys()
    keys.sort()
    for k in keys:
        ifile.write(k)
        ifile.write("\t")
        ifile.write(str(imap[k]))
        ifile.write("\n")
    ifile.close()

def analy_search(content):
    itime1 = parse_time(content)
    kt_map1 = parse_kt_map(content)
    po_map1 = parse_po_map(content)
    return [itime1, kt_map1, po_map1]

def analy_search_file(fname):
    content = open(fname, "r").read();
    return analy_search(content)

def analy_all_search(content1, content2):
    res1 = analy_search(content1)
    res2 = analy_search(content2)
    all_kt = merge_map(res1[1], res2[1])
    all_po = merge_map(res1[2], res2[2])
    return [all_kt, all_po]

def analy_all_search_file(fname1, fname2):
    content1 = open(fname1, "r").read();
    content2 = open(fname2, "r").read();
    return analy_all_search(content1, content2)


