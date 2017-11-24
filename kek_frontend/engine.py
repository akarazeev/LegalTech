from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import pymorphy2
import os
import re


ru_stopwords = stopwords.words('russian')
morph = pymorphy2.MorphAnalyzer()
cached_idfs = {}


def score_bm25(TF, IDF, doc_len, avg_doc_len, k1=2.0, b=0.75):
    """
    :param TF: term frequency
    :param IDF: inversed document frequency
    :param doc_len: length of current document
    :param avg_doc_len: average length of documents
    :return: BM25 score for word from query
    """
    def compute_K():
        return k1 * ((1 - b) + b * (float(doc_len)/float(avg_doc_len)))

    K = compute_K()

    frac = ((k1 + 1) * TF) / (TF + K)
    return IDF * frac


def lemmatize(word):
    return morph.parse(word)[0].normal_form


def tokenize(string):
    rgx = re.compile("([\w]*\w)")
    return rgx.findall(string)


def preprocess_string(string):
    """
    Lower input `string` -> tokenize() ->
    -> lemmatize each of the words -> remove stopwords.

    :param string: str
    :return: list of str
    """
    lemmatized = list(map(lambda x: lemmatize(x), tokenize(string.lower())))
    filtered = list(filter(lambda x: x not in ru_stopwords, lemmatized))
    return filtered


def tf(word, document):
    """
    :param word: str
    :param document: list of str
    :return: int
    """
    return document.count(word)


def idf(word, documents):
    """
    :param word: str
    :param documents: list of list of str
    :return: float
    """
    n = sum(list(map(lambda x: word in x, documents)))
    return np.log((len(documents) - n + 0.5) / (n + 0.5))


def score_doc(query, documents):
    """
    :param query: str
    :param documents: list of list of str
    :return scores: list
    """
    avg_doc_len = np.mean(list(map(lambda x: len(x), documents)))
    preprocessed_query = preprocess_string(query)
    scores = []

    for document in documents:
        doc_len = len(document)
        score = 0

        for word in preprocessed_query:
            word_tf = tf(word, document)

            # Use `cached_idfs` to speed up computation for each of documents.
            if word not in cached_idfs:
                cached_idfs[word] = idf(word, documents)

            word_idf = cached_idfs[word]

            score += score_bm25(word_tf, word_idf, doc_len, avg_doc_len)

        # Score of relevance of `query` and `document`.
        scores.append(score)

    return scores


def get_df():
    """
    Return DataFrame of BashData from 'posts/' folder.

    :return df: pandas.DataFrame
    """
    path = 'posts/'
    posts = list(filter(lambda x: x.startswith('.') is False, os.listdir(path)))

    urls_content = []

    for file_name in posts:
        post = os.path.join(path, file_name)

        with open(post, 'r', encoding='utf-8') as f:
            data = f.readlines()

        title, url, content = data[1], data[4], data[5:]
        url = url[:-1]
        title = title[:-1]
        content = ''.join(content)
        urls_content.append((title, url, preprocess_string(content), content))

    df = pd.DataFrame(urls_content, columns=['title', 'url', 'preprocessed', 'content'])

    return df


def process_query(query, dataframe):
    """
    Return maximum 10 of top relevant urls to the `query`.

    :param query: str
    :param dataframe: pandas.DataFrame
    :return entries: list of tuples
    """
    scored = score_doc(query, dataframe['preprocessed'])

    topk = 10

    # Get indices of highest relevance score.
    top_indices = list(reversed(np.argsort(scored)[-topk:]))

    SCORES = list(map(lambda x: "{:.2f}".format(scored[x]), top_indices))
    SCORES = list(filter(lambda x: float(x) > 0.0, SCORES))
    DOCUMENTS = list(map(lambda x: dataframe['content'][x][:100] + '...', top_indices))
    TITLES = list(map(lambda x: dataframe['title'][x], top_indices))
    URLS = list(map(lambda x: dataframe['url'][x], top_indices))

    entries = []

    for i in range(len(SCORES)):
        entries.append((SCORES[i], TITLES[i], URLS[i], DOCUMENTS[i]))

    return entries


if __name__ == '__main__':
    raise RuntimeError
