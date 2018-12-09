import re
import numpy as np
import pandas as pd
from nltk.stem.snowball import SnowballStemmer
import wordbatch
from wordbatch.extractors import WordBag, WordHash
from scipy.sparse import hstack
from nltk.corpus import stopwords

stemmer = SnowballStemmer("english")

# Define helpers for text normalization
stopwords = {x: 1 for x in stopwords.words('english')}
non_alphanums = re.compile(u'[^A-Za-z0-9]+')

def rmsle(y, y0):
    assert len(y) == len(y0)
    return np.sqrt(np.mean(np.power(np.log1p(y) - np.log1p(y0), 2)))

def normalize_text(text):
    return u" ".join(
        [x for x in [y for y in non_alphanums.sub(' ', text).lower().strip().split(" ")] \
         if len(x) > 1 and x not in stopwords])

def preprocess(df):

    # fill nans
    print("Filling NaNs")
    df['author'].fillna('No author', inplace=True)
    df['title'].fillna('No title', inplace=True)
    df['text'].fillna('No text', inplace=True)

    #search author encoded
    df_author = pd.read_csv('data/author_cat.csv')

    #TODO check at notebook the values for the author and the equal query set the cateory id right
    df['author_cat'] = 1

    print("Start Stemming Title")
    df['stemmed_title'] = df['title'].map(lambda x: ' '.join([stemmer.stem(y) for y in x.split(' ')]))

    print("Start Stemming News Text")
    df['stemmed_text'] = df['text'].map(lambda x: ' '.join([stemmer.stem(y) for y in x.split(' ')]))

    # drop the title autor and text
    df.drop(['title', 'author', 'text'], axis=1, inplace=True)

    return df