import os
import re

import nltk
from nltk.corpus import stopwords as nltk_stopwords
import jieba


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


def preprocess_for_term_dict(args, content):
    raw_term_list = content.split(" ")
    if args.seg == 0:
        r = r"[\n,]+"
    elif args.seg == 1:
        r = r"[^a-zA-Z0-9.]+"
    elif args.mode == 2:
        r = r""
        raw_term_list = nltk.word_tokenize(content)
    elif args.mode == 3:
        r = r""
        raw_term_list = list(jieba.cut_for_search(content))
    else:
        raise NameError("Undefined segmentation mode {:}".format(args.seg))

    args.stop = 1
    args.norm = 1
    args.lem = 1
    args.stem = 1

    # For convenience of coding, we initialize these part anyway
    stopwords = read_stopwords()
    wnl = nltk.WordNetLemmatizer()
    porter = nltk.PorterStemmer()

    term_list = list()
    for term in raw_term_list:
        term = re.sub(r, r"", term)
        if term == "":
            continue
        if args.stop:
            if is_stopword(term, stopwords):
                continue
        if args.norm:
            term = normalization(term)
            # print(term)
        if args.lem:
            term = lemmatization(wnl, term)
            # print(term)
        if args.stem:
            term = stemming(porter, term)
            # print(term)
        term_list.append(term)

    # print(term_list)
    return term_list
