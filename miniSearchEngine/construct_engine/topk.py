import pandas as pd
import numpy as np
import time
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
        start=time.time()
        tmp_df=pd.read_csv(csv_file_path+"/"+file)
        print("read_csv:",time.time()-start)
        strat = time.time()
        for index,row in tmp_df.iterrows():
            doc_id=traversed_files*100+index+1
            if doc_id in doc_set:
                doc_vector=np.array(row[1:])
                sim_dict[doc_id]=sum(doc_vector*query_vector)/(np.linalg.norm(doc_vector) *query_vector_norm)
        # print("calculate:",time.time()-start)
        traversed_files+=1
    sim_dict=sorted(sim_dict.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
    topk_list=[]
    for _ in sim_dict[0:k]:
        # print(_)
        if _[1]!=0:
            topk_list.append(_[0])
        else : break;
    print(sim_dict[0:k])
    return topk_list
