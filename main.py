from miniSearchEngine.construct_engine.construct import main
from miniSearchEngine.construct_engine.utils import get_engine_from_csv
from miniSearchEngine.construct_engine.preprocess import preprocess_for_query
from miniSearchEngine.search_engine.interaction import start
from miniSearchEngine.search_engine.pretreatment import initialize, set_dict
from miniSearchEngine.search_engine.utils import write_other_dict2disk
from miniSearchEngine.construct_engine.utils import display_query_result, display_query_result_detailed

if __name__ == '__main__':
    # engine_path = "engine/2021_06_26_21_56_17"
    engine_path = main()

    term_dict = get_engine_from_csv(engine_path, "term_dict")
    term_dict_ = get_engine_from_csv(engine_path, "term_dict_compressed", "vb")
    print(term_dict == term_dict_)
