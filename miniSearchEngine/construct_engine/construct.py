import os
import time
import math
import json
import argparse
import pandas as pd

from .preprocess import preprocess_for_term_dict


def read_files(data_path="Reuters"):
    """

    :param data_path:
    :return:
    """
    print("\tI'm reading raw data from disk...")
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
            doc_dict[i]['content'] = content
        file.close()
    print("\tDoc dict with {:} files has been collected!".format(len(doc_dict)))
    return doc_dict


def construct_term_dict(args, doc_dict):
    print("\tI'm constructing term dict...")
    term_dict = dict()

    for key in doc_dict.keys():
        doc_id = doc_dict[key]['doc_id']
        content = doc_dict[key]['content']
        term_list = preprocess_for_term_dict(args, content)
        for i, term in enumerate(term_list):
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
    term_col = list()
    doc_feq_col = list()
    posting_list_col = list()
    for term in term_dict.keys():
        term_col.append(term)
        doc_feq_col.append(term_dict[term]['doc_feq'])
        posting_list_col.append(term_dict[term]['posting_list'])

    data_frame = pd.DataFrame({'term': term_col, 'doc_feq': doc_feq_col, 'posting_list': posting_list_col})
    data_frame.to_csv("engine/term_dict.csv", index=False, sep=',')

    print("Dict with {:d} terms has been created!".format(len(term_dict)))
    return term_dict


def construct_vector_model(args, term_dict, doc_dict):
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

    return vector_model


def construct_engine(args):
    data_path = args.data_path

    doc_dict = read_files(data_path)
    term_dict = construct_term_dict(args, doc_dict)
    vector_model = construct_vector_model(args, term_dict, doc_dict)

    return term_dict, vector_model


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", type=str, default="Reuters/",
                        help="Path to the directory which contains raw data files.")
    parser.add_argument("--engine_path", type=str, default="engine/",
                        help="Path to store the posting list, vector model and other necessary files.")

    parser.add_argument("--seg", "--segmentation", type=int, default=0,
                        help="0: Split by SPACES ONLY."
                             "1: Split by SPACES with PUNCTUATION removed."
                             "default is 0.")
    parser.add_argument("--stop", "--stopwords", type=bool, default=False,
                        help="Whether to remove stop words, default is FALSE.")
    parser.add_argument("--norm", "--normalization", type=bool, default=False,
                        help="Whether to use token normalization, default is FALSE.")
    parser.add_argument("--lem", "--lemmatization", type=bool, default=False,
                        help="Whether to use token Lemmatization, default is FALSE.")
    parser.add_argument("--stem", "--stemming", type=bool, default=False,
                        help="Whether to use token Stemming, default is FALSE.")

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
