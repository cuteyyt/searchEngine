from miniSearchEngine.construct_engine.construct import main
from miniSearchEngine.construct_engine.utils import get_engine_from_csv
from miniSearchEngine.construct_engine.preprocess import preprocess_for_query
from miniSearchEngine.search_engine.interaction import start

if __name__ == '__main__':
    engine_path = "engine/2021_06_26_21_56_17"
    # engine_path = main()

    term_dict = get_engine_from_csv(engine_path, "term_dict_vector_model")
    # sentence = "this is an example."
    # print(preprocess_for_query(sentence, engine_path))
    # start(term_dict, term_dict_with_positional_index, vector_model)
