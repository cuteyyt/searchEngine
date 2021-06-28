import json
import os
import time
from tqdm import tqdm
from easydict import EasyDict

import pandas as pd

from .index_compression import restore_dict


def find_pos_in_str(zi, mu):
    len1 = len(zi)
    pl = []
    for each in range(len(mu) - len1):
        if mu[each:each + len1] == zi:  # 找出与子字符串首字符相同的字符位置
            pl.append(each)
    return pl


def insert_term2dict(term, _dict, doc_id, pos_id):
    if term != "":
        if term not in _dict.keys():
            _dict[term] = dict()
            _dict[term]['doc_feq'] = 1
            _dict[term]['posting_list'] = dict()  # This is for future modification
            _dict[term]['posting_list'][doc_id] = [pos_id]
        else:
            if doc_id not in _dict[term]['posting_list'].keys():
                _dict[term]['doc_feq'] += 1
                _dict[term]['posting_list'][doc_id] = [pos_id]
            else:
                _dict[term]['posting_list'][doc_id].append(pos_id)


def write_term_dict2disk(term_dict, filename):
    print("\tI'm writing {} to disk...".format(filename))
    start = time.time()
    term_dict = dict(sorted(term_dict.items(), key=lambda x: x[0]))
    term_col = list(term_dict.keys())
    doc_feq_col = list()
    posting_list_col = list()
    for term in tqdm(term_dict.keys()):
        doc_feq_col.append(term_dict[term]['doc_feq'])
        posting_list = dict(sorted(term_dict[term]['posting_list'].items(), key=lambda x: x[0]))
        term_dict[term]['posting_list'] = posting_list
        posting_list_col.append(posting_list)

    data_frame = pd.DataFrame({'term': term_col, 'doc_feq': doc_feq_col, 'posting_list': posting_list_col})
    data_frame.to_csv(filename, index=False, sep=',')

    end = time.time()
    print("\tFile {} has been successfully wrote to disk in {:.4f} seconds.".format(filename, end - start))

    return term_dict


def get_engine_from_csv(file_path, name, mode="vb"):
    filename = name + ".csv"
    file_name = os.path.join(file_path, name + ".csv")
    if filename not in os.listdir(file_path):
        raise NameError("No such file : {}.".format(file_name))

    print("\tI'm Loading the {} from {}...".format(name, file_name))
    start = time.time()
    dict_map = dict()
    if "compressed" in name:
        end = time.time()
        print("\tSuccessfully load {} in {:.4f} seconds.".format(name, end - start))
        return restore_dict(file_name, mode)
    if "dict" in name and "vector_model" not in name and "spell" not in name:
        df = pd.read_csv(file_name)
        for i, term in enumerate(df['term']):
            term = str(term)
            dict_map[term] = dict()
            dict_map[term]['doc_feq'] = df['doc_feq'][i]
            dict_map[term]['posting_list'] = eval(df['posting_list'][i])
    if "vector_model" in name:
        df = pd.read_csv(file_name)
        for i, doc_id in enumerate(df['doc_id']):
            dict_map[doc_id] = eval(df['values'][i])
    if "spell" in name or "rotation" in name:
        df = pd.read_csv(file_name)
        for i, key in enumerate(df['key']):
            key = str(key)
            dict_map[key] = eval(df['value'][i])

    end = time.time()
    print("\tSuccessfully load {} in {:.4f} seconds.".format(name, end - start))
    return dict_map


def parsing_json(file_path):
    args_dict = json.load(open(file_path, "rb"))
    args = EasyDict()
    for key, value in args_dict.items():
        args[key] = value
    return args


def get_doc_name_from_doc_id(data_path, doc_id):
    filenames = os.listdir(data_path)
    filenames = sorted(filenames, key=lambda x: int(x.split(".")[0]))
    return filenames[doc_id]


def display_query_result(data_path, term, pos):
    """

    :param data_path:
    :param term:
    :param pos:
    :return:
    """
    filenames = os.listdir(data_path)
    filenames = sorted(filenames, key=lambda x: int(x.split(".")[0]))
    for doc_id, pos_list in pos.items():
        doc_name = filenames[doc_id]
        print("{}: {}".format(doc_name, term))


def display_query_result_detailed(data_path, term, pos, k=10):
    """

    :param data_path:
    :param term:
    :param pos:
    :param k: Display k words before and after the sentence
    :return:
    """
    filenames = os.listdir(data_path)
    filenames = sorted(filenames, key=lambda x: int(x.split(".")[0]))
    for doc_id, pos_list in pos.items():
        doc_name = filenames[doc_id]
        print("{}: {}".format(doc_name, term))
        print("----------------------------------------------------------")
        with open(os.path.join(data_path, doc_name), "r") as file:
            content = file.read()
            raw_term_list = content.split(" ")
            for pos_id in pos[doc_id]:
                display_content = " ".join(raw_term_list[pos_id - k:pos_id + k + 1])
                print(display_content)
        file.close()
