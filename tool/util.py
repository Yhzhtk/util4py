# coding=utf-8
'''
Created on 2013-11-24

@author: gudh
'''

import urllib2

def get_baidu_redirect(url):
    '''获取百度的302跳转'''
    headers = {
               "User-Agent" : "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36",
               "Referer" : "http://www.baidu.com"
    }
    req = urllib2.Request(url, None, headers)
    inf = urllib2.urlopen(req)
    return inf.url

def convert_unicode(str):
    '''unicode转中文'''
    return str.decode('unicode_escape')
    
if __name__ == '__main__':
    #url = "http://www.baidu.com/zhixin.php?url=Wx_K000Zo_Nj0_Byu7bTs6b58kpV60VWGVTvX5k-KSGu_kjhW7gPu0cVos7IMB7HZOyP5zed-SzoRCvW9dkSeKIqrYx4XkLmbBksHsnzpPOwyUNM0Jr4zLyn6qmkB511zIas4wC.Db_Khqlx0BKhqva9QY2N9h9mzyTTMD0.THLHCV5EkXjwVfKYTh7buy-b5HmL0APETLwxTh78p1YdP6K1IyFkpyfqnHn3PHnsnj6YnWmsPH0sn0K-IZ-suHYknjD0uy-b5HTzP1nY0ANbugPWpyfqn0KWUA-WpdqYXgK-5Hc0TA3qn6KYugFVpy49UjYs0ZGY5gP-UAm0mLFW5HfYnjcv&ck=7723.514.136.285.125.709.191.344"
    #print get_302(url)
    str = "\u4e09\u5143\u6865\u4e2d\u5fc3"
    print convert_unicode(str)


