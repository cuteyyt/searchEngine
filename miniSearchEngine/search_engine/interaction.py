from .bool_search import bool_search
# from .pretreatment import initialize
from .output_format import success_info, error_info, warning_info, plain_info


close_word_correction = ["! close word correction", "! close wc"]
open_word_correction = ["! open word correction", "! open wc"]
EXIT_COMMAND = ["! exit"]
word_correction = True


def start(term_dict=None, term_dict_with_positional_index=None, vector_model=None):
    # initialize(term_dict, term_dict_with_positional_index)

    global word_correction
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
        if query in EXIT_COMMAND:
            break
        ret = bool_search(query, term_dict, word_correction)
        if ret is None:
            warning_info("Please input your query in format!")
        else:
            plain_info(ret)

    success_info("Bye~")


if __name__ == '__main__':
    start()
