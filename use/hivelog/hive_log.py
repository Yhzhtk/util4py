#coding=utf-8
'''
Created on 2014年8月15日

@author: gudh
'''

import subprocess

# 基础的sql语句
base_sql = "select %s,count(*) from %s where %s in (%%s) group by %s"

# search 表相关统计
s_spc = [('search', 'spc', '搜索类型'), [('0', '公司职位'), ('1', '职位'), ('2', '职位'), ('3', '公司'), ('4', '公司'), ('5', '城市'), ('', '无')]]
s_label = [('search', 'label_words', '搜索来源'), [('sug', 'Suggest词'), ('hot', '热门搜索词'), ('label', '左侧标签词'), ('label,label', '加筛选条件'), ('', '用户输入')]]
s_salary = [('search', 'monthly_salary', '薪资点击'), [('50k以上', '50k以上'), ('2k-5k', '2k-5k'), ('25k-50k', '25k-50k'), ('5k-10k', '5k-10k'), ('10k-15k', '10k-15k'), ('15k-25k', '15k-25k'), ('', '无')]]
s_experience = [('search', 'working_experience', '工作经验点击'), [('不限', '不限'), ('应届毕业生', '应届毕业生'), ('1年以下', '1年以下'), ('1-3年', '1-3年'), ('3-5年', '3-5年'), ('5-10年', '5-10年'), ('10年以上', '10年以上'), ('', '无')]]
s_educational = [('search', 'educational_background', '教育背景点击'), [('不限', '不限'), ('大专', '大专'), ('本科', '本科'), ('硕士', '硕士'), ('博士', '博士'), ('', '无')]]
s_nature = [('search', 'nature_of_work', '工作性质点击'), [('全职', '全职'), ('兼职', '兼职'), ('实习', '实习'), ('', '无')]]
s_time = [('search', 'publish_time', '时间筛选点击'), [('今天', '今天'), ('3天内', '3天内'), ('一周内', '一周内'), ('一月内', '一月内'), ('', '无')]]
# 页码自动生成0到30页
s_pn = [('search', 'pn', '翻页统计'), []]
s_pn[1].extend([(str(i), '第%d页' % i) for i in range(31)])
s_pn.append(('', '无'))

# position 表相关统计
p_source = [('view_position', 'current_source', '职位查看来源'), [('profile_rec', '个人简历页'), ('home_hot', '首页热门'), ('home_latest', '首页最新'), ('home_rec', '首页推荐'), ('rec', '推荐页'), ('company_list', '公司列表页'), ('job_rec', '猜你喜欢'), ('pl', '公司职位列表'), ('position_rec', '相似推荐'), ('company', '公司页'), ('', '无'), ('search', '搜索页')]]

def generate_sql(words):
    tinfo = words[0]
    params = words[1]
    global base_sql
    sql = base_sql % (tinfo[1], tinfo[0], tinfo[1], tinfo[1])
    sql = sql %  ','.join(["'%s'" % word[0] for word in params])
    return sql

def execute_hive(para):
    sql = generate_sql(para)
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
    head.append("总数")
    value.append(total)
    # 计算占比
    ratio = ['%.2f' % (val * 100 / float(total)) + "%"  for val in value]
    # 转成字符串
    value = [str(val) for val in value]
    
    # 打印结果
    print "统计分析 %s 信息" % para[0][2]
    print '\t'.join(head)
    print '\t'.join(value)
    print '\t'.join(ratio)
    print ''
    print ''
    
    
if __name__ == '__main__':
#     print generate_sql(s_spc)
#     print generate_sql(s_label)
#     print generate_sql(s_salary)
#     print generate_sql(s_experience)
#     print generate_sql(s_educational)
#     print generate_sql(s_nature)
#     print generate_sql(s_time)
#     print generate_sql(s_pn)
#     print generate_sql(p_source)
    execute_hive(s_spc)
    execute_hive(s_label)
    execute_hive(s_salary)
    execute_hive(s_experience)
    execute_hive(s_educational)
    execute_hive(s_nature)
    execute_hive(s_time)
    execute_hive(s_pn)
    execute_hive(p_source)

