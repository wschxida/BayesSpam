#encoding=utf-8
'''
Created on 2018年11月23日

@author: cedar
'''

from spam.spamEmail import spamEmailBayes
import re
import json
from flask import Flask
from flask import request

app = Flask(__name__)



# 获得正常邮件、垃圾邮件字典及样本个数
normDict_result_file = r'E:\python_project\BayesSpam\data\normDict_result_file.txt'
spamDict_result_file = r'E:\python_project\BayesSpam\data\spamDict_result_file.txt'
normFilelen_result_file = r'E:\python_project\BayesSpam\data\normFilelen_result_file.txt'
spamFilelen_result_file = r'E:\python_project\BayesSpam\data\spamFilelen_result_file.txt'
# 获得停用词表，用于对停用词过滤
spam = spamEmailBayes()
stopList = spam.getStopWords()
# 获得正常邮件中的词频及样本个数
fl_normDict = open(normDict_result_file, 'r', encoding='UTF-8')
normDict = fl_normDict.read()
normDict = json.loads(normDict)
fl_normDict.close()
fl_normFilelen = open(normFilelen_result_file, 'r', encoding='UTF-8')
normFilelen = fl_normFilelen.read()
normFilelen = json.loads(normFilelen)
fl_normFilelen.close()
# 获得垃圾邮件中的词频及样本个数
fl_spamDict = open(spamDict_result_file, 'r', encoding='UTF-8')
spamDict = fl_spamDict.read()
spamDict = json.loads(spamDict)
fl_normDict.close()
fl_spamFilelen = open(spamFilelen_result_file, 'r', encoding='UTF-8')
spamFilelen = fl_spamFilelen.read()
spamFilelen = json.loads(spamFilelen)
fl_spamFilelen.close()
# testArticleList = [{"id":1,"article_title":"某国有银行山东省分行财务管理人员培训圆满结束","article_abstract":"“两荒并存”的协调很重要,刚性费用要向弹性费用"},
#                    {"id":2,"article_title":"中移在线服务有限公司2019校园","article_abstract":"河北、海南、甘肃、福建、安徽【职位】1. 开发类:软件开发"}]


@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>Home</h1>'

@app.route('/spam', methods=['GET'])
def spam_form():
    return '''<form action="/spam" method="post" align="center">
              <p style="width: 50%; height:50px; margin: 50px auto 0 auto; font-size: 2rem;">垃圾信息判断</p>
			  <textarea  rows="1" cols="120" style="width: 50%; height:400px;margin: 50px auto 0 auto; font-size: 2rem;" name="json_data" title="请输入Json"></textarea>
			  <p><button type="submit" style="width: 10%; height:100px; font-size: 2rem;">测试</button></p>
              </form>'''

@app.route('/spam', methods=['POST'])
def spam():
    # spam类对象
    spam = spamEmailBayes()
    testDict = {}
    # 保存每封邮件中出现的词
    wordsList = []
    wordsDict = {}
    # 保存预测结果,key为文件名，值为预测类别
    testResult = {}
    testDict.clear()
    wordsDict.clear()
    wordsList.clear()
    # 需要从request对象读取表单内容：
    json_data = request.form['json_data']
    json_data = json.loads(json_data)
    for data in json_data:
        article_id = data['id']
        article_title = data['article_title']
        article_abstract = data['article_abstract']
        article_title_abstract = article_title + article_abstract

        rule = re.compile(r"[^\u4e00-\u9fa5]")
        article_title_abstract = rule.sub("", article_title_abstract)
        spam.get_word_list(article_title_abstract, wordsList, stopList)
        spam.addToDict(wordsList, wordsDict)
        testDict = wordsDict.copy()
        # 通过计算每个文件中p(s|w)来得到对分类影响最大的10个词
        wordProbList = spam.getTestWords(testDict, spamDict, normDict, normFilelen, spamFilelen)
        print(wordProbList)
        # Detail =
        # 对每封邮件得到的5个词计算贝叶斯概率
        p = spam.calBayes(wordProbList, spamDict, normDict)
        if (p > 0.8):
            testResult.setdefault(article_id, 1)
        else:
            testResult.setdefault(article_id, 0)
        # for i, ic in testResult.items():
        #     print(i + "/" + str(ic))

    return '''
           <h3>Result:</h3><h3>{}</h3>
           '''.format(testResult)

if __name__ == '__main__':
    app.run()



