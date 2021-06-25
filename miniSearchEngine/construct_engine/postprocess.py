import os
import time

from .utils import write_term_dict2disk, read_from_csv


def compress_by_string(term_dict, file_path):
    compressed_term_dict = dict()
    term_str = ""
    for i, term in enumerate(term_dict.keys()):
        term_str += term
        compressed_term_dict[i] = term_dict[term]

    # write_term_dict2disk(compressed_term_dict, file_path)
    return compressed_term_dict, term_str


def compress_by_block(term_dict, file_path, k):
    pass


def compress_term(mode, file_path):
    if mode == 'single':
        print("11")
        dict_to_deal = read_from_csv(file_path)
        compress_by_string(term_dict, file_path)
    elif mode == 'block':
        dict_to_deal = read_from_csv(file_path)
        compress_by_block(term_dict, file_path)


def compress_index(args):
    args.engine_path = 'engine/2021_06_24_15_31_18'
    for engine_file in os.listdir(args.engine_path):
        if engine_file.endswith('csv'):
            print("\tI'm compressing the file {}...".format(engine_file))
            start = time.time()
            if args.compress_term != 'none':
                file_path = os.path.join(args.engine_path, engine_file)
                compress_term(args.compress_term, file_path)
            if args.compress_doc_id != 'none':
                pass
            if args.compress_pos_id != 'none':
                pass

            end = time.time()
            print("\tCompressed file has been saved to {} with {} memory reduce in {}")
