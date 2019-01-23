#encoding=utf-8
'''
Created on 2018年11月30日

@author: cedar
'''

from flask import Flask
from flask import request
import pymysql
import hashlib



app = Flask(__name__)


##插入
def insert(title,abstract,content,record_md5):
    conn = pymysql.connect(user='root', passwd='poms@db',
                     host='192.168.1.166', db='test',charset='utf8mb4')
    cur = conn.cursor()
    sql= "INSERT IGNORE INTO Invalid_Article (article_title,article_abstract,article_content,record_md5_id) VALUES ('{}','{}','{}','{}')".format(title,abstract,content,record_md5)
    print(sql)
    sta=cur.execute(sql)
    if sta==1:
        print('Done')
    else:
        print('Failed')
    conn.commit()
    cur.close()
    conn.close()


@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>Home</h1>'

@app.route('/invalid_article', methods=['GET'])
def invalid_form():
    return '''<form action="/invalid_article" method="post" align="center">
              <h1 style="width: 50%; height:50px; margin: 50px auto 0 auto; font-size: 2rem;">杂信息样本记录</h1>
			  </br></br><span style="font-size: 1rem;">*标题:</span></br>
			  <textarea  rows="1" cols="120" style="width: 50%; height:50px;margin: 0 auto 10px auto; font-size: 1.5rem;" name="article_title" title="请输入标题"></textarea>
			  </br><span style="font-size: 1rem;">*摘要:</span></br>
			  <textarea  rows="5" cols="120" style="width: 50%; height:100px;margin: 0 auto 10px auto; font-size: 1rem;" name="article_abstract" title="请输入摘要"></textarea>
              </br><span style="font-size: 1rem;"> 正文:</span></br>
			  <textarea  rows="100" cols="120" style="width: 50%; height:200px;margin: 0 auto 10px auto; font-size: 1rem;" name="article_content" title="请输入正文"></textarea>
              <p><button type="submit" style="width: 10%; height:50px; font-size: 1rem;">记录存档</button></p>
              </form>'''

@app.route('/invalid_article', methods=['POST'])
def invalid():
    article_title = request.form['article_title']
    article_abstract = request.form['article_abstract']
    article_content = request.form['article_content']
    record_md5_source = article_title + article_abstract + article_content
    m2 = hashlib.md5()
    m2.update(record_md5_source.encode('utf-16LE'))
    record_md5_id = m2.hexdigest()
    insert(article_title, article_abstract, article_content, record_md5_id)

    return '''<h3>文章</h3> <h3>{}</h3> <h3>已存档</h3>'''.format(article_title)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)



