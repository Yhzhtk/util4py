#coding=utf-8
'''
Created on 2014年8月15日

@author: gudh
'''

import subprocess,sys,os

# 基础的sql语句
base_day_sql = "select %s,count(*) from %s where log_date = %s and %s in (%%s) group by %s"
base_all_sql = "select %s,count(*) from %s where %s in (%%s) group by %s"

# search 表相关统计
s_spc = [('search', 'spc', '搜索类型'), [('0', '联合搜索(0)'), ('1', '职位(1)'), ('2', '职位(2)'), ('3', '公司(3)'), ('4', '公司(4)'), ('5', '城市(5)'), ('', '无(空)')]]
s_label = [('search', 'label_words', '搜索来源'), [('sug', 'Suggest词'), ('hot', '热门搜索词'), ('label', '左侧标签词'), ('label,label', '加筛选条件'), ('', '用户输入')]]
s_salary = [('search', 'monthly_salary', '薪资点击'), [('50k以上', '50k以上'), ('2k-5k', '2k-5k'), ('25k-50k', '25k-50k'), ('5k-10k', '5k-10k'), ('10k-15k', '10k-15k'), ('15k-25k', '15k-25k'), ('', '无')]]
s_experience = [('search', 'working_experience', '工作经验点击'), [('不限', '不限'), ('应届毕业生', '应届毕业生'), ('1年以下', '1年以下'), ('1-3年', '1-3年'), ('3-5年', '3-5年'), ('5-10年', '5-10年'), ('10年以上', '10年以上'), ('', '无')]]
s_educational = [('search', 'educational_background', '教育背景点击'), [('不限', '不限'), ('大专', '大专'), ('本科', '本科'), ('硕士', '硕士'), ('博士', '博士'), ('', '无')]]
s_nature = [('search', 'nature_of_work', '工作性质点击'), [('全职', '全职'), ('兼职', '兼职'), ('实习', '实习'), ('', '无')]]
s_time = [('search', 'publish_time', '时间筛选点击'), [('今天', '今天'), ('3天内', '3天内'), ('一周内', '一周内'), ('一月内', '一月内'), ('', '无')]]
# 页码自动生成0到30页
s_pn = [('search', 'pn', '翻页统计'), []]
s_pn[1].extend([(str(i), '第%d页' % i) for i in range(31)])
s_pn[1].append(('', '无'))

# position 表相关统计
p_source = [('view_position', 'current_source', '职位查看来源'), [('profile_rec', '个人简历页'), ('home_hot', '首页热门'), ('home_latest', '首页最新'), ('home_rec', '首页推荐'), ('rec', '推荐页'), ('company_list', '公司列表页'), ('job_rec', '猜你喜欢'), ('pl', '公司职位列表'), ('position_rec', '相似推荐'), ('company', '公司页'), ('', '无'), ('search', '搜索页')]]

def generate_sql(words, log_date):
    tinfo = words[0]
    params = words[1]
    global base_day_sql, base_all_sql
    sql = ''
    if log_date == '0':
        sql = base_all_sql % (tinfo[1], tinfo[0], tinfo[1], tinfo[1])
    else:
        sql = base_day_sql % (tinfo[1], tinfo[0], log_date, tinfo[1], tinfo[1])
    sql = sql %  ','.join(["'%s'" % word[0] for word in params])
    return sql

def execute_hive(para, log_date, to_file):
    sql = generate_sql(para, log_date)
    hive_sql = '''hive -e "%s"''' % sql
    print 'Execute hive sql:', hive_sql
    result = subprocess.Popen(hive_sql, shell=True, stdout=subprocess.PIPE).stdout.read()
    print result
    print ''
    ress = [res.split("\t") for res in result.split("\n") if res]
    head = []
    value = []
    ratio = []
    total = 0
    for word in para[1]:
        for res in ress:
            if res[0] == word[0]:
                head.append(word[1])
                value.append(int(res[1]))
                total += int(res[1])
                break
        else:
            # 补齐格式
            head.append(word[1])
            value.append(0)
            total += 0
    head.append("总数")
    value.append(total)
    # 计算占比
    ratio = ['%.2f' % (val * 100 / float(total)) + "%"  for val in value]
    # 转成字符串
    value = [str(val) for val in value]
    
    # 打印结果
    tfile = open(to_file, "a")
    rstr = "%s 统计" % para[0][2] + "\n"
    rstr += '\t'.join(head) + "\n"
    rstr +=  '\t'.join(value) + "\n"
    rstr +=  '\t'.join(ratio) + "\n"
    rstr +=  '\n'
    rstr +=  '\n'
    print rstr
    tfile.write(rstr)
    tfile.close()
    
    
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print '请输入两个个参数，第一个表示要统计的日期，如20140808, 当其为0时，则统计所有日期数据的和；第二个参数表示结果输出的文件名'
        sys.exit(0)
    log_date = sys.argv[1]
    to_file = sys.argv[2]
    if not os.path.exists(os.path.dirname(to_file)):
        print '文件路径 %s 不存在，请重新输入' % to_file
        sys.exit(0)
    
#     print generate_sql(s_spc, log_date)
#     print generate_sql(s_label, log_date)
#     print generate_sql(s_salary, log_date)
#     print generate_sql(s_experience, log_date)
#     print generate_sql(s_educational, log_date)
#     print generate_sql(s_nature, log_date)
#     print generate_sql(s_time, log_date)
#     print generate_sql(s_pn, log_date)
#     print generate_sql(p_source, log_date)
    execute_hive(s_spc, log_date, to_file)
    execute_hive(s_label, log_date, to_file)
    execute_hive(s_salary, log_date, to_file)
    execute_hive(s_experience, log_date, to_file)
    execute_hive(s_educational, log_date, to_file)
    execute_hive(s_nature, log_date, to_file)
    execute_hive(s_time, log_date, to_file)
    execute_hive(s_pn, log_date, to_file)
    execute_hive(p_source, log_date, to_file)

