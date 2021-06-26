import time

from .bool_search import bool_search
from .output_format import success_info, error_info, warning_info, plain_info


close_word_correction = ["! close word correction", "! close wc"]
open_word_correction = ["! open word correction", "! open wc"]
EXIT_COMMAND = ["! exit"]
word_correction = True


def start():

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
        query_start = time.time()
        ret = bool_search(query, word_correction)
        query_end = time.time()
        success_info("Successfully handle query {} in {:.4f} seconds.".format(query, query_end - query_start))
        if ret is None:
            warning_info("Please input your query in format!")
        else:
            plain_info(ret)

    success_info("Bye~")


if __name__ == '__main__':
    start()
