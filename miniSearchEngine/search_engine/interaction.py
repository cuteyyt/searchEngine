from .bool_search import bool_search


def start(term_dict=None, term_dict_with_positional_index=None, vector_model=None):
    while True:
        query = input("come on, baby: ")
        ret = bool_search(query, term_dict)
        if ret is None:
            print("Please input your query in format!")
        else:
            print(ret)


if __name__ == '__main__':
    start()