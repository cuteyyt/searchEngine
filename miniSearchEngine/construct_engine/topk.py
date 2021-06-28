import pandas as pd
import numpy as np
import time
import os
import math

def Binaryfind(TermList, target):
    start = 0
    end = len(TermList) - 1
    while start < end:
        middle =int((start + end)/ 2)
        midpoint = TermList[middle]
        if midpoint > target:
            end = middle - 1
            if start==end:
                return start
        elif midpoint < target:
            start = middle + 1
            if start==end:
                return start
        else:
            #print("middle",middle) 
            return middle

def get_doc_set(term_dict,term_list):
    term_set=set(term_dict.index)
    doc_set=set()
    for term in term_list:
        if term in term_set:
            docs=eval(term_dict.loc[term]["posting_list"])
            docs=list(docs.keys())
            for doc in docs:
                doc_set.add(doc)
    # print(doc_set)
    return doc_set

#total_doc_num=len(filenames = os.listdir("./tmp_dir"))
def Topk(term_dict,csv_file_path,query,k=10):
    """
    term_dict:存放term_dict的DataFrame   即term_dict=pd.read_csv(term_dict_file)
    csv_file_path:存放vector_model的csv文件夹路径
    query:查询字符串
    k:最多返回k个
    返回值:得分最高的docid列表
    """
    term_list=list(term_dict.index)
    query=query.split(" ")
    query_vector=np.zeros(len(term_list))# 建立查询向量
    doc_set=get_doc_set(term_dict,query)
    for qterm in query:
        idx = Binaryfind(term_list,qterm)
        # print(idx)
        if term_list[idx]==qterm:# 可能词项列表中没有query的词汇
            query_vector[idx]=1
    query_vector_norm= np.linalg.norm(query_vector)
    if sum(query_vector)==0: return [] #如果向量表中没有对应词项，直接返回空列表 
    sim_dict={}# 每个doc对应的的余弦相似度
    filenames = os.listdir(csv_file_path)
    #filenames = sorted(filenames, key=lambda x: int(x.split(".")[0]))
    traversed_files=0
    for file in filenames:
        tmp_df=pd.read_csv(csv_file_path+"/"+file)
        for index,row in tmp_df.iterrows():
            doc_id=traversed_files*100+index+1
            if doc_id in doc_set:
                doc_vector=np.array(row[1:])
                sim_dict[doc_id]=sum(doc_vector*query_vector)/(np.linalg.norm(doc_vector) *query_vector_norm)
        traversed_files+=1
    sim_dict=sorted(sim_dict.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
    topk_list=[]
    for _ in sim_dict[0:k]:
        # print(_)
        if _[1]!=0:
            topk_list.append(_[0])
        else : break;
    # print(sim_dict[0:k])
    return topk_list

def NewTopK(term_dict,vector_model,query,k=10):
    term_list=list(term_dict.index)
    query=query.split(" ")
    term_idx_set=set()
    for qterm in query:
        idx = Binaryfind(term_list,qterm)
        # print(idx)
        if term_list[idx]==qterm:# 可能词项列表中没有query的词汇
            term_idx_set.add(idx)
    if len(term_idx_set)==0: return []  # 如果查询的词在词项词典中不存在，直接返回空列表
    query_vector_norm=math.sqrt(len(query))# 查询向量的模就是根号下查询向量的长度
    doc_vectors=list(vector_model["values"])# [[(5,3),(6,1),(200,1.5)],[(4,0.8),(6,1.2),(100,1.5)]]
    sim_dict={}# 每个doc对应的的余弦相似度
    i=1
    for doc_vector in doc_vectors:
        doc_vector=eval(doc_vector)
        fenzi=0
        doc_vector_norm=0# 文档向量的模
        for x in doc_vector:# x[0]是词项索引，x[1]是tf-idf
            if x[0] in term_idx_set:
                fenzi+=x[1]
            doc_vector_norm+=x[1]*x[1]    
        doc_vector_norm=math.sqrt(doc_vector_norm)
        if fenzi!=0: sim_dict[i]=fenzi/(doc_vector_norm*query_vector_norm) # 如果文档和查询一个匹配都没有，不需要加入词典
        i+=1
    sim_dict=sorted(sim_dict.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
    topk_list=[]
    if len(sim_dict)>k:
        topk_list=sim_dict[0:k]
    else: topk_list=sim_dict
    return topk_list