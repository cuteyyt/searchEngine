from miniSearchEngine.construct_engine.construct import main
from miniSearchEngine.search_engine.interaction import start

if __name__ == '__main__':
    term_dict, term_dict_with_positional_index, vector_model = main()
    start(term_dict, term_dict_with_positional_index, vector_model)
