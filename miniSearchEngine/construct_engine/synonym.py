from nltk.corpus import wordnet
import string

def get_synonyms(query, n=5):# 获取查询的同义词，返回值为[[每个词的同义词列表],……]
    punctuations=list(string.punctuation)# 去除标点
    for punctuation in punctuations:
        query = query.replace(punctuation,' ')
    # 去除停词
    query = query.split(' ')# 分隔
    
    if n:
        n += 1
    
    Flag = True
    while Flag:    # 移除空字符串
        for i in query:
            if i == '':
                query.remove(i)
        Flag = False
        for i in query:
            if i == '':
                Flag = True
    
    result = []

    for i in query:
        sym_list=getThesaurus(i, n)
        if sym_list != []:
            result.append(sym_list)

    return result

def getThesaurus(word, n=5):# 返回值为word的同义词列表
    thesaurus = []
    
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            if l.name() in thesaurus:
                pass
            elif "_" in list(l.name()):
                pass
            elif "-" in list(l.name()):
                pass
            else:
                thesaurus.append(l.name())

    if n == None:
        return thesaurus

    if len(thesaurus) > (n+1):
        thesaurus = thesaurus[0:n] # thesaurus[0]即word自身  thesaurus[1:n]是其同义词

    return thesaurus