import os
import time
import pandas as pd

from .b_plus_tree import write_tree2disk


def get_permuterm_index(term):
    term += "$"
    permuterm_list = list()
    for i in range(len(term)):
        tmp_term = term[i:] + term[:i]
        permuterm_list.append(tmp_term)
    return permuterm_list


def construct_permuterm_index(engine_path):
    print("I'm doing the task: adding permuterm index to {}.".format(engine_path))
    start = time.time()

    for engine_name in os.listdir(engine_path):
        if engine_name == "term_dict.csv":
            df = pd.read_csv(os.path.join(engine_path, engine_name))
            new_column = dict()
            for i, term in enumerate(df['term']):
                term = str(term)
                new_column[i] = str(get_permuterm_index(term))
            df['permuterm_index'] = list(new_column.values())
            df.to_csv(os.path.join(
                engine_path, engine_name.replace(".csv", "_with_permuterm_index.csv")),
                index=False,
                sep=',')
    end = time.time()
    print("I have done the task in {:.4f} seconds.".format(end - start))


def get_k_gram(term, k=2):
    term = "$" + term + "$"
    k_gram_list = list()
    for i in range(0, len(term)):
        if len(term) - i >= k:
            k_gram_list.append(term[i:i + k])
    return k_gram_list


def construct_gram_index(engine_path, k=2):
    print("I'm doing the task: adding {}-gram index to {}.".format(k, engine_path))
    start = time.time()

    for engine_name in os.listdir(engine_path):
        if engine_name == "term_dict.csv":
            df = pd.read_csv(os.path.join(engine_path, engine_name))
            gram_term_dict = dict()
            new_df = pd.DataFrame(columns=['term', 'posting_list'])
            for i, term in enumerate(df['term']):
                term = str(term)
                k_gram_list = get_k_gram(term, k)
                for new_term in k_gram_list:
                    if new_term not in gram_term_dict.keys():
                        gram_term_dict[new_term] = [term]
                    else:
                        gram_term_dict[new_term].append(term)
            new_df['term'] = list(gram_term_dict.keys())
            new_df['posting_list'] = list(gram_term_dict.values())
            new_df.to_csv(os.path.join(engine_path, engine_name.replace(".csv", "_with_{}_gram_index.csv".format(k))),
                          index=False, sep=',')
    end = time.time()
    print("I have done the task in {:.4f} seconds.".format(end - start))


def construct_b_plus_tree(engine_path, order=4):
    print("I'm doing the task: creating a b+ tree with order {} to {}.".format(order, engine_path))
    start = time.time()

    for engine_name in os.listdir(engine_path):
        if engine_name == "term_dict.csv":
            df = pd.read_csv(os.path.join(engine_path, engine_name))
            keys = list(df['term'])
            values = list([str(_) for _ in range(len(keys))])
            write_tree2disk(engine_path, keys, values, order)
    end = time.time()
    print("I have done the task in {:.4f} seconds.".format(end - start))


def compress_files_by_gzip(path):
    import gzip
    print("I'm doing the task: compress files in {} using gzip".format(path))
    start = time.time()
    os.makedirs(os.path.join(path, "gzip"), exist_ok=True)
    for filename in os.listdir(path):
        if filename != 'gzip' and 'tree' not in filename:
            file = gzip.GzipFile(filename=os.path.join(path, "gzip", filename), mode="wb", compresslevel=9)
            file.write(open(os.path.join(path, filename), "rb").read())
            file.close()
    end = time.time()
    print("I have done the task in {:.4f} seconds".format(end - start))
