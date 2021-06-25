from .bool_search import bool_search
from .pretreatment import initialize

close_word_correction = "! close word correction", "! close wc"
open_word_correction = "! open word correction", "! open wc"
word_correction = True



def start(term_dict=None, term_dict_with_positional_index=None, vector_model=None):
    initialize(term_dict,term_dict_with_positional_index)

    global word_correction
    while True:
        query = input("come on, baby: ")
        if query in close_word_correction:
            word_correction = False
            print("Close word correction.")
            continue
        if query in open_word_correction:
            word_correction = True
            print("Open word correction.")
            continue

        ret = bool_search(query, term_dict, word_correction)
        if ret is None:
            print("Please input your query in format!")
        else:
            print(ret)


if __name__ == '__main__':
    start()
