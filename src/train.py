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
#保存词频的词典
spamDict={}
normDict={}
#保存每封邮件中出现的词
wordsList=[]
wordsDict={}
#分别获得正常邮件、垃圾邮件及测试文件名称列表
normFileList=spam.get_File_List(r"E:\python_project\BayesSpam\data\normal")
spamFileList=spam.get_File_List(r"E:\python_project\BayesSpam\data\spam")
normDict_result_file = r'E:\python_project\BayesSpam\data\normDict_result_file.txt'
spamDict_result_file = r'E:\python_project\BayesSpam\data\spamDict_result_file.txt'
normFilelen_result_file = r'E:\python_project\BayesSpam\data\normFilelen_result_file.txt'
spamFilelen_result_file = r'E:\python_project\BayesSpam\data\spamFilelen_result_file.txt'
#获取训练集中正常邮件与垃圾邮件的数量
normFilelen=len(normFileList)
spamFilelen=len(spamFileList)
#获得停用词表，用于对停用词过滤
stopList=spam.getStopWords()
#获得正常邮件中的词频
for fileName in normFileList:
    wordsList.clear()
    for line in open("../data/normal/"+fileName, 'r', encoding='UTF-8'):
        #过滤掉非中文字符
        rule=re.compile(r"[^\u4e00-\u9fa5]")
        line=rule.sub("",line)
        #将每封邮件出现的词保存在wordsList中
        spam.get_word_list(line,wordsList,stopList)
    #统计每个词在所有邮件中出现的次数
    spam.addToDict(wordsList, wordsDict)
normDict=wordsDict.copy()  

#获得垃圾邮件中的词频
wordsDict.clear()
for fileName in spamFileList:
    wordsList.clear()
    for line in open("../data/spam/"+fileName, 'r', encoding='UTF-8'):
        rule=re.compile(r"[^\u4e00-\u9fa5]")
        line=rule.sub("",line)
        spam.get_word_list(line,wordsList,stopList)
    spam.addToDict(wordsList, wordsDict)
spamDict=wordsDict.copy()

print(normDict)
print(normFilelen)
print(spamDict)
print(spamFilelen)

fl_normDict = open(normDict_result_file, 'w', encoding='UTF-8')
fl_normDict.write(json.dumps(normDict))
fl_normDict.close()
fl_normFilelen = open(normFilelen_result_file, 'w', encoding='UTF-8')
fl_normFilelen.write(json.dumps(normFilelen))
fl_normFilelen.close()

fl_spamDict = open(spamDict_result_file, 'w', encoding='UTF-8')
fl_spamDict.write(json.dumps(spamDict))
fl_spamDict.close()
fl_spamFilelen = open(spamFilelen_result_file, 'w', encoding='UTF-8')
fl_spamFilelen.write(json.dumps(spamFilelen))
fl_spamFilelen.close()