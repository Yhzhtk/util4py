# import code for encoding urls and generating md5 hashes
import urllib, hashlib

def gravatar_url(email = "yhzhtk@gmail.com", size = 40, default = ""):
    ''' email 需要获取头像URL的邮箱，size 获取的尺寸大小， default 当该邮箱不存在时使用默认URL '''
    # 拼接URL
    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    param = {'s':str(size)}
    if default:
        param['d'] = default
    gravatar_url += urllib.urlencode(param)
    return gravatar_url

# 设定邮箱打印出头像URL
email = "yhzhtk@gmail.com"
print gravatar_url(email)
