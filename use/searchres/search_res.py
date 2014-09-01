#coding=utf-8
'''
Created on 2014年9月1日

@author: gudh
'''

import urllib2, re

base_url = "http://10.7.0.174:18080/search/list_%s"

def get_url_content(url, headers={"User-Agent":"statist_auto 1.0 by delfi"}):
    '''以指定UA获取网页内容'''
    print "# start crawl", url
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()
    return html

def regex_one(regex, content, group=1):
    '''正则查找第一个匹配返回指定分组'''
    pattern = re.compile(regex, re.DOTALL)
    match = pattern.search(content)
    return match.group(group)

def regex_top100(regex, content, group=1):
    '''正则查找所有匹配返回指定分组'''
    pattern = re.compile(regex, re.DOTALL)
    matchs = pattern.finditer(content)
    res = []
    for match in matchs:
        if match:
            res.append(match.group(group))
            if len(res) >= 100:
                break
    return res


def get_parse_pname(key):
    key = urllib2.quote(key, "utf-8")
    content = get_url_content(base_url % key)
    table_reg = "注：推广分含更新时间、公司属性得分</p><table>(.*?)</table>"
    table_str = regex_one(table_reg, content)
    
    pname_reg = "<tr>.*?<a.*?>(.*?)</a>"
    pnames = regex_top100(pname_reg, table_str)
    return pnames

def get_sorted(pnames):
    nmap = {}
    for name in pnames:
        name = name.lower()
        if name in nmap:
            nmap[name] = nmap[name] + 1
        else:
            nmap[name] = 1
    res = []
    for k in nmap:
        res.append([k, nmap[k]])
    res.sort(key=lambda x:x[1], reverse=True)
    return res

def get_search_res_sorted(key):
    r = get_parse_pname(key)
    res = get_sorted(r)
    ss = "【%s】\t" % key
    for rr in res:
        ss += rr[0] + "\t"
    ss += "\n【%s】\t" % key
    for rr in res:
        ss += "%d\t" % rr[1]
    ss += "\n"
    return ss

if __name__ == '__main__':
    f = open("d:/key.txt", "r")
    lines = f.readlines()
    f.close()
    o = open("d:/key_s.txt", "a")
    for key in lines:
        key = key.strip()
        s = get_search_res_sorted(key)
        print s
        o.write(s)
    o.close()
    
    
    
    