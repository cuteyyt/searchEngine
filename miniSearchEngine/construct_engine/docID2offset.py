import pandas as pd
def docID2offset(filename):
    """
    作用：把原来{doc_id:[文档位置]}格式的倒排索引转换成[(offset,[文档位置])]格式
    参数：filename: csv文件路径
    返回值：倒排索引列表
    """
    df=pd.read_csv(filename)
    posting_list=df["posting_list"]
    posting_list=posting_list[:]
    newdict={}
    for index,value in posting_list.items():
        #print(index,value)
        tmp_dict=eval(value)
        keys=list(tmp_dict.keys())
        length=len(keys)
        i=length-1
        tmp_list=[] #把原来的词典变成列表，因为文档id偏移有重复
        while(i>=0):
            if i==0:# 第一项不用减
                tmp_tuple=tuple((keys[0],tmp_dict[keys[0]]))
            else: 
                tmp_tuple=tuple((keys[i]-keys[i-1],tmp_dict[keys[i]]))
            tmp_list.insert(0,tmp_tuple)
            i=i-1
        newdict[index]=tmp_list
    newcolumn=pd.Series(newdict)
    del df["posting_list"]
    df["posting_list"]=newcolumn
    return df
