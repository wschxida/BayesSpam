# -*- coding: utf-8 -*-
'''
Created on 2018年11月23日

@author: cedar
'''

import pymysql


# 连接mysql
config = {
    'host': '192.168.1.166',
    'port': 3306,
    'user': 'root',
    'passwd': 'poms@db',
    'db':'test',
    'charset':'utf8mb4',
    'cursorclass':pymysql.cursors.DictCursor
    }
conn = pymysql.connect(**config)
# conn.autocommit(1)
# 使用cursor()方法获取操作游标
cur = conn.cursor()

# 1.查询操作
# 编写sql 查询语句
sql = "select Article_Title,Article_Abstract,Article_Content from invalid_article"
path = "E:\\python_project\\BayesSpam\\data\\spam\\"

try:
    cur.execute(sql)  # 执行sql语句

    results = cur.fetchall()  # 获取查询的所有记录
    # 遍历结果
    article_title_set = ''
    i = 0
    for row in results:
        # website_no = row['website_no']
        Article_Title = row['Article_Title']
        Article_Abstract = row['Article_Abstract']
        Article_Content = row['Article_Content']
        i +=1
        file_name = path + str(i) + '.txt'
        fn = open(file_name, 'w', encoding='UTF-8')  # 打开文件
        if Article_Title:
            fn.write(Article_Title)
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

