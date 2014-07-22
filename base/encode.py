import sys
reload(sys)
oencode = sys.getdefaultencoding()
sys.setdefaultencoding('utf-8')
nencode = sys.getdefaultencoding()
print oencode, " -> ", nencode
