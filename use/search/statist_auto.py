#coding=utf-8
'''
Created on 2014年7月22日

@author: gudh
'''

import urllib2,time,sys,os
import statist_tosql

save_path = "d:/statist"
statist_show_template = "http://%s/statist/show"
statist_refresh_template = "http://%s/statist/refresh"
search_hosts = ["118.192.75.87:18080"] #["10.7.1.2:18080", "10.7.1.6:18080"]

def get_url_content(url, headers={"User-Agent":"statist_auto 1.0 by delfi"}):
    '''以指定UA获取网页内容'''
    print "# start crawl", url
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()
    return html

def analy_and_refresh(search_host):
    surl = statist_show_template % search_host
    content = get_url_content(surl)
    bname = "%s/%s-%s" % (save_path, search_host.replace(".", "_").replace(":", "_"), time.strftime("%Y_%m_%d_%H_%M_%S"))

    # write source html to file
    hfile = open("%s.html" % bname, "w")
    hfile.write(content)
    hfile.close()
    
    # write sqls to file
    sqls = statist_tosql.generate_all_sql(search_host, content)
    ofile = open("%s.sql" % bname, "w")
    for sql in sqls:
        ofile.write(sql)
        ofile.write("\n")
    print "# write sqls to %s, total %d" % (ofile.name, len(sqls))
    ofile.close()
    
    rurl = statist_refresh_template % search_host
    content = get_url_content(rurl)
    print "#", content

if __name__ == '__main__':
    if len(sys.argv) == 2:
        save_path = sys.argv[1]
        if os.path.exists(save_path):
            for host in search_hosts:
                print "# start analy host ", host
                analy_and_refresh(host)
            print "##### end analy ", time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            print "# Warning: please give a right path param, the path %s is not exist" % save_path
    else:
        print "# Warning: please give a path param, use for save the sql file"

