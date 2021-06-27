import pandas


def k_nearest_for_query(df,query,k=5):
    """
    参数：查询字符串query
    返回值：满足query中的每一词项都相邻不超过k的文档列表
    """
    # query = query.lower().split(" ")
    query = query.split(" ")
    length=len(query)
    i=0
    tmp_list=[]
    while i<length-1: # 获取每邻近的两个单词的k邻近列表
        tmp_list.append(k_nearest_in_doc(df,query[i],query[i+1]))
        i+=1
    # print(tmp_list)
    length = len(tmp_list)
    i=0
    while i<length-1:# 每两个k邻近列表融合
        l2=tmp_list.pop()
        l1=tmp_list.pop()
        tmp_list.append(merge_doc_list(l1,l2,k))
        i+=1
    # print(tmp_list)
    tmp_list=tmp_list[0] # 取出嵌套的列表
    doc_id_list=[triple[0] for triple in tmp_list] # 取出列表的doc_id
    return doc_id_list

def merge_doc_list(list1,list2,k):
    """
    返回docid同时在list1和list2出现,且list1的第一个词项与list2的第二个词项距离小于k的三元组列表
    """
    doclist=[]
    for item1 in list1:
        for item2 in list2:
            if item1[0]==item2[0] and abs(item1[1]-item2[2])<k:
                doclist.append((item1[0],item1[1],item2[2]))
    return  doclist

def k_nearest_in_doc(df,term1,term2,k=5):
    """
    df是term_dict_with_positional_index.csv文件转换成的DataFrame结构
    term1和term2是词项(字符串)
    k是邻近值
    返回值是三元组列表，三元组形式为:(文档编号，词项1在文档中的位置，词项2在文档中的位置)
    """
    answer=[]
    df=df.set_index(["term"])
    dict1=eval((df.loc[term1])["posting_list"])
    dict2=eval((df.loc[term2])["posting_list"])
    #print(dict1)
    #print(dict2)
    k1=list(dict1.keys())
    k2=list(dict2.keys())
    len1=len(k1)
    len2=len(k2)
    i1=0
    i2=0
    while i1<len1 and i2<len2:
        if k1[i1]==k2[i2]:
            l=[]
            t_list1=dict1[k1[i1]] #词项在文档k1[i1]中的位置列表
            t_list2=dict2[k2[i2]] 
            t_list_len1=len(t_list1)
            t_list_len2=len(t_list2)
            t_i1=0
            t_i2=0
            while t_i1<t_list_len1:
                while t_i2<t_list_len2:
                    if abs(t_list1[t_i1]-t_list2[t_i2])<k:# 如果两词项在同一文档中相邻度小于k       
                        l.append(t_list2[t_i2]) # 将与词项1距离小于k的词项2的位置添加到列表中
                    elif t_list2[t_i2]-t_list1[t_i1]>k:break;
                    t_i2+=1;
                while len(l)>0 and abs(l[0]-t_list1[t_i1])>k:
                    del(l[0])
                for pos2 in l:
                    answer.append((k1[i1],t_list1[t_i1],pos2))#添加三元组(文档编号，词项1在文档中的位置，词项2在文档中的位置)至结果中
                t_i1+=1;
            i1+=1
            i2+=1
        elif k1[i1]<k2[i2]:i1+=1
        else : i2+=1     
    return answer

if __name__ == '__main__':
    df=pandas.read_csv("term_dict_with_positional_index.csv")
    print(k_nearest_for_query(df,"Vegetable oil registrations",5))