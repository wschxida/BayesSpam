# -*- coding: utf-8 -*-
'''
Created on 2018年11月23日

@author: cedar
'''

import pymysql


# 连接mysql
config = {
    'host': '192.168.1.116',
    'port': 3306,
    'user': 'root',
    'passwd': 'poms@db',
    'db':'mymonitor',
    'charset':'utf8mb4',
    'cursorclass':pymysql.cursors.DictCursor
    }
conn = pymysql.connect(**config)
# conn.autocommit(1)
# 使用cursor()方法获取操作游标
cur = conn.cursor()

# 1.查询操作
# 编写sql 查询语句
sql = """
select ad.Article_Title,ac.Article_Abstract,ac.Article_Content
from article_detail ad,article_content ac
where ad.Record_MD5_ID=ac.Article_Record_MD5_ID
and ad.extracted_time>DATE_SUB(CURRENT_DATE(),INTERVAL 2 day)
and ad.Website_No='S0051'
and ac.article_content is not null
and ac.article_content !=''
and ac.article_content not like'%<%'
limit 200
"""

path = "E:\\python_project\\BayesSpam\\data\\normal\\"

try:
    cur.execute(sql)  # 执行sql语句

    results = cur.fetchall()  # 获取查询的所有记录
    # 遍历结果
    article_title_set = ''
    i = 0
    for row in results:
        # website_no = row['website_no']
        article_title = row['Article_Title']
        Article_Abstract = row['Article_Abstract']
        Article_Content = row['Article_Content']
        i +=1
        file_name = path + str(i) + '.txt'
        fn = open(file_name, 'w', encoding='UTF-8')  # 打开文件
        if article_title:
            fn.write(article_title)
            fn.write('\n')
        if Article_Abstract:
            fn.write(Article_Abstract)
            fn.write('\n')
        if Article_Content:
            fn.write(Article_Content)
            fn.write('\n')
        fn.close()  # 关闭文件

except Exception as e:
    raise e
finally:
    conn.close()  # 关闭连接

