import os
import re
import time

import nltk
from nltk.corpus import stopwords as nltk_stopwords
import jieba


def segmentation(mode):
    # FIXME: Complete mode 0, 2, 3
    r = None
    if mode == 0:
        r = r"[\n,'\"]+"
    elif mode == 1:
        r = r"[^a-zA-Z0-9.]+"
    return r


def read_stopwords(path="miniSearchEngine/help/stopword_en.txt"):
    stopwords = list()
    with open(path, 'r', encoding='utf8') as f:
        word = f.readline()
        while word:
            stopwords.append(word.replace('\n', ''))
            word = f.readline()
    f.close()

    # FIXME: May add this later
    stopwords = set(nltk_stopwords.words("english"))
    # print(stopwords)
    return stopwords


def is_stopword(term, stopwords):
    if term in stopwords:
        return True
    return False


def normalization(term):
    return term.lower()


def lemmatization(lemmatizer, term):
    return lemmatizer.lemmatize(term)


def stemming(stemmer, term):
    return stemmer.stem(term)


def preprocess_for_term(args, term):
    r = segmentation(args.seg)
    stopwords = read_stopwords()
    wnl = nltk.WordNetLemmatizer()
    porter = nltk.PorterStemmer()

    if r is None:
        pass
    else:
        term = re.sub(r, r"", term)

    # FIXME: Complete mode 2
    if args.stop == 1:
        if is_stopword(term, stopwords):
            term = ""
    elif args.stop == 2:
        pass

    if args.norm:
        term = normalization(term)
    if args.lem:
        term = lemmatization(wnl, term)
    if args.stem:
        term = stemming(porter, term)
    return term


def preprocess_for_text(args, text):
    raw_term_list = text.split(" ")

    term_list = list()
    for term in raw_term_list:
        term = preprocess_for_term(args, term)
        if term != "":
            term_list.append(term)

    return term_list


def preprocess_for_docs(args, docs):
    doc_nums = len(docs)
    if args.store:
        print("\tI'm preprocessing {} docs and saving them to {}".format(doc_nums, args.engine_path))
    else:
        print("\tI'm preprocessing {} docs without saving them.".format(doc_nums))
    start = time.time()
    for key in docs.keys():
        content = docs[key]['text']
        term_list = preprocess_for_text(args, content)
        if args.store:
            filename = docs[key]['file_path']
            with open(os.path.join(args.engine_path, filename), 'w') as file:
                file.write(" ".join(term_list))
            file.close()
    if args.store:
        pass
    end = time.time()
    print("\t{} docs have been preprocessed in {:.4f} second".format(doc_nums, end - start))
