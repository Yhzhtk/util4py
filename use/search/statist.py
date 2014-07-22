
#coding=utf-8
import re,types

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
    for k in imap.keys():
        ifile.write(k)
        ifile.write("\t")
        ifile.write(str(imap[k]))
        ifile.write("\n")
    ifile.close()

def analy_search(fname1, fname2):
    content1 = open(fname1, "r").read()
    itime1 = parse_time(content1)
    kt_map1 = parse_kt_map(content1)
    po_map1 = parse_po_map(content1)

    print "1 complete"

    content2 = open(fname2, "r").read()
    itime2 = parse_time(content2)
    kt_map2 = parse_kt_map(content2)
    po_map2 = parse_po_map(content2)

    print "2 complete"

    all_kt = merge_map(kt_map1, kt_map2)
    all_po = merge_map(po_map1, po_map2)

    return [itime1, itime2, kt_map1, kt_map2, all_kt, po_map1, po_map2, all_po]

maps = analy_search("d:/s01.txt", "d:/s02.txt")
ii = 0
for imap in maps:
    if type(imap) == type({}):
        fname = "d:/%d.txt" % ii
        ii += 1
        print fname
        write_map(fname, imap)
    else:
        print imap

