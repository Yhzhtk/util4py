# coding=utf-8

import socket,urllib,urllib2,re,time

#这里对整个socket层设置超时时间。后续文件中如果再使用到socket，不必再设置
socket.setdefaulttimeout(10)

url = "http://ci.aizhan.com/#key#/"
refer = "http://ci.aizhan.com/#key#/"
cookie = "defaultSiteState=1; allSites=%2C1; userId=184432; userName=244048116%40qq.com; userGroup=1; userSecure=kKyplDhvvyjyCxCkJMoHt6mak%2BMmVDD5vtHoG3jk5mvlq6ZWl5AyQqkkde%2FV%2FrVX; keywordWords=#key#; allWords=#key#"

headers = {
    "Referer" : "http://ci.aizhan.com/",
    "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
    "Cookie" : "defaultSiteState=1; allSites=%2C1; userId=184432; userName=244048116%40qq.com; userGroup=1; userSecure=kKyplDhvvyjyCxCkJMoHt6mak%2BMmVDD5vtHoG3jk5mvlq6ZWl5AyQqkkde%2FV%2FrVX"
}

all_reg = "<div class=\"box_05\">(.*?)<div class=\"page\">"
detail_reg = "blue t_l\"><a.*?>(.*?)</a></td>\\s*?<td align=\"right\">(\\d*?)</td>"

def get_url_content(url, headers={}):
    '''以指定UA获取网页内容'''
    print url
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()
    #html = get_code_str(html)
    return html

def get_az_content(key):
    key = urllib.quote(key)
    headers["Referer"] = refer.replace("#key#", key)
    headers["Cookie"] = cookie.replace("#key#", key)
    turl = url.replace("#key#", key)
    content = get_url_content(turl, headers)
    return content

def regex_one(regex, content, group=1):
    '''正则查找第一个匹配返回指定分组'''
    pattern = re.compile(regex, re.DOTALL)
    match = pattern.search(content)
    return match.group(group)

def regex_all(regex, content):
    '''正则查找所有匹配返回指定分组'''
    pattern = re.compile(regex, re.DOTALL)
    matchs = pattern.finditer(content)
    return ["%s,%s\r" % (match.group(1).replace("<font color=\"#FF0000\">", "").replace("</font>", ""),match.group(2)) for match in matchs if match]

def parse_key_info(content):
    avail_content = regex_one(all_reg, content)
    result = regex_all(detail_reg, avail_content)
    print len(result)
    return result

ofile = open("d:/out.csv", "a")
ifile = open("d:/key.txt", "r")
lines = ifile.readlines()
ifile.close()

for line in lines:
    line = line.strip()
    if line:
        s = get_az_content(line)
        res = parse_key_info(s)
        res = ["%s,%s" % (line, c) for c in res]
        ofile.writelines(res)
        ofile.flush()
        time.sleep(2)
ofile.close()




