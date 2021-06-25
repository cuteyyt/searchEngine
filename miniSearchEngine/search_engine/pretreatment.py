import functools
import operator

pre_term_dict = {}
pre_term_dict_with_positional_index = {}
spell_correction_dict = {}
wildcards_dict = {}


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


def initialize(term_dict, term_dict_with_positional_index):
    global pre_term_dict, pre_term_dict_with_positional_index
    global spell_correction_dict, wildcards_dict
    pre_term_dict = term_dict
    pre_term_dict_with_positional_index = term_dict_with_positional_index
    term_list = list(term_dict.keys())

    last_pos = 0
    last_letter = term_list[0][0]
    for i in range(1, len(term_list)):
        if term_list[i][0] != last_letter:
            wildcards_dict[last_letter] = term_list[last_pos:i]
            last_letter = term_list[i][0]
            last_pos = i
    wildcards_dict[last_letter] = term_list[last_pos:]

    term_list.sort(key=functools.cmp_to_key(spell_correction_cmp))

    last_pos = 0
    last_tuple = (term_list[0][0], len(term_list[0]))
    for i in range(1, len(term_list)):
        if not operator.eq((term_list[i][0], len(term_list[i])), last_tuple):
            spell_correction_dict[last_tuple] = term_list[last_pos:i]
            last_tuple = (term_list[i][0], len(term_list[i]))
            last_pos = i
    spell_correction_dict[last_tuple] = term_list[last_pos:]


def get_spell_correction_dict(initial_letter, word_length):
    if (initial_letter, word_length) in spell_correction_dict:
        return spell_correction_dict[(initial_letter, word_length)]
    return []


def get_wildcards_dict(initial_letter):
    if initial_letter in wildcards_dict:
        return wildcards_dict[initial_letter]
    return []


def get_frequency(word):
    if word in pre_term_dict:
        return pre_term_dict[word]['doc_feq']
    return 0

