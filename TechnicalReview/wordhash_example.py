import time
import re
import pandas as pd
import numpy as np
import scipy as sp
from sklearn.feature_extraction.text import HashingVectorizer
import wordbatch
from wordbatch.extractors import WordHash, WordBag, WordSeq, WordVec
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

n_x = 10

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


if __name__ == "__main__":

    # normalize_text= default_normalize_text, spellcor_count=0, spellcor_dist= 2, n_words= 10000000,
    # min_df= 0, max_df= 1.0, raw_min_df= -1, procs= 0, verbose= 1, minibatch_size= 20000,

    vectorizer = HashingVectorizer(preprocessor=normalize_text, decode_error='ignore', n_features=2 ** 23,
                                   non_negative=False, ngram_range=(1, 2), norm='l2')
    start = time.time()
    X = vectorizer.fit_transform(df['text_normalized'])
    print("Process time: {}".format(time.time() - start))
    print(X.shape)

    start = time.time()
    wb = wordbatch.WordBatch(normalize_text, extractor=(WordHash, {"decode_error": 'ignore', "n_features": 2 ** 23,
                                                   "non_negative": False, "ngram_range": (1, 2), "norm": 'l2'}
                                        )
                             , procs=8
                             #, method="serial"
                             )

    Xwb = wb.fit_transform(df['text_normalized'].values)
    print("Process time: {}".format(time.time() - start))
    print(Xwb.shape)