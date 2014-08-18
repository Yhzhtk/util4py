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
s_spc = [('search', 'spc', '搜索类型', 's_spc'), [('0', '联合搜索(0)', 'spc0'), ('1', '职位(1)', 'spc1'), ('2', '职位(2)', 'spc2'), ('3', '公司(3)', 'spc3'), ('4', '公司(4)', 'spc4'), ('5', '城市(5)', 'spc5'), ('', '无(空)', 'empty')]]
s_label = [('search', 'label_words', '搜索来源', 's_label'), [('sug', 'Suggest词', 'sug'), ('hot', '热门搜索词', 'hot'), ('label', '左侧标签词', 'label'), ('label,label', '加筛选条件', 'label_lable'), ('', '用户输入', 'empty')]] 
s_salary = [('search', 'monthly_salary', '薪资点击', 's_salary'), [('2k以下', '2k以下', '_2'), ('50k以上', '50k以上', '50_'), ('2k-5k', '2k-5k', '2_5'), ('25k-50k', '25k-50k', '25_50'), ('5k-10k', '5k-10k', '5_10'), ('10k-15k', '10k-15k', '10_15'), ('15k-25k', '15k-25k', '15_25'), ('', '无', 'empty')]]
s_experience = [('search', 'working_experience', '工作经验点击', 's_experience'), [('不限', '不限', 'any'), ('应届毕业生', '应届毕业生', '_0'), ('1年以下', '1年以下', '_1'), ('1-3年', '1-3年', '1_3'), ('3-5年', '3-5年', '3_5'), ('5-10年', '5-10年', '5_10'), ('10年以上', '10年以上', '10_'), ('', '无', 'empty')]]
s_educational = [('search', 'educational_background', '教育背景点击', 's_educational'), [('不限', '不限', 'any'), ('大专', '大专', 'zhuan'), ('本科', '本科', 'ben'), ('硕士', '硕士', 'shuo'), ('博士', '博士', 'bo'), ('', '无', 'empty')]]
s_nature = [('search', 'nature_of_work', '工作性质点击', 's_nature'), [('全职', '全职', 'quan'), ('兼职', '兼职', 'jian'), ('实习', '实习', 'shi'), ('', '无', 'empty')]]
s_time = [('search', 'publish_time', '时间筛选点击', 's_time'), [('今天', '今天', '_0'), ('3天内', '3天内', '_3'), ('一周内', '一周内', '_7'), ('一月内', '一月内', '_30'), ('', '无', 'empty')]]
# 页码自动生成0到30页
s_pn = [('search', 'pn', '翻页统计', 's_pn'), []]
s_pn[1].extend([(str(i), '第%d页' % i, str(i)) for i in range(31)])
s_pn[1].append(('', '无', 'empty'))

# position 表相关统计
p_source = [('view_position', 'current_source', '职位查看来源', 'p_source'), [('profile_rec', '个人简历页', 'profile_rec'), ('home_hot', '首页热门', 'home_hot'), ('home_latest', '首页最新', 'home_latest'), ('home_rec', '首页推荐', 'home_rec'), ('rec', '推荐页', 'rec'), ('company_list', '公司列表页', 'company_list'), ('job_rec', '猜你喜欢', 'job_rec'), ('pl', '公司职位列表', 'pl'), ('position_rec', '相似推荐', 'position_rec'), ('company', '公司页', 'company'), ('', '无', 'empty'), ('search', '搜索页', 'search')]]

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

def export_sql(para, values):
    sql = "insert into %s (%s) values (%s)"
    table_name = para[0][3]
    fields = ','.join([ v[2] for v in para[1]])
    values = ','.join(values)
    sql = sql % (table_name, fields, values)
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
    rstr += "insert into %s values (%s)" % (para.__name__, ",".join(value))
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

