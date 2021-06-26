from miniSearchEngine.construct_engine.construct import main
from miniSearchEngine.construct_engine.utils import get_engine_from_csv
from miniSearchEngine.construct_engine.preprocess import preprocess_for_query
from miniSearchEngine.search_engine.interaction import start
from miniSearchEngine.search_engine.pretreatment import initialize
from miniSearchEngine.search_engine.utils import write_other_dict2disk
from miniSearchEngine.construct_engine.utils import display_query_result, display_query_result_detailed

if __name__ == '__main__':
    # engine_path = "engine/2021_06_26_21_56_17"
    engine_path = main()

    term_dict = get_engine_from_csv(engine_path, "term_dict_with_positional_index")
    import os

    spell_correction_dict, rotation_index = initialize(term_dict)
    write_other_dict2disk(spell_correction_dict, os.path.join(engine_path, "spell_correction_dict.csv"))
    write_other_dict2disk(rotation_index, os.path.join(engine_path, "rotation_index.csv"))

    spell_correction_dict = get_engine_from_csv(engine_path, "spell_correction_dict")
    rotation_index = get_engine_from_csv(engine_path, "rotation_index")

    print(spell_correction_dict == spell_correction_dict)
    print(rotation_index == rotation_index)
    # sentence = "this is an example."
    # print(preprocess_for_query(sentence, engine_path))
    # start(term_dict, term_dict_with_positional_index, vector_model)
