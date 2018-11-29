#encoding=utf-8
'''
Created on 2018年11月23日

@author: cedar
'''

from spam.spamEmail import spamEmailBayes
import re
import json



#spam类对象
spam=spamEmailBayes()
spamDict={}
normDict={}
testDict={}
#保存每封邮件中出现的词
wordsList=[]
wordsDict={}
#保存预测结果,key为文件名，值为预测类别
testResult={}
#获得正常邮件、垃圾邮件字典及样本个数
normDict_result_file = r'E:\python_project\BayesSpam\data\normDict_result_file.txt'
spamDict_result_file = r'E:\python_project\BayesSpam\data\spamDict_result_file.txt'
normFilelen_result_file = r'E:\python_project\BayesSpam\data\normFilelen_result_file.txt'
spamFilelen_result_file = r'E:\python_project\BayesSpam\data\spamFilelen_result_file.txt'
#获取测试样本文件列表
testFileList=spam.get_File_List(r"E:\python_project\BayesSpam\data\test")
#获得停用词表，用于对停用词过滤
stopList=spam.getStopWords()
#获得正常邮件中的词频及样本个数
fl_normDict = open(normDict_result_file, 'r', encoding='UTF-8')
normDict = fl_normDict.read()
normDict = json.loads(normDict)
fl_normDict.close()
fl_normFilelen = open(normFilelen_result_file, 'r', encoding='UTF-8')
normFilelen = fl_normFilelen.read()
normFilelen = json.loads(normFilelen)
fl_normFilelen.close()
#获得垃圾邮件中的词频及样本个数
fl_spamDict = open(spamDict_result_file, 'r', encoding='UTF-8')
spamDict = fl_spamDict.read()
spamDict = json.loads(spamDict)
fl_normDict.close()
fl_spamFilelen = open(spamFilelen_result_file, 'r', encoding='UTF-8')
spamFilelen = fl_spamFilelen.read()
spamFilelen = json.loads(spamFilelen)
fl_spamFilelen.close()

# print(normDict)
# print(type(normDict))
# print(normFilelen)
# print(type(normFilelen))
# print(spamDict)
# print(type(spamDict))
# print(spamFilelen)
# print(type(spamFilelen))


# 测试邮件
for fileName in testFileList:
    testDict.clear( )
    wordsDict.clear()
    wordsList.clear()
    for line in open("../data/test/"+fileName, 'r', encoding='UTF-8'):
        rule=re.compile(r"[^\u4e00-\u9fa5]")
        line=rule.sub("",line)
        spam.get_word_list(line,wordsList,stopList)
    spam.addToDict(wordsList, wordsDict)
    testDict=wordsDict.copy()
    #通过计算每个文件中p(s|w)来得到对分类影响最大的10个词
    wordProbList=spam.getTestWords(testDict, spamDict,normDict,normFilelen,spamFilelen)
    print(wordProbList)
    #对每封邮件得到的5个词计算贝叶斯概率
    p=spam.calBayes(wordProbList, spamDict, normDict)
    if(p>0.8):
        testResult.setdefault(fileName,1)
    else:
        testResult.setdefault(fileName,0)

for i,ic in testResult.items():
    print(i+"/"+str(ic))
