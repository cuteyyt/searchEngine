from .pretreatment import get_wildcards_dict_prefix, get_wildcards_dict_suffix


def get_words_by_prefix(prefix):
    candidate_words = get_wildcards_dict_prefix(prefix[0])
    lens = len(candidate_words)

    index = lens
    left = 0
    right = lens - 1
    while left <= right:
        mid = (left + right) // 2
        if candidate_words[mid] < prefix:
            left = mid + 1
        else:
            index = mid
            right = mid - 1

    ret_words = []
    while index < lens:
        if candidate_words[index].startswith(prefix):
            ret_words.append(candidate_words[index])
            index += 1
        else:
            break
    return ret_words


def get_words_by_suffix(suffix):
    candidate_words = get_wildcards_dict_suffix(suffix[-1])
    lens = len(candidate_words)

    index = lens
    left = 0
    right = lens - 1
    while left <= right:
        mid = (left + right) // 2
        if candidate_words[mid][::-1] < suffix[::-1]:
            left = mid + 1
        else:
            index = mid
            right = mid - 1

    ret_words = []
    while index < lens:
        if candidate_words[index].endswith(suffix):
            ret_words.append(candidate_words[index])
            index += 1
        else:
            break
    return ret_words


def get_wildcards_word(word_pieces):
    pass

