#coding = utf-8

import time

st = "2014-07-07 %d:00:00"

for i in xrange(24):
    ss = st % i
    tt = time.mktime(time.strptime(ss, '%Y-%m-%d %H:%M:%S'))
    print ss
    print int(tt)
