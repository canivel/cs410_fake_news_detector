import time
import re
import pandas as pd
import numpy as np
import scipy as sp
from sklearn.feature_extraction.text import HashingVectorizer
import wordbatch
from wordbatch.extractors import WordHash, WordBag, WordSeq, WordVec, Hstack
from nltk.stem.porter import PorterStemmer
stemmer= PorterStemmer()

non_alphanums = re.compile('[\W+]')
nums_re= re.compile("\W*[0-9]+\W*")
triples_re= re.compile(r"(\w)\1{2,}")
trash_re= [re.compile("<[^>]*>"), re.compile("[^a-z0-9' -]+"), re.compile(" [.0-9'-]+ "), re.compile("[-']{2,}"),
re.compile(" '"),re.compile("  +")]

df = pd.read_csv("data/Tweets.csv", encoding="utf8")

re_attags= re.compile(" @[^ ]* ")
re_spaces= re.compile("\w+]")
df['text']= df['text'].apply(lambda x: re_spaces.sub(" ",re_attags.sub(" ", " "+x+" "))[1:-1])
df= df.drop_duplicates(subset=['text'])
df.index= df['id']= range(df.shape[0])

non_alphanums=re.compile('[^A-Za-z]+')
def normalize_text(text):
    return non_alphanums.sub(' ', text).lower().strip()

df['text_normalized']= df['text'].map(lambda x: normalize_text(x))

df= df.drop_duplicates(subset=['text'])

n_x = 2

for i in range(n_x):
    df = df.append(df)


# print(df.shape)
# df = df.append(df)
# df = df.append(df)
# df = df.append(df)
# df = df.append(df)
# df = df.append(df)
#


def normalize_text(text):
    text= text.lower()
    text= nums_re.sub(" NUM ", text)
    text= " ".join([word for word in non_alphanums.sub(" ",text).strip().split() if len(word)>1])
    return text


maxlen = 200
max_words = 20000
wb= wordbatch.WordBatch(normalize_text, max_words=max_words, extractor=(WordSeq, {"seq_maxlen": maxlen}))

wb = wordbatch.WordBatch(normalize_text,
                         extractor=(Hstack,[
                             (WordVec,{"wordvec_file": "../../../data/word2vec/glove.twitter.27B.100d.txt.gz",
                                       "normalize_text": normalize_text, "encoding": "utf8"}),
                             (WordVec, {"wordvec_file": "../../../data/word2vec/glove.6B.50d.txt.gz",
                                        "normalize_text": normalize_text, "encoding": "utf8"})]))
