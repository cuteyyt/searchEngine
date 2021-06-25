from preprocess import preprocess_for_text
import pandas as pd
import numpy as np


def Binaryfind(TermList, target):
    start = 0
    end = len(TermList) - 1
    while start <= end:
        middle =int((start + end)/ 2)
        midpoint = TermList[middle]
        if midpoint > target:
            end = middle - 1
        elif midpoint < target:
            start = middle + 1
        else:
            return middle

def TopK(query,vector_model_file,k=10):
    """
    query:查询字符串
    vector_model_file:向量空间文件名
    k:最相关k篇
    返回值:最相关k篇的docID组成的列表
    """
    df=pd.read_csv(open(vector_model_file))
    term_list=list(df.columns[1:])
    #query=preprocess_for_text(args,query)
    query = query.split(" ")
    query_vector=np.zeros(len(term_list))
    for qterm in query:
        idx = Binaryfind(term_list,qterm)
        if term_list[idx]==qterm:# 可能词项列表中没有query的词汇
            query_vector[idx]=1
    sim_dict={}# 每个doc对应的的余弦相似度
    for index, row in df.iterrows():
        doc_vector=np.array(row)[1:]
        sim_dict[index+1]=sum(doc_vector*query_vector)/np.linalg.norm(doc_vector) * np.linalg.norm(query_vector)
    #print(dot_dict)
    sim_dict=sorted(sim_dict.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
    topk_list=[]
    for _ in sim_dict[0:k]:
        topk_list.append(_[0])
    return topk_list

# print(TopK("Prime Minister","../../vector_model.csv"))