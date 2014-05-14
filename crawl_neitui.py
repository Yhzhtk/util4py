
# encoding=utf-8


import urllib,urllib2,re,traceback,time

header = {"Referer" : "http://www.neitui.me"}

infos_reg = "<div class=\"jobmore\">(.*?)</div>"
time_reg = "<span class=\"createtime\">(.*?)</span>"
count_reg = "<span class=\"viewcounts\">(\\d*?)</span>"
resume_reg = "<span class=\"resumecounts\">(.*?)</span>"

pname_reg = "<div class=\"jobnote\">.*?@(.*?)\).*?<b>(.*?)</b>"
cname_reg = "<div class=\"company_name\"> <strong><a .*?>(.*?)</a>"


def nt(s=60000, e=70000):
    outfile = open("neitui6-7.txt", "a")
    for i in xrange(s, e):
        time.sleep(0.2)
        print i
        res = neitui(i)
        if res:
            try:
                outfile.write(str(i))
                outfile.write("\t")
                for j in xrange(1, 7):
                    outfile.write(res[j])
                    outfile.write("\t")
                outfile.write(res[0])
                outfile.write("\n")
                outfile.flush()
            except:
                print "write error: "
    outfile.close

def neitui(id):
    res = []
    try:
        content = crawl_neitui(id)
        res = parse_neitui(content)
        return res
    except:
        # traceback.print_exc()
        print "parse error, id: ", id
    return None

def crawl_neitui(id):
    url = "http://www.neitui.me/j/%d" % id

    return get_url_content(url, header)

def parse_neitui(content):
    res = []
    infos = regex_one(infos_reg, content)

    res.append(infos)
    res.append(regex_one(time_reg, infos))
    res.append(regex_one(count_reg, infos))
    res.append(regex_one(resume_reg, infos))

    res.append(regex_one(pname_reg, content, 1))
    res.append(regex_one(pname_reg, content, 2))

    try:
        res.append(regex_one(cname_reg, content))
    except:
        pass
    return res

def get_url_content(url, headers={}):
    '''以指定UA获取网页内容'''
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()
    html = get_code_str(html)
    return html

def print_local_info():
    '''打印本机的UA和IP信息'''
    ip_url = "http://iframe.ip138.com/ic.asp"
    content = get_url_content(ip_url)
    ip = regex_one('''<center>(.*?)</''', content)
    print "IP:" + ip
    
    ua_url = "http://useragentstring.com/"
    content = get_url_content(ua_url)
    ua = regex_one('''<textarea name='uas' id='uas_textfeld' rows='4' cols='30'>(.*?)<''', content)
    print "UA:" + ua

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

def get_code_str(s, ts="utf-8", cs="utf-8"):
    '''获取指定编码'''
    return str(s).decode(ts).encode(cs)

nt()

