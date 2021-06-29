from .spell_correction import correct_bad_words, spell_correction_info
from .wildcards_search import get_wildcards_word
from .output_format import warning_info, error_info, plain_info, highlight_info
from .pretreatment import get_term_dict
from ..construct_engine.preprocess import preprocess_for_query

BRACKETS_LEFT = "("
BRACKETS_RIGHT = ")"
SPACES_REDUNDANCY = " "
OPT_AND = "&"
OPT_OR = "|"
OPT_NOT = "~"
WILDCARDS_STAR = "*"


def bool_opt_and(docs1, docs2):
    ret = []
    len1 = len(docs1)
    len2 = len(docs2)
    index2 = 0
    for index1 in range(len1):
        while index2 < len2 and docs2[index2] < docs1[index1]:
            index2 += 1
        if index2 >= len2:
            break
        if docs1[index1] == docs2[index2]:
            ret.append(docs1[index1])
            index2 += 1
    return ret


def bool_opt_or(docs1, docs2):
    ret = []
    len1 = len(docs1)
    len2 = len(docs2)
    index1, index2 = 0, 0
    while index1 < len1 or index2 < len2:
        if index1 >= len1:
            ret.append(docs2[index2])
            index2 += 1
        elif index2 >= len2:
            ret.append(docs1[index1])
            index1 += 1
        elif docs1[index1] < docs2[index2]:
            ret.append(docs1[index1])
            index1 += 1
        elif docs1[index1] > docs2[index2]:
            ret.append(docs2[index2])
            index2 += 1
        else:
            ret.append(docs1[index1])
            index1 += 1
            index2 += 1
    return ret


def bool_opt_not(docs1, max_doc_num=100):
    ret = []
    len1 = len(docs1)
    index = 0
    for doc_id in range(1, max_doc_num):
        if index < len1 and doc_id == docs1[index]:
            index += 1
        else:
            ret.append(doc_id)
    return ret


def bool_search(query_list, engine_path, word_correction=True, wildcards_search=True):
    if len(query_list) == 0:
        error_info("Input can't be empty.")
        return
    query_list = query_list.split(' ')
    term_dict = get_term_dict()

    sta = []
    words = []

    for word in query_list:
        if word == SPACES_REDUNDANCY or word == "":
            continue

        if word == BRACKETS_LEFT:
            sta.append(BRACKETS_LEFT)
        elif word == BRACKETS_RIGHT:
            if len(sta) < 2 or not isinstance(sta[-1], list) or sta[-2] != BRACKETS_LEFT:
                error_info("ERROR! Syntax failed!")
                return
            sta.pop(-2)
        elif word == OPT_AND:
            sta.append(OPT_AND)
        elif word == OPT_OR:
            sta.append(OPT_OR)
        elif word == OPT_NOT:
            sta.append(OPT_NOT)
        else:
            # handle wildcards search
            if wildcards_search and WILDCARDS_STAR in word:
                candidate_words = get_wildcards_word(word)
                if candidate_words is None:
                    warning_info("wildcards can't be '*' only!")
                    return

                term_slice = []
                for candidate_word in candidate_words:
                    term_slice = bool_opt_or(term_slice, list(term_dict[candidate_word]['posting_list'].keys()))
                sta.append(term_slice)
                highlight_info("using wildcards search, words matched: " + str(candidate_words))
                # plain_info("docs with these words are: " + str(term_slice))
                words = words + candidate_words
            # no wildcards search
            else:
                word = preprocess_for_query(word, engine_path)
                if len(word) == 0:
                    word = "!!!InvalidCharacter!!!"
                else:
                    word = word[0]
                # word correction
                if word_correction and word not in term_dict:
                    new_word = correct_bad_words(word)
                    if new_word != "":
                        spell_correction_info(word, new_word)
                        word = new_word

                # normal search
                if word in term_dict:
                    term_slice = list(term_dict[word]['posting_list'].keys())
                    words.append(word)
                else:
                    term_slice = []

                sta.append(term_slice)
                # plain_info(word + " " + str(term_slice))

        while isinstance(sta[-1], list):
            if len(sta) >= 2 and isinstance(sta[-2], list):
                sta[-2] = bool_opt_and(sta[-2], sta[-1])
                sta.pop()
            elif len(sta) >=2 and sta[-2] == OPT_NOT:
                sta[-2] = bool_opt_not(sta[-1], 10788)
                sta.pop()
            elif len(sta) >=3 and sta[-2] == OPT_AND and isinstance(sta[-3], list):
                sta[-3] = bool_opt_and(sta[-3], sta[-1])
                sta.pop()
                sta.pop()
            elif len(sta) >= 3 and sta[-2] == OPT_OR and isinstance(sta[-3], list):
                sta[-3] = bool_opt_or(sta[-3], sta[-1])
                sta.pop()
                sta.pop()
            else:
                break

    if not isinstance(sta[0], list) or len(sta) > 1:
        error_info("ERROR! Syntax failed!")
        return

    return sta[0], words
