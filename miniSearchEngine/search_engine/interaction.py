import time
import pandas

from .bool_search import bool_search
from .output_format import success_info, error_info, warning_info, plain_info, highlight_info
from .spell_correction import correct_bad_words, spell_correction_info
from .wildcards_search import get_wildcards_word
from .pretreatment import get_term_dict, get_term_dict_vector_model, set_dict, get_doc_word_position
from ..construct_engine.topk import TopK
from ..construct_engine.k_nearest_neighbors import k_nearest_for_query


close_word_correction = ["! close word correction", "! close wc"]
open_word_correction = ["! open word correction", "! open wc"]
EXIT_COMMAND = ["! exit"]
WILDCARDS_STAR = "*"

engine_path = "engine/2021_06_27_19_38_59"


def bool_search_interface(query, word_correction, wildcards_search=True):
    return bool_search(query, word_correction, wildcards_search)


def parse_query(query, word_correction=True, wildcards_search=True):
    query_list = query.split(' ')
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
            if word_correction and word not in term_dict:
                new_word = correct_bad_words(word)
                if new_word != "":
                    spell_correction_info(word, new_word)
                    words.append(new_word)
            else:
                words.append(word)
    return words


def topk_search_interface(query, word_correction=True, wildcards_search=True):
    words = parse_query(query, word_correction, wildcards_search)
    if len(words) == 0:
        return None
    query = ' '.join(words)
    return TopK(query, engine_path + "/term_dict_vector_model.csv"), words


def k_nearest_search_interface(query, word_correction, wildcards_search=True):
    words = parse_query(query, word_correction, wildcards_search)
    if len(words) == 0:
        return None
    query = ' '.join(words)
    df = pandas.read_csv(open(engine_path+"/term_dict_with_positional_index.csv"))
    return k_nearest_for_query(df, query), words


def display_document_details(doc, words, sentence_num=5, sentence_len=10):
    pos_list = []
    for word in words:
        pos = get_doc_word_position(word, doc)
        if pos is not None:
            pos_list = pos_list + pos

    pos_list.sort()
    print(doc, pos_list)



def display_result(query, ret):
    if len(ret[0]) == 0:
        highlight_info("Can't find related documents about your query: " + query)
        return

    print(ret[0])
    for doc in ret[0]:
        display_document_details(doc, ret[1])


def start():
    set_dict(engine_path)
    word_correction = True
    while True:
        model_select = input("select search method(1.bool search | 2.topk search | 3.k_nearest search):\n")
        query = input("come on, baby: ")
        if query in close_word_correction:
            word_correction = False
            success_info("Close word correction.")
            continue
        if query in open_word_correction:
            word_correction = True
            success_info("Open word correction.")
            continue
        if query in EXIT_COMMAND:
            break
        query_start = time.time()
        if model_select == "1":
            ret = bool_search_interface(query, word_correction)
        elif model_select == "2":
            ret = topk_search_interface(query, word_correction)
        elif model_select == "3":
            ret = k_nearest_search_interface(query,word_correction)
        else:
            ret = bool_search_interface(query, word_correction)
        query_end = time.time()
        success_info("Successfully handle query {} in {:.4f} seconds.".format(query, query_end - query_start))
        if ret is None:
            warning_info("Please input your query in format!")
        else:
            display_result(query, ret)

    success_info("Bye~")


if __name__ == '__main__':
    start()
