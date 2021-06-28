from nltk.corpus import wordnet
import string

def merge_synonyms_list(sym_list):
    sym_list=[" ".join(sym) for sym in sym_list]
    return " ".join(sym_list)

def get_synonyms(query, n=5):
    """
    query:查询字符串 如"term1 term2 term3"
    n:每个term最多返回n个同义词(注意term自身也算在里面)
    返回值:所有term的同义词组成的字符串，用空格隔开
    """
    #punctuations=list(string.punctuation)# 去除标点
    #for punctuation in punctuations:
    #    query = query.replace(punctuation,' ')
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
    return merge_synonyms_list(result)

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
    if len(thesaurus)==0:# 没找到同义词
        thesaurus = [word]
    return thesaurus