import time
import pandas as pd
import os
import json
from pathlib import Path

from .bool_search import bool_search
from .output_format import success_info, error_info, warning_info, plain_info, highlight_info
from .spell_correction import correct_bad_words, spell_correction_info
from .wildcards_search import get_wildcards_word
from .pretreatment import get_term_dict, get_term_dict_vector_model, set_dict, get_doc_word_position
from ..construct_engine.topk import NewTopK
from ..construct_engine.synonym import get_synonyms
from ..construct_engine.k_nearest_neighbors import k_nearest_for_query
from ..construct_engine.preprocess import preprocess_for_query

close_word_correction = ["! close word correction", "! close wc", "! cwc"]
open_word_correction = ["! open word correction", "! open wc", "! owc"]
EXIT_COMMAND = ["! exit", "! e"]
BRIEF_MODE = ["! brief", "! b"]
DETAIL_MODE = ["! detail", "! d"]
SWITCH_MODE_1 = ["! switch bool search mode", "! s1", "! switch 1"]
SWITCH_MODE_2 = ["! switch topk mode", "! s2", "! switch 2"]
SWITCH_MODE_3 = ["! switch k nearest search mode", "! s3", "! switch 3"]
SWITCH_MODE_4 = ["! switch synonym topk mode", "! s4", "! switch 4"]
HELP = ["! help", "! h"]
WILDCARDS_STAR = "*"

data_path = "Reuters/"
engine_path = ""


def bool_search_interface(query, word_correction, wildcards_search=True):
    return bool_search(query, engine_path=engine_path, word_correction=word_correction,
                       wildcards_search=wildcards_search)


def parse_query(query, word_correction=True, wildcards_search=True):
    query_list = query.split(" ")
    term_dict = get_term_dict()
    words = []
    for word in query_list:
        if wildcards_search and WILDCARDS_STAR in word:
            candidate_words = get_wildcards_word(word)
            if candidate_words is None:
                warning_info("wildcards can't be '*' only!")
                return
            highlight_info("using wildcards search, words matched: " + str(candidate_words))
            words = words + candidate_words
        else:
            word = preprocess_for_query(word, engine_path)
            if len(word) == 0:
                word = "!!!InvalidCharacter!!!"
            else:
                word = word[0]
            if word_correction and word not in term_dict:
                new_word = correct_bad_words(word)
                if new_word != "":
                    spell_correction_info(word, new_word)
                    words.append(new_word)
            else:
                words.append(word)
    return words


def topk_search_interface(query, vector_model, term_dict, synonym=False, word_correction=True, wildcards_search=True):
    if synonym:
        query = get_synonyms(query)
        print(query)
    words = parse_query(query, word_correction, wildcards_search)
    if len(words) == 0:
        return None
    query = ' '.join(words)
    res = NewTopK(term_dict, vector_model, query)
    ret = []
    scores = []
    for x in res:
        ret.append(x[0])
        scores.append(x[1])
    return ret, words, scores


def k_nearest_search_interface(query, word_correction, wildcards_search=True):
    words = parse_query(query, word_correction, wildcards_search)
    if len(words) == 0:
        return None
    query = ' '.join(words)
    df = pd.read_csv(open(engine_path + "/term_dict_with_positional_index.csv"))
    return k_nearest_for_query(df, query), words


def display_document_details(doc, words, sentence_num=5, sentence_len=10, brief=False, score=None):
    if brief:
        filenames = os.listdir(data_path)
        filenames = sorted(filenames, key=lambda x: int(x.split(".")[0]))
        doc_name = filenames[doc - 1]
        highlight_info(doc_name + ("" if score is None else " score: {:.6f}".format(score)))
        return

    pos_list = []
    for word in words:
        pos = get_doc_word_position(word, doc)
        if pos is not None:
            pos_list = pos_list + pos

    pos_list.sort()
    # print(doc, pos_list)
    display_list = []
    sentence_cnt = 0
    for pos in pos_list:
        if len(display_list) == 0 or pos - display_list[-1] > sentence_len:
            display_list.append(pos)
            sentence_cnt += 1
            if sentence_cnt >= sentence_num:
                break

    filenames = os.listdir(data_path)
    filenames = sorted(filenames, key=lambda x: int(x.split(".")[0]))
    doc_name = filenames[doc - 1]
    highlight_info(doc_name + ("" if score is None else " score: {:.6f}".format(score)))
    plain_info("========================================================")
    with open(os.path.join(data_path, doc_name), "r") as file:
        content = file.read()
        raw_term_list = content.split(" ")
        for pos_id in display_list:
            display_content = " ".join(
                raw_term_list[pos_id - sentence_len // 2 if pos_id > sentence_len // 2 else 0: pos_id + sentence_len])
            print(display_content)
    file.close()


def display_result(query, ret, brief=False):
    if len(ret[0]) == 0:
        highlight_info("Can't find related documents about your query: " + query)
        return

    success_info(str(len(ret[0])) + " results returned.")
    # print(ret[0])
    # print(ret[1])
    cnt = 0
    index = 0
    while index < len(ret[0]):
        for cnt in range(0, 10):
            if index >= len(ret[0]):
                break
            display_document_details(ret[0][index], ret[1], brief=brief, score=ret[2][index] if len(ret) > 2 else None)
            cnt += 1
            index += 1
        else:
            nxt_flag = input("Read more?(y/n)")
            if nxt_flag != 'y' and nxt_flag != "":
                break


def start():
    global engine_path
    with open("config.json", 'r') as load_f:
        config = json.load(load_f)
        if "engine_path" in config:
            engine_path = config["engine_path"]
    if engine_path == "" or not Path(engine_path).is_dir():
        error_info("Error when get engine_path. Please use 'construct_engine' to build indexes or check 'config.json'")
        return
    set_dict(engine_path)
    term_dict = pd.read_csv(engine_path + "/term_dict.csv", index_col=0)
    vector_model = pd.read_csv(engine_path + "/term_dict_vector_model.csv")
    word_correction = True
    brief = True
    model_select = 1
    while True:
        query = input("come on, baby: ")
        if query in close_word_correction:
            word_correction = False
            success_info("Close word correction.")
            continue
        if query in open_word_correction:
            word_correction = True
            success_info("Open word correction.")
            continue
        if query in BRIEF_MODE:
            brief = True
            success_info("Brief mode.")
            continue
        if query in DETAIL_MODE:
            brief = False
            success_info("Detail mode.")
            continue
        if query in SWITCH_MODE_1:
            model_select = 1
            success_info("You are using bool search.")
            continue
        if query in SWITCH_MODE_2:
            model_select = 2
            success_info("You are using top k search.")
            continue
        if query in SWITCH_MODE_3:
            model_select = 3
            success_info("You are using k nearest search.")
            continue
        if query in SWITCH_MODE_4:
            model_select = 4
            success_info("You are synonym topk search.")
            continue
        if query in HELP:
            print("You can read Readme.md.")
            continue
        if query in EXIT_COMMAND:
            break
        query_start = time.time()
        if model_select == 1:
            ret = bool_search_interface(query, word_correction)
        elif model_select == 2:
            ret = topk_search_interface(query, vector_model, term_dict, word_correction=word_correction)
        elif model_select == 3:
            ret = k_nearest_search_interface(query, word_correction)
        elif model_select == 4:
            ret = topk_search_interface(query, vector_model, term_dict, synonym=True, word_correction=word_correction)
        else:
            ret = bool_search_interface(query, word_correction)
        query_end = time.time()
        success_info("Successfully handle query {} in {:.4f} seconds.".format(query, query_end - query_start))
        if ret is None:
            warning_info("Please input your query in format!")
        else:
            display_result(query, ret, brief=brief)

    success_info("Bye~")


if __name__ == '__main__':
    start()
