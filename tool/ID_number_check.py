#coding=utf-8
'''
Created on 2014年7月22日
身份证校验

可访问 http://codepad.org/lGqMr6Xv，修改身份证号，在线运行校验你的身份证号
@author: gudh
'''

def calc_last_code(id_number):
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2, 1]
    code = None
    if len(id_number) == 17 or len(id_number) == 18:
        sum_num = 0
        for i in xrange(17):
            sum_num += weights[i] * int(id_number[i])
        # 加权求和对11取模，在用12减去模
        remainder = 12 - sum_num % 11
        # remainder 可能为12，所以在取模
        remainder = remainder % 11
        if remainder == 10:
            code = "X"
        else:
            code = str(remainder)
    else:
        print "不是一个有效身份证号，应为18位(可输入前17计算最后一位)，当前%d位" % len(id_number) 
    return code

def check_ID_number(id_number):
    code = calc_last_code(id_number)
    if code:
        # X 可能是大小写
        code = code.upper()
        if code == id_number[-1].upper():
            return True
        else:
            print "验证失败，尾号应为：%s" % code
            return False

def print_ID_info(id_number):
    print "身份证号: %s" % id_number
    if check_ID_number(id_num):
        brith_day = "%s-%s-%s" % (id_num[6 : 10], id_num[10 : 12], id_num[12 : 14])
        sex = "男"
        if int(id_num[-2]) % 2 == 0:
            sex = "女" 
        print "生日：%s" % brith_day
        print "性别：%s" % sex
    
if __name__ == '__main__':
    id_num = "11000119900101001X"
    print_ID_info(id_num)



