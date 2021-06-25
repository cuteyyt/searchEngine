def k_nearest_in_doc(df,term1,term2,k=5):
    """
    df是term_dict_with_positional_index.csv文件转换成的DataFrame结构
    term1和term2是词项(字符串)
    k是邻近值
    返回值是三元组列表，三元组形式为:(文档编号，词项1在文档中的位置，词项2在文档中的位置)
    """
    answer=[]
    dict1=eval(df[term1].iloc[1])
    dict2=eval(df[term2].iloc[1])
    print(dict1)
    print(dict2)
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