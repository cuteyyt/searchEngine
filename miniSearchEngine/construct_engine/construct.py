import os
import re
import math
import pandas as pd


def read_files(dataset_path="Reuters"):
    """
    Read files from Reuters
    :param dataset_path: Reuters corpus path
    :return:
    """
    doc_dict = dict()
    for i, filename in enumerate(os.listdir(dataset_path)):
        # Choose first 100 files as an example
        if i >= 100:
            break
        with open(os.path.join(dataset_path, filename), 'r') as file:
            content = file.read()
            doc_dict[i] = dict()
            doc_dict[i]['doc_id'] = i + 1
            doc_dict[i]['filename'] = filename
            doc_dict[i]['content'] = content
            file.close()
    print("{:} files has been collected!".format(len(doc_dict)))
    return doc_dict


def construct_term_dict(doc_dict):
    """
    Construct a term dict.
    :param doc_dict:
    :return:
    """
    term_dict = dict()

    for key in doc_dict.keys():
        doc_id = doc_dict[key]['doc_id']
        content = doc_dict[key]['content']
        term_list = content.split(" ")
        for i, term in enumerate(term_list):
            # FIXME: Some pre processing works
            # FIXME: Word Segmentation; Stop words; Normalization; Lemmatization; Stemming
            term = re.sub(r'[\":\s ,]*', '', term)
            if term == "":
                continue
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

    # Extract term, doc feq, posting list from term dict
    term_col = list()
    doc_feq_col = list()
    posting_list_col = list()
    for term in term_dict.keys():
        term_col.append(term)
        doc_feq_col.append(term_dict[term]['doc_feq'])
        posting_list_col.append(term_dict[term]['posting_list'])

    data_frame = pd.DataFrame({'term': term_col, 'doc_feq': doc_feq_col, 'posting_list': posting_list_col})
    data_frame.to_csv("engine/term_dict.csv", index=False, sep=',')

    return term_dict


def construct_vector_model(term_dict, doc_dict):
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


def construct_engine(dataset_path="Reuters"):
    doc_dict = read_files(dataset_path)
    term_dict = construct_term_dict(doc_dict)
    vector_model = construct_vector_model(term_dict, doc_dict)

    return term_dict, vector_model


def main():
    construct_engine()


if __name__ == '__main__':
    construct_engine()
