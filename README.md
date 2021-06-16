# searchEngine

Project for ZJU 2021 Information Retrieval and Web Search

## Usage

1. Environment setup:

```shell
pip install -r requirements.txt
```

2. Construct the Search Engine

```shell
python main.py
```

The program will create a `term dict` and a `vector model` based on the corpus. Here I use 100 files as an example.
Function `construct_engine` will return these two variables, you can use them in the program directly At the same time,
they are saved to directory `engine`. You can check the chapter below to see the detailed data structure.

## Data structure

### term dict

```python
term_dict = {
    'a': {  # term
        'doc_feq': 1,  # term's tf
        'posting_list': {  # posting list with positional index
            1: [2, 3, ...]  # doc_id: [pos]
        },
    },
}
```

The corresponding csv file is 'engine/term_dict.csv'.

|term | doc_feq | posting_list | 
| ---- | ---- | ---- | 
| a | 1 | {1:[2,3, ...]} |

### vector model

```python
vector_model = {
    'a': {
        1: 1.1,  # doc_id: tf-idf
        2: 2.2,
        # ...
    },
    'b': {
        1: 1.1,  # doc_id: tf-idf
        2: 2.2,
        # ...
    },
    # ...
}
```

The corresponding csv file is 'engine/term_dict.csv'.

| |term | doc_id | doc_id | 
| ---- | ---- | ---- | ---- | 
| | a | 1.1 | 2.2 |
| | b | 1.1 | 2.2 |

### Others

Note: tf value and df value has also been saved on disk. You can easily distinguish them by filename.