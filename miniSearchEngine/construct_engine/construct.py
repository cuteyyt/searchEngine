import os
import time
import math
import json
import argparse
import pandas as pd

from .preprocess import preprocess_for_term


def read_files(data_path="Reuters"):
    """

    :param data_path:
    :return:
    """
    print("\tI'm reading raw data from disk...")
    start = time.time()
    doc_dict = dict()
    if len(os.listdir(data_path)) == 0:
        raise ValueError("No file in directory {}".format(data_path))
    for i, filename in enumerate(os.listdir(data_path)):
        # FIXME: Choose first 100 files as an example
        if i >= 100:
            break
        with open(os.path.join(data_path, filename), 'r') as file:
            content = file.read()
            doc_dict[i] = dict()
            doc_dict[i]['doc_id'] = i + 1
            doc_dict[i]['filename'] = filename
            doc_dict[i]['text'] = content
        file.close()
    end = time.time()
    print("\tDoc dict with {:} files has been collected in {:.4f} seconds!".format(len(doc_dict), end - start))
    return doc_dict


def construct_term_dict(args, doc_dict):
    print("\tI'm constructing the term dict...")
    start = time.time()
    term_dict = dict()

    for key in doc_dict.keys():
        doc_id = doc_dict[key]['doc_id']
        content = doc_dict[key]['text']
        term_list = content.split(" ")
        for i, term in enumerate(term_list):
            term = preprocess_for_term(args, term)
            if term != "":
                if term not in term_dict.keys():
                    term_dict[term] = dict()
                    term_dict[term]['doc_feq'] = 1
                    term_dict[term]['posting_list'] = dict()
                    term_dict[term]['posting_list'][doc_id] = [i]
                else:
                    if doc_id not in term_dict[term]['posting_list'].keys():
                        term_dict[term]['doc_feq'] += 1
                        term_dict[term]['posting_list'][doc_id] = [i]
                    else:
                        term_dict[term]['posting_list'][doc_id].append(i)

    # Write term_dict to "engine/term_dict.csv"
    term_dict = dict(sorted(term_dict.items(), key=lambda x: x[0]))
    term_col = list(term_dict.keys())
    doc_feq_col = list()
    posting_list_col = list()
    for term in term_dict.keys():
        doc_feq_col.append(term_dict[term]['doc_feq'])
        posting_list = dict(sorted(term_dict[term]['posting_list'].items(), key=lambda x: x[0]))
        term_dict[term]['posting_list'] = posting_list
        posting_list_col.append(posting_list)

    data_frame = pd.DataFrame({'term': term_col, 'doc_feq': doc_feq_col, 'posting_list': posting_list_col})
    data_frame.to_csv("engine/term_dict.csv", index=False, sep=',')

    end = time.time()
    print("\tDict with {:d} terms has been created in {:.4f} seconds!".format(len(term_dict), end - start))
    return term_dict


def construct_bi_term_dict(args, doc_dict):
    print("\tI'm constructing the bi term dict...")
    start = time.time()
    bi_term_dict = dict()

    for key in doc_dict.keys():
        doc_id = doc_dict[key]['doc_id']
        content = doc_dict[key]['text']
        term_list = content.split(" ")
        for i in range(len(term_list) - 1):
            term = term_list[i]
            term_next = term_list[i + 1]
            term = preprocess_for_term(args, term)
            term_next = preprocess_for_term(args, term_next)
            bi_term = term + " " + term_next
            if bi_term != "":
                if bi_term not in bi_term_dict.keys():
                    bi_term_dict[bi_term] = dict()
                    bi_term_dict[bi_term]['doc_feq'] = 1
                    bi_term_dict[bi_term]['posting_list'] = dict()
                    bi_term_dict[bi_term]['posting_list'][doc_id] = [i]
                else:
                    if doc_id not in bi_term_dict[bi_term]['posting_list'].keys():
                        bi_term_dict[bi_term]['doc_feq'] += 1
                        bi_term_dict[bi_term]['posting_list'][doc_id] = [i]
                    else:
                        bi_term_dict[bi_term]['posting_list'][doc_id].append(i)

    # Write bi_term_dict to "engine/bi_term_dict.csv"
    bi_term_dict = dict(sorted(bi_term_dict.items(), key=lambda x: x[0]))
    term_col = list(bi_term_dict.keys())
    doc_feq_col = list()
    posting_list_col = list()
    for bi_term in bi_term_dict.keys():
        doc_feq_col.append(bi_term_dict[bi_term]['doc_feq'])
        posting_list = dict(sorted(bi_term_dict[bi_term]['posting_list'].items(), key=lambda x: x[0]))
        bi_term_dict[bi_term]['posting_list'] = posting_list
        posting_list_col.append(posting_list)

    data_frame = pd.DataFrame({'bi_term': term_col, 'doc_feq': doc_feq_col, 'posting_list': posting_list_col})
    data_frame.to_csv("engine/bi_term_dict.csv", index=False, sep=',')

    end = time.time()
    print("\tDict with {:d} terms has been created in {:.4f} seconds!".format(len(bi_term_dict), end - start))
    return bi_term_dict


def construct_vector_model(args, term_dict, doc_dict):
    print("\tI'm constructing the vector model...")
    start = time.time()

    tf_matrix = dict()
    df_matrix = dict()
    vector_model = dict()
    n = len(doc_dict)

    for term in term_dict.keys():
        tf_matrix[term] = dict()
        vector_model[term] = dict()

        df_matrix[term] = term_dict[term]['doc_feq']

        for key in doc_dict.keys():
            doc_id = doc_dict[key]['doc_id']
            if doc_id not in term_dict[term]['posting_list'].keys():
                tf_matrix[term][doc_id] = 0
                vector_model[term][doc_id] = 0
            else:
                tf_matrix[term][doc_id] = len(term_dict[term]['posting_list'][doc_id])
                vector_model[term][doc_id] = (1. + math.log10(tf_matrix[term][doc_id])) * math.log10(
                    n / df_matrix[term])

    # Write tf_matrix, df_matrix, vector_model to csv files

    tf_dict = {'term': list(tf_matrix.keys())}
    vm_dict = {'term': list(vector_model.keys())}

    for key in doc_dict.keys():
        doc_id = doc_dict[key]['doc_id']
        tf_dict[doc_id] = list()
        vm_dict[doc_id] = list()
        for term in tf_matrix.keys():
            tf_dict[doc_id].append(tf_matrix[term][doc_id])
        for term in vector_model.keys():
            vm_dict[doc_id].append(vector_model[term][doc_id])

    df_matrix_term_col = list(df_matrix.keys())
    df_matrix_df_col = list(df_matrix.values())

    tf = pd.DataFrame(tf_dict)
    df = pd.DataFrame({'term': df_matrix_term_col, 'df': df_matrix_df_col})
    vm = pd.DataFrame(vm_dict)

    tf.to_csv("engine/tf.csv", index=False, sep=',')
    df.to_csv("engine/df.csv", index=False, sep=',')
    vm.to_csv("engine/vector_model.csv", index=False, sep=',')

    end = time.time()
    print("\tVector model has been created in {:.4f} seconds!".format(end - start))
    return vector_model


def compress_index(term_dict, k):
    # 单一字符串
    compressed_term_dict = dict()
    term_str = ""
    for i, term in enumerate(term_dict.keys()):
        term_str += term
        compressed_term_dict[i] = term_dict[term]

    # 按块存储
    # compressed_term_dict = dict()
    # term_str = ""
    # for i, term in enumerate(term_dict.keys()):
    #     term_str += str(len(term)) + term
    #     if i % k == 0:
    #         compressed_term_dict[i] = [term_dict[term]]
    #     else:
    #         compressed_term_dict[i].append(term_dict[term])

    # 使用间隔
    for term in compressed_term_dict.keys():
        posting_list = compressed_term_dict[term]['posting_list']
        for key in posting_list.key():
            internal_key = posting_list[key_next] - posting_list[key]
    # 间隔 VB 编码
    compressed_key = vb_coding()
    compressed_key = vb_decoding()

    # 间隔 γ 编码

    return compressed_term_dict, term_str


def construct_engine(args):
    data_path = args.data_path

    doc_dict = read_files(data_path)
    term_dict = construct_term_dict(args, doc_dict)
    # bi_word_dict = construct_bi_term_dict(args, doc_dict)
    vector_model = construct_vector_model(args, term_dict, doc_dict)

    return term_dict, vector_model


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", type=str, default="Reuters/",
                        help="Path to the directory which contains raw data files.")
    parser.add_argument("--engine_path", type=str, default="engine/",
                        help="Path to store the posting list, vector model and other necessary files.")

    # Preprocess
    parser.add_argument("--seg", "--segmentation", type=int, default=1,
                        help="0: Split by SPACES ONLY."
                             "1: Split by SPACES with PUNCTUATION removed."
                             "default is 1.")
    parser.add_argument("--stop", "--stopwords", type=bool, default=False,
                        help="Whether to remove stop words, default is FALSE.")
    parser.add_argument("--norm", "--normalization", type=bool, default=False,
                        help="Whether to use token normalization, default is FALSE.")
    parser.add_argument("--lem", "--lemmatization", type=bool, default=False,
                        help="Whether to use token Lemmatization, default is FALSE.")
    parser.add_argument("--stem", "--stemming", type=bool, default=False,
                        help="Whether to use token Stemming, default is FALSE.")

    # index compression
    parser.add_argument("--compress_stem", type=str, default="single",
                        help="none:"
                             "single:"
                             "block:", )
    parser.add_argument("--compress_doc_id", type=str, default="vb",
                        help="none:"
                             "vb:"
                             "gamma:")
    parser.add_argument("--compress_pos_id", type=str, default="none",
                        help="none:"
                             "vb:"
                             "gamma:"
                        )

    print("I have received the task: construct search engine.")
    print("I'm using the following parameters:")
    args = parser.parse_args()
    print(json.dumps(args.__dict__, indent=2))

    print("I'm doing the task: construct search engine...")
    start = time.time()
    construct_engine(args)
    end = time.time()
    print("I have done the task \"construct search engine\" in {:.4f} seconds.".format(end - start))

    if __name__ == '__main__':
        main()
