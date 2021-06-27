import os
import functools
import operator
from ..construct_engine.utils import get_engine_from_csv
from .utils import write_other_dict2disk

pre_term_dict = {}
pre_term_dict_vector_model = {}
spell_correction_dict = {}
rotation_index = {}


def spell_correction_cmp(x, y):
    if x[0] < y[0]:
        return -1
    if x[0] > y[0]:
        return 1
    if len(x) < len(y):
        return -1
    if len(y) > len(x):
        return 1
    if x < y:
        return -1
    if y > x:
        return 1
    return 0


def wildcards_suffix_cmp(x, y):
    if x[::-1] < y[::-1]:
        return -1
    if x[::-1] > y[::-1]:
        return 1
    return 0


def initialize_rotation_index(term_list):
    global rotation_index
    rotated_term_list = []
    for word_src in term_list:
        word = word_src + '$'
        lens = len(word)
        rotated_term_list.append((word, word_src))
        for i in range(1, lens):
            rotated_term_list.append((word[i:] + word[0:i], word_src))
    rotated_term_list.sort(key=lambda word_tuple: word_tuple[0])

    last_pos = 0
    last_2_letter = rotated_term_list[0][0][0:2]
    for i in range(1, len(rotated_term_list)):
        if rotated_term_list[i][0][0:2] != last_2_letter:
            rotation_index[last_2_letter] = rotated_term_list[last_pos:i]
            last_2_letter = rotated_term_list[i][0][0:2]
            last_pos = i
    rotation_index[last_2_letter] = rotated_term_list[last_pos:]


def initialize(term_dict, engine_path):
    global pre_term_dict
    global spell_correction_dict
    pre_term_dict = term_dict
    # pre_term_dict_with_positional_index = term_dict_with_positional_index
    term_list = list(term_dict.keys())

    initialize_rotation_index(term_list)

    term_list.sort(key=functools.cmp_to_key(spell_correction_cmp))

    last_pos = 0
    last_tuple = (term_list[0][0], len(term_list[0]))
    for i in range(1, len(term_list)):
        if not operator.eq((term_list[i][0], len(term_list[i])), last_tuple):
            spell_correction_dict[last_tuple] = term_list[last_pos:i]
            last_tuple = (term_list[i][0], len(term_list[i]))
            last_pos = i
    spell_correction_dict[last_tuple] = term_list[last_pos:]
    write_other_dict2disk(spell_correction_dict, os.path.join(engine_path, "spell_correction_dict.csv"))
    write_other_dict2disk(rotation_index, os.path.join(engine_path, "rotation_index.csv"))


def set_dict(engine_path):
    global pre_term_dict, spell_correction_dict, rotation_index, pre_term_dict_vector_model
    pre_term_dict = get_engine_from_csv(engine_path, "term_dict_with_positional_index")
    # pre_term_dict_vector_model = get_engine_from_csv(engine_path, "term_dict_vector_model")
    initialize(pre_term_dict, engine_path)
    # spell_correction_dict = get_engine_from_csv(engine_path, "spell_correction_dict")
    # rotation_index = get_engine_from_csv(engine_path, "rotation_index")


def get_spell_correction_dict(initial_letter, word_length):
    global spell_correction_dict
    if (initial_letter, word_length) in spell_correction_dict:
        return spell_correction_dict[(initial_letter, word_length)]
    return []


def get_rotation_index(prefix):
    global rotation_index
    if len(prefix) < 1:
        print("get rotation index: prefix is null")
    if len(prefix) == 1:
        ret = []
        for key in rotation_index:
            if key[0] == prefix[0]:
                ret = ret + rotation_index[key]
        return ret

    if prefix[0:2] in rotation_index:
        return rotation_index[prefix[0:2]]
    return []


def get_frequency(word):
    if word in pre_term_dict:
        return pre_term_dict[word]['doc_feq']
    return 0


def get_doc_word_position(word, doc):
    if word in pre_term_dict and doc in pre_term_dict[word]['posting_list']:
        return pre_term_dict[word]['posting_list'][doc]
    else:
        return None


def get_term_dict():
    return pre_term_dict


def get_term_dict_vector_model():
    return pre_term_dict_vector_model
