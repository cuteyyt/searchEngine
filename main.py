from miniSearchEngine.construct_engine.construct import main
from miniSearchEngine.construct_engine.utils import get_engine_from_csv
from miniSearchEngine.construct_engine.synonym import get_synonyms
from miniSearchEngine.construct_engine.k_nearest_neighbors import k_nearest_for_query
from miniSearchEngine.construct_engine.topk import Topk, NewTopK
from miniSearchEngine.construct_engine.preprocess import preprocess_for_query
# from miniSearchEngine.search_engine.interaction import start
# from miniSearchEngine.search_engine.pretreatment import initialize, set_dict
from miniSearchEngine.search_engine.utils import write_other_dict2disk
from miniSearchEngine.construct_engine.utils import display_query_result, display_query_result_detailed
from miniSearchEngine.construct_engine.utils import get_doc_name_from_doc_id
import pandas as pd

if __name__ == '__main__':
    # engine_path = "engine/2021_06_27_15_13_01"
    engine_path = main()
    # get_engine_from_csv(engine_path, "term_dict_vector_model")

    """
    term_dict = get_engine_from_csv(engine_path, "term_dict_with_positional_index")
    import os
    query_options = {
        "synonym": False,
        "synonym_num": 5,
        "K_nearest": False,  # k邻近，专用于短语查询,不要和同义词扩展一起用
        "K_nearest_num": 5,
        "TopK": True,  # 通用查询，可与同义词扩展一起用
        "TopK_num": 10,
        "vector_model_path": "engine/2021_06_26_19_31_59/term_dict_vector_model.csv"
    }
    query = "Vegetable oil registrations"
    position_index_df = pd.read_csv("engine/2021_06_26_19_31_59/term_dict_with_positional_index.csv")
    if query_options["K_nearest"]:
        doc_id_list = k_nearest_for_query(position_index_df, query, query_options["K_nearest_num"])  # 返回文档列表
    if query_options["synonym"]:  # 同义词扩展
        query = get_synonyms(query, query_options["synonym_num"])
    if query_options["TopK"]:  # topk
        doc_id_list = TopK(query, query_options["vector_model_path"], query_options["TopK_num"])
    doc_id_list = [get_doc_name_from_doc_id("Reuters/", doc_id) for doc_id in doc_id_list]  # 按序号对应文件名
    print(doc_id_list)
    """
    # start()
