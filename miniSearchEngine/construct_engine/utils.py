import csv

import pandas as pd


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
    data_frame.to_csv(filename, index=False, sep=',')

    return term_dict


def read_from_csv(file_path):
    if 'df' in file_path:
        pass
    df = pd.read_csv(file_path, sep=',')
    dict_map = dict(zip(df.values[:, 0], df.values[:, 1]))
    return dict_map
