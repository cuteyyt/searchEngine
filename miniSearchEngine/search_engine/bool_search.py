BRACKETS_LEFT = "("
BRACKETS_RIGHT = ")"
SPACES_REDUNDANCY = " "
OPT_AND = "&"
OPT_OR = "|"
OPT_NOT = "~"


def dict_to_slice(doc_dict):
    doc_slice = []
    for key in doc_dict:
        doc_slice.append(key)
    return doc_slice


def bool_opt_and(docs1, docs2):
    ret = []
    len1 = len(docs1)
    len2 = len(docs2)
    index2 = 0
    for index1 in range(len1):
        while index2 < len2 and docs2[index2] < docs1[index1]:
            index2 += 1
        if index2 >= len2:
            break
        if docs1[index1] == docs2[index2]:
            ret.append(docs1[index1])
            index2 += 1
    return ret


def bool_opt_or(docs1, docs2):
    ret = []
    len1 = len(docs1)
    len2 = len(docs2)
    index1, index2 = 0, 0
    while index1 < len1 or index2 < len2:
        if index1 >= len1:
            ret.append(docs2[index2])
            index2 += 1
        elif index2 >= len2:
            ret.append(docs1[index1])
            index1 += 1
        elif docs1[index1] < docs2[index2]:
            ret.append(docs1[index1])
            index1 += 1
        elif docs1[index1] > docs2[index2]:
            ret.append(docs2[index2])
            index2 += 1
        else:
            ret.append(docs1[index1])
            index1 += 1
            index2 += 1
    return ret


def bool_opt_not(docs1, max_doc_num=100):
    ret = []
    len1 = len(docs1)
    index = 0
    for doc_id in range(1,max_doc_num):
        if index < len1 and doc_id == docs1[index]:
            index += 1
        else:
            ret.append(doc_id)
    return ret


def bool_search(query_list, term_dict):
    if len(query_list) == 0:
        print("???")
        return

    query_list = query_list.split(' ')

    sta = []

    for word in query_list:
        if word == SPACES_REDUNDANCY or word == "":
            continue

        if word == BRACKETS_LEFT:
            sta.append(BRACKETS_LEFT)
        elif word == BRACKETS_RIGHT:
            if len(sta) < 2 or not isinstance(sta[-1], list) or sta[-2] != BRACKETS_LEFT:
                print("ERROR! Syntax failed!")
                return
            sta.pop(-2)
        elif word == OPT_AND:
            sta.append(OPT_AND)
        elif word == OPT_OR:
            sta.append(OPT_OR)
        elif word == OPT_NOT:
            sta.append(OPT_NOT)
        else:
            if word in term_dict:
                term_slice = dict_to_slice(term_dict[word]['posting_list'])
            else:
                term_slice = []
            sta.append(term_slice)
            print(word, term_slice)

        while isinstance(sta[-1], list):
            if len(sta) >= 2 and isinstance(sta[-2], list):
                sta[-2] = bool_opt_and(sta[-2], sta[-1])
                sta.pop()
            elif len(sta) >=2 and sta[-2] == OPT_NOT:
                sta[-2] = bool_opt_not(sta[-1],100)
                sta.pop()
            elif len(sta) >=3 and sta[-2] == OPT_AND and isinstance(sta[-3], list):
                sta[-3] = bool_opt_and(sta[-3],sta[-1])
                sta.pop()
                sta.pop()
            elif len(sta) >= 3 and sta[-2] == OPT_OR and isinstance(sta[-3], list):
                sta[-3] = bool_opt_or(sta[-3],sta[-1])
                sta.pop()
                sta.pop()
            else:
                break

    if len(sta) > 1 or not isinstance(sta[0], list):
        print("ERROR! Syntax failed!")
        return
    return sta[0]
