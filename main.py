from miniSearchEngine.construct_engine.construct import main
from miniSearchEngine.construct_engine.utils import get_engine_from_csv
from miniSearchEngine.construct_engine.preprocess import preprocess_for_query
from miniSearchEngine.search_engine.interaction import start
from miniSearchEngine.search_engine.pretreatment import initialize
from miniSearchEngine.construct_engine.utils import display_query_result, display_query_result_detailed

if __name__ == '__main__':
    # engine_path = "engine/2021_06_27_00_12_09"
    # engine_path = main()

    # term_dict = get_engine_from_csv(engine_path, "term_dict")

    # spell_correction_dict, rotation_index = initialize(term_dict)
    # sentence = "this is an example."
    # print(preprocess_for_query(sentence, engine_path))
    start()