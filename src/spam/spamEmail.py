#encoding=utf-8
'''
Created on 2018年11月23日

@author: cedar
'''

import jieba;
import os;


class spamEmailBayes:
    #获得停用词表
    def getStopWords(self):
        stopList=[]
        for line in open("../data/中文停用词表.txt", 'r', encoding='UTF-8'):
            stopList.append(line[:len(line)-1])
        return stopList;
    #获得词典
    def get_word_list(self,content,wordsList,stopList):
        #分词结果放入res_list
        res_list = list(jieba.cut(content))
        for i in res_list:
            if i not in stopList and i.strip()!='' and i!=None:
                if i not in wordsList:
                    if len(i)>1: # 分词规定长度大于1
                        wordsList.append(i)

                    
    #若列表中的词已在词典中，则加1，否则添加进去
    def addToDict(self,wordsList,wordsDict):
        for item in wordsList:
            if item in wordsDict.keys():
                wordsDict[item]+=1
            else:
                wordsDict.setdefault(item,1)
                            
    def get_File_List(self,filePath):
        filenames=os.listdir(filePath)
        return filenames
    
    #通过计算每个文件中p(s|w)来得到对分类影响最大的10个词
    def getTestWords(self,testDict,spamDict,normDict,normFilelen,spamFilelen):
        wordProbList={}
        for word,num  in testDict.items():
            if word in spamDict.keys() and word in normDict.keys():
                #该文件中包含词个数
                pw_s=spamDict[word]/spamFilelen
                pw_n=normDict[word]/normFilelen
                #wsc:如果小于0.05，则置为0.05
                if pw_n<0.05:
                    pw_n=0.05
                ps_w=pw_s/(pw_s+pw_n) 
                wordProbList.setdefault(word,ps_w)
            if word in spamDict.keys() and word not in normDict.keys():
                pw_s=spamDict[word]/spamFilelen
                pw_n=0.05
                ps_w=pw_s/(pw_s+pw_n) 
                wordProbList.setdefault(word,ps_w)
            if word not in spamDict.keys() and word in normDict.keys():
                pw_s=0.05
                pw_n=normDict[word]/normFilelen
                ps_w=pw_s/(pw_s+pw_n) 
                wordProbList.setdefault(word,ps_w)
            if word not in spamDict.keys() and word not in normDict.keys():
                #若该词不在脏词词典中，概率设为0.4
                wordProbList.setdefault(word,0.4)
        wordProbList=sorted(wordProbList.items(),key=lambda item:item[1],reverse=True)[0:20]
        return (wordProbList)
    
    #计算贝叶斯概率
    def calBayes(self,wordList,spamdict,normdict):
        ps_w=1
        ps_n=1
         
        for word,prob in wordList :
            print(word+"/"+str(prob))
            ps_w*=(prob)
            ps_n*=(1-prob)
        p=ps_w/(ps_w+ps_n)
#         print(str(ps_w)+"////"+str(ps_n))
        return p        


