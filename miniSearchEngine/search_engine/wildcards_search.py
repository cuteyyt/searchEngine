from .pretreatment import get_rotation_index


def get_words_by_prefix(prefix):
    candidate_words = get_rotation_index(prefix)
    lens = len(candidate_words)
    index = lens
    left = 0
    right = lens - 1
    while left <= right:
        mid = (left + right) // 2
        if candidate_words[mid][0] < prefix:
            left = mid + 1
        else:
            index = mid
            right = mid - 1

    ret_words = []
    while index < lens:
        if candidate_words[index][0].startswith(prefix):
            ret_words.append(candidate_words[index][1])
            index += 1
        else:
            break
    return ret_words


def check_wildcards(word, word_pieces, prefix="", suffix=""):
    if prefix != "" and not word.startswith(prefix):
        return False
    if suffix != "" and not word.endswith(suffix):
        return False

    index = 0
    word_len = len(word)
    for piece in word_pieces:
        piece_len = len(piece)
        while index + piece_len <= word_len:
            if word[index:index+piece_len] == piece:
                index += piece_len
                break
            index += 1
        else:
            return False

    return True


def get_wildcards_word(word):
    word_pieces = word.split('*')
    word_pieces = [i for i in word_pieces if i != '']
    if len(word_pieces) == 0:
        return
    prefix = ""
    suffix = ""
    if word[0] != '*':
        prefix = word_pieces[0]
    if word[-1] != '*':
        suffix = word_pieces[-1]

    if word[0] != '*':
        candidate_words = get_words_by_prefix('$'+word_pieces[0])
    elif word[-1] != '*':
        candidate_words = get_words_by_prefix(word_pieces[-1]+'$')
    else:
        candidate_words = get_words_by_prefix(word_pieces[0])
    ret_word = []
    for candidate_word in candidate_words:
        if check_wildcards(candidate_word, word_pieces, prefix, suffix):
            ret_word.append(candidate_word)
    return ret_word


