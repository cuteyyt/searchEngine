import os
import time
import math
import json
import argparse
import pandas as pd

from copy import deepcopy

from nltk import pos_tag

from .utils import insert_term2dict, write_term_dict2disk
from .preprocess import preprocess_for_docs, preprocess_for_term
from .postprocess import compress_index


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
        # FIXME: Choose first 100 files for debug.
        if i >= 100:
            break
        with open(os.path.join(data_path, filename), 'r') as file:
            content = file.read()
            doc_dict[i + 1] = dict()
            doc_dict[i + 1]['file_path'] = filename
            doc_dict[i + 1]['text'] = content
        file.close()
    end = time.time()
    print("\tDoc dict with {:} files has been collected in {:.4f} seconds!".format(len(doc_dict), end - start))
    return doc_dict


def construct_term_dict(args, raw_doc_dict):
    """

    :param args:
    :param raw_doc_dict:
    :return:
    """
    print("\tI'm creating the term dict...")
    start = time.time()
    term_dict = dict()

    for doc_id in raw_doc_dict.keys():
        content = raw_doc_dict[doc_id]['text']
        raw_term_list = content.split(" ")
        for i, term in enumerate(raw_term_list):
            term = preprocess_for_term(args, term)
            insert_term2dict(term, term_dict, doc_id)

    term_dict = write_term_dict2disk(term_dict, os.path.join(args.engine_path, "term_dict.csv"))

    end = time.time()
    print("\tDict with {:d} terms has been created in {:.4f} seconds!".format(len(term_dict), end - start))
    return term_dict


def construct_bi_term_dict(args, raw_doc_dict):
    print("\tI'm creating the bi term dict...")
    start = time.time()
    biword_dict = dict()

    for doc_id in raw_doc_dict.keys():
        content = raw_doc_dict[doc_id]['text']
        raw_term_index = content.split(" ")
        for i in range(len(raw_term_index) - 1):
            term = raw_term_index[i]
            term_next = raw_term_index[i + 1]
            term = preprocess_for_term(args, term)
            term_next = preprocess_for_term(args, term_next)
            bi_term = term + " " + term_next
            insert_term2dict(bi_term, biword_dict, doc_id)

    biword_dict = write_term_dict2disk(biword_dict, os.path.join(args.engine_path, "biword_dict.csv"))

    end = time.time()
    print("\tDict with {:d} terms has been created in {:.4f} seconds!".format(len(biword_dict), end - start))
    return biword_dict


def construct_extended_biword_dict(args, raw_doc_dict):
    print("\tI'm creating the extended biword dict...")
    start = time.time()
    extended_biword_dict = dict()

    for doc_id in raw_doc_dict.keys():
        content = raw_doc_dict[doc_id]['text']
        raw_term_list = content.split(" ")
        pointer = 0
        while pointer < len(raw_term_list):
            while True:
                extended_biword = ""
                term = preprocess_for_term(args, raw_term_list[pointer])
                term_tag = pos_tag(term)
                if term_tag == 'n':
                    pass
                insert_term2dict(extended_biword, extended_biword_dict, doc_id)

    extended_biword_dict = write_term_dict2disk(extended_biword_dict,
                                                os.path.join(args.engine_path, "extended_biword_dict.csv"))

    end = time.time()
    print("\tDict with {:d} terms has been created in {:.4f} seconds!".format(len(extended_biword_dict), end - start))
    return extended_biword_dict


def construct_positional_index(args, term_dict, raw_doc_dict, filename):
    print("\tI'm creating the {} with positional index...".format(filename))
    start = time.time()

    term_dict_with_positional_index = deepcopy(term_dict)
    for doc_id in raw_doc_dict.keys():
        content = raw_doc_dict[doc_id]['text']
        raw_term_list = content.split(" ")
        for i, term in enumerate(raw_term_list):
            term = preprocess_for_term(args, term)
            if term in term_dict.keys():
                term_dict_with_positional_index[term]['posting_list'][doc_id].append(i)

    end = time.time()
    print("\tDict with {:d} terms has been create in {:.4f} seconds".format(len(term_dict_with_positional_index),
                                                                            end - start))

    write_term_dict2disk(term_dict_with_positional_index,
                         os.path.join(args.engine_path, filename.replace(' ', '_') + '_with_positional_index.csv'))
    return term_dict_with_positional_index


def construct_vector_model(args, doc_dict, term_dict):
    print("\tI'm creating the vector model...")
    start = time.time()

    tf_matrix = dict()
    df_matrix = dict()
    vector_model = dict()
    n = len(doc_dict)

    for term in term_dict.keys():
        tf_matrix[term] = dict()
        vector_model[term] = dict()

        df_matrix[term] = term_dict[term]['doc_feq']

        for doc_id in doc_dict.keys():
            if doc_id not in term_dict[term]['posting_list'].keys():
                tf_matrix[term][doc_id] = 0.
                vector_model[term][doc_id] = 0.
            else:
                tf_matrix[term][doc_id] = len(term_dict[term]['posting_list'][doc_id])
                vector_model[term][doc_id] = (1. + math.log10(tf_matrix[term][doc_id])) * math.log10(
                    n / df_matrix[term])

    # Write tf_matrix, df_matrix, vector_model to csv files

    tf_dict = {'term': list(tf_matrix.keys())}
    vm_dict = {'term': list(vector_model.keys())}

    for doc_id in doc_dict.keys():
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

    tf.to_csv(os.path.join(args.engine_path, "tf.csv"), index=False, sep=',')
    df.to_csv(os.path.join(args.engine_path, "df.csv"), index=False, sep=',')
    vm.to_csv(os.path.join(args.engine_path, "vector_model.csv"), index=False, sep=',')

    row = len(vector_model)
    col = len(vm_dict[1])

    end = time.time()
    print("\tVector model {:d}*{:d}(docs*terms) has been created in {:.4f} seconds!".format(row, col, end - start))
    return vector_model


def construct_dict_with_vector_model(args, raw_doc_dict, name):
    if args.biword:
        term_dict = construct_bi_term_dict(args, raw_doc_dict)
    elif args.extended_biword:
        term_dict = construct_extended_biword_dict(args, raw_doc_dict)
    else:
        term_dict = construct_term_dict(args, raw_doc_dict)
    term_dict_with_positional_index = construct_positional_index(args, term_dict, raw_doc_dict, name)
    vector_model = construct_vector_model(args, raw_doc_dict, term_dict_with_positional_index, )
    return term_dict, term_dict_with_positional_index, vector_model


def construct_engine(args):
    """

    :param args:
    :return:
    """
    data_path = args.data_path

    raw_doc_dict = read_files(data_path)

    # At least (default) we should construct a term dict and its corresponding vector model.
    term_dict, term_dict_with_positional_index, vector_model = construct_dict_with_vector_model(args, raw_doc_dict,
                                                                                                "term dict")

    # if args.biword:
    #     construct_dict_with_vector_model(args, raw_doc_dict, "biword dict")
    #
    # if args.extended_biword:
    #     construct_dict_with_vector_model(args, raw_doc_dict, "extended biword")

    # positional index will be created anyway for vector model
    if args.pos:
        pass
    if args.mixed:
        pass

    # compress_index(args)

    return term_dict, term_dict_with_positional_index, vector_model


def check_parameter_integrity(args):
    # Check each single arg
    if args.seg not in [0, 1, 2, 3]:
        raise ValueError("Unsupported segmentation mode {}, "
                         "use command \"construct_engine -h\" to see more details.".format(args.seg))
    if args.stop not in [0, 1, 2]:
        raise ValueError("Unsupported stopwords mode {}, "
                         "use command \"construct_engine -h\" to see more details.".format(args.stop))
    if args.tree <= 2 and args.tree != 0:
        raise ValueError("--tree/--B_plus_tree must be given a positive integer larger than 2 or 0, "
                         "use command \"construct_engine -h\" to see more details.".format(args.tree))
    if args.tree > 5:
        raise ValueError(
            "Although tree order larger than 5 is theoretically allowed, "
            "the construction process will fail if the space or time reaches limit."
            "use command \"construct_engine -h\" to see more details.".format(args.tree))
    if args.gram <= 1 and args.gram != 0:
        raise ValueError("--gram must be given a positive integer or 0, "
                         "use command \"construct_engine -h\" to see more details.".format(args.gram))
    if args.gram >= 5:
        raise ValueError(
            "Although k-gram with k larger than 5 is theoretically allowed, "
            "the construction process will fail if the space or time reaches limit."
            "use command \"construct_engine -h\" to see more details.".format(args.gram))
    if args.compress_term not in ['none', 'single', 'block']:
        raise ValueError("Unsupported compress term mode {}, "
                         "use command \"construct_engine -h\" to see more details.".format(args.compress_term))
    if args.compress_doc_id not in ['none', 'vb', 'gamma']:
        raise ValueError("Unsupported compress/encode doc id mode {}, "
                         "use command \"construct_engine -h\" to see more details.".format(args.compress_doc_id))
    if args.compress_pos_id not in ['none', 'vb', 'gamma']:
        raise ValueError("Unsupported compress/encode pos id mode {}, "
                         "use command \"construct_engine -h\" to see more details.".format(args.compress_pos_id))

    # Check arg relationships
    if not args.pos:
        print("Note: positional index will be created anyway for tf calculate and result display."
              "However, set this FALSE means we will refer to the dict without positional index "
              "and may have a faster query speed.")
    if (not args.biword) and (not args.pos) and (not args.mixed) and (not args.extended_biword):
        print("Warning: please set at least one of the "
              "[\'--biword\',\'--pos\',\'--mixed\',\'extended_biword\'] TRUE to enable phrase query.")

    if (not args.permuterm) and (not args.gram) and (not args.tree):
        print(
            "Warning: please set at least one of the "
            "[\'--permuterm\',\'--gram\',\'--tree\'] TRUE to enable 'mon*' like query.")

    args.engine_path = os.path.join(args.engine_path, time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()))
    os.makedirs(args.engine_path, exist_ok=True)
    # Save parameters
    with open(os.path.join(args.engine_path, 'args.json'), 'w') as file:
        json_data = json.dumps(args.__dict__, indent=2)
        file.write(json_data)
    file.close()
    return args


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", type=str, default="Reuters/",
                        help="Path to the directory which contains raw data files.")
    parser.add_argument("--engine_path", type=str, default="engine/",
                        help="Path to store the posting list, vector model and other necessary files.")

    # Preprocess
    parser.add_argument("--store_preprocessed", "--store", type=bool, default=True,
                        help="Whether to store preprocessed data files, default is TRUE.")
    parser.add_argument("--seg", "--segmentation", type=int, default=1,
                        help="0: Split by SPACES and PUNCTUATIONS. This will treat [-./] as separate words."
                             "1: Except [a-zA-Z0-9.-/], all other characters will be replaced by BLANK."
                             "2: Split by default NLTK API."
                             "3: Split by default JIEBA API."
                             "default is 1.")
    parser.add_argument("--stop", "--stopwords", type=int, default=0,
                        help="Whether to remove stop words, default is FALSE."
                             "1: Use user editable stopwords"
                             "2: Use stopwords from NLTK")
    parser.add_argument("--norm", "--normalization", type=bool, default=False,
                        help="Whether to use token normalization, default is FALSE."
                             "Convert UPPER to LOWER only.")
    parser.add_argument("--lem", "--lemmatization", type=bool, default=False,
                        help="Whether to use token Lemmatization, default is FALSE."
                             "Use NLTK's WordNetLemmatizer.")
    parser.add_argument("--stem", "--stemming", type=bool, default=False,
                        help="Whether to use token Stemming, default is FALSE."
                             "Use NLTK's PorterStemmer.")

    # index specification
    parser.add_argument("--biword", "--biword_index", type=bool, default=False,
                        help="Whether to create biword indexes.")
    parser.add_argument("--pos", "--positional_index", type=bool, default=True,
                        help="Whether to create positional indexes.")
    parser.add_argument("--mixed", "--mixed_index", type=bool, default=False,
                        help="Whether to use biword and positional mixed index."
                             "Note: This is not equal to biword + positional index."
                             "We use highly queried biword from users to reduce index scale.")
    parser.add_argument("--extended_biword", type=bool, default=False,
                        help="Whether to use extended biword, default is FALSE.")

    # Faster term search
    parser.add_argument("--tree", "--B_plus_tree", type=int, default=0,
                        help="Whether to create a B+ tree for the term."
                             "0 stands for NOT and other POSITIVE INTEGER stands for the B+ tree's order.")
    parser.add_argument("--permuterm", "--perm", type=bool, default=False,
                        help="Whether to create a permuterm index.")
    parser.add_argument("--gram", type=int, default=0,
                        help="Whether to create a K-gram index."
                             "0 stands for NOT and other POSITIVE INTEGER stands for the K value.")

    # index compression (as postprocess)
    parser.add_argument("--compress_term", type=str, default="single",
                        help="Whether to compress the term, default is single."
                             "none: Keep original form."
                             "single: Compress terms based on a single string."
                             "block: Compress terms based on block strategy.")
    parser.add_argument("--compress_doc_id", type=str, default="vb",
                        help="Whether to compress doc id."
                             "none: keep original form."
                             "vb: use vb encoding."
                             "gamma: use gamma encoding.")
    parser.add_argument("--compress_pos_id", type=str, default="none",
                        help="Whether to compress positional index, only valid when specify positional index."
                             "none: keep original form."
                             "vb: use vb encoding."
                             "gamma: use gamma encoding."
                        )

    # Effective when doing queries
    parser.add_argument("--skip_list", type=bool, default=False,
                        help="Whether to use skip list when doing queries.")

    args = parser.parse_args()

    print("I have received the task: construct search engine.")
    print("I'm using the following parameters:")
    print(json.dumps(args.__dict__, indent=2))

    print("I'm checking the given parameters:")
    if check_parameter_integrity(args):
        print("Parameter specification is complete.")

    print("I'm doing the task: construct search engine...")
    start = time.time()
    term_dict, term_dict_with_positional_index, vector_model = construct_engine(args)
    end = time.time()
    print("I have done the task \"construct search engine\" in {:.4f} seconds.".format(end - start))
    return term_dict, term_dict_with_positional_index, vector_model

if __name__ == '__main__':
    main()
