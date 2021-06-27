import pandas as pd


def write_other_dict2disk(term_dict, filename):
    data_frame = pd.DataFrame({'key': list(term_dict.keys()), 'value': list(term_dict.values())})
    data_frame.to_csv(filename, index=False, sep=',')
