import os
import time

import pandas as pd

from .encoding_decoding import vb_encoding, vb_decoding, gamma_encoding, gamma_decoding


def index_compression(engine_path, mode):
    print("I'm doing the task: compressing dicts in {}".format(engine_path))
    start = time.time()
    cnt = 0
    for engine_name in os.listdir(engine_path):
        file_path = os.path.join(engine_path, engine_name)
        if "dict" in engine_name and "spell" not in engine_name and "vector_model" not in engine_name and \
                'compressed' not in engine_name:
            compress_dict(file_path, mode)
            cnt += 1
    end = time.time()
    print("I have compressed {} files in {:.4f} seconds.".format(cnt, end - start))


def compress_dict(engine_path, mode):
    """
    作用：把原来{doc_id:[文档位置]}格式的倒排索引转换成[(offset,[文档位置])]格式
    参数：engine_path: csv文件路径
    返回值：倒排索引列表
    """
    print("\tI'm compressing {}...".format(engine_path))
    start = time.time()
    df = pd.read_csv(engine_path)
    new_dict = dict()
    for i in range(len(df['posting_list'])):
        posting_list = eval(df['posting_list'][i])
        new_list = list()
        j = 0
        last_key = 0
        for key, value in posting_list.items():
            if mode == "vb":
                tmp_list = [vb_encoding(key - last_key), value]
            else:
                tmp_list = [gamma_encoding(key - last_key), value]
            last_key = key
            new_list += tmp_list
            j += 1
        new_dict[i] = new_list
    new_column = pd.Series(new_dict)
    del df["posting_list"]
    df["posting_list"] = new_column
    df.to_csv(engine_path.replace(".csv", "_compressed.csv"), index=False, sep=',')
    end = time.time()
    print("\t{} has been compressed in {:.4f} seconds.".format(engine_path, end - start))


def restore_dict(engine_path, mode):
    df = pd.read_csv(engine_path)

    term_dict = dict()
    for i, term in enumerate(df['term']):
        term = str(term)
        term_dict[term] = dict()
        term_dict[term]['doc_feq'] = df['doc_feq'][i]
        posting_list = eval(df['posting_list'][i])
        term_dict[term]['posting_list'] = dict()
        last_key = 0
        for j in range(0, len(posting_list), 2):
            if mode == "vb":
                offset = vb_decoding(posting_list[j])
            else:
                offset = gamma_decoding(posting_list[j])
            term_dict[term]['posting_list'][offset + last_key] = posting_list[j + 1]
            last_key += offset
    return term_dict
