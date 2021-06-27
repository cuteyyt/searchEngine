from .pretreatment import get_spell_correction_dict, get_frequency
from .output_format import highlight_info, plain_info, warning_info


def calc_edition_distance(str1, str2):
    str1 = " " + str1
    str2 = " " + str2
    len1 = len(str1)
    len2 = len(str2)
    f = [[0 for j in range(len2)] for i in range(len1)]
    for i in range(0, len1):
        f[i][0] = i
    for j in range(0, len2):
        f[0][j] = j
    for i in range(1, len1):
        for j in range(1, len2):
            f[i][j] = min(f[i-1][j]+1, f[i][j-1]+1, f[i-1][j-1] + (1 if str1[i] != str2[j] else 0))

    return f[len1-1][len2-1]


def get_similar_words(bad_word, dis=2):
    candidate_words = []
    for i in range(len(bad_word) - dis if len(bad_word) > dis else 0, len(bad_word) + dis):
        candidate_words = candidate_words + get_spell_correction_dict(bad_word[0], i)

    ret_words = []
    for word in candidate_words:
        word_dis = calc_edition_distance(bad_word,word)
        if word_dis <= dis:
            ret_words.append((word,word_dis))
    return ret_words


def correct_bad_words(bad_word):
    candidate_words = get_similar_words(bad_word)
    max_freq = 0
    if len(candidate_words) == 0:
        return ""
    best_word = candidate_words[0]
    for word_tuple in candidate_words:
        word_freq = get_frequency(word_tuple[0])
        if word_freq > max_freq:
            best_word = word_tuple
            max_freq = word_freq
        elif word_freq == max_freq:
            if word_tuple[1] < best_word[1]:
                best_word = word_tuple
    return best_word[0]


def spell_correction_info(word, new_word):
    highlight_info(word + " can't be recognized. Do you mean '" + new_word + "' ?")

    highlight_info("We have shown you the result of '" + new_word + "'")

    plain_info("If you still want to search '" + word + "', please use such command to close word correction:")

    warning_info('"! close word correction" or "! close wc"')


if __name__ == '__main__':
    print(calc_edition_distance("cab", "cbb"))