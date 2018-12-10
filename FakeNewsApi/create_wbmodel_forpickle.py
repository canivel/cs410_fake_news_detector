import re
import numpy as np
import pandas as pd
from nltk.stem.snowball import SnowballStemmer
import wordbatch
from wordbatch.extractors import WordBag, WordHash
from nltk.corpus import stopwords
import pickle as pkl
import gzip
from models.model import normalize_text

stemmer = SnowballStemmer("english")

# Define helpers for text normalization
stopwords = {x: 1 for x in stopwords.words('english')}
non_alphanums = re.compile(u'[^A-Za-z0-9]+')


train = pd.read_csv('../FakeNewsClassifier/data/df_final_v1.csv')
test = pd.read_csv('../FakeNewsClassifier/data/kaggle/test.csv')

train_size = train.shape[0]
y = train['label']
test_ids = test['id']
test_size = test.shape[0]

train.drop(['label'], axis=1, inplace=True)
test.drop(['id'], axis=1, inplace=True)

df = train.append(test, sort=False)

# fill nans
print("Filling NaNs")
df['author'].fillna('No author', inplace=True)
df['title'].fillna('No title', inplace=True)
df['text'].fillna('No text', inplace=True)


print("Start Stemming Title")
df['stemmed_title'] = df['title'].map(lambda x: ' '.join([stemmer.stem(y) for y in x.split(' ')]))

print("Start Stemming News Text")
df['stemmed_text'] = df['text'].map(lambda x: ' '.join([stemmer.stem(y) for y in x.split(' ')]))

wb = wordbatch.WordBatch(normalize_text
                         , extractor=(WordBag, {"hash_ngrams": 2,
                                                "hash_ngrams_weights": [0.5, -1.0],
                                                "hash_size": 2 ** 23,
                                                "norm": 'l2',
                                                "tf": 'log',
                                                "idf": 10.0}
                                     )
                         , procs=8
                         , method="serial")

wb.dictionary_freeze = True

X_title = wb.transform(df['stemmed_title'])
X_text = wb.transform(df['stemmed_text'])

print("Saving wb model")
with open('wb_transform_5a.pkl', 'wb') as model_file:
    pkl.dump(wb, model_file, protocol=2)
print('Model Saved')