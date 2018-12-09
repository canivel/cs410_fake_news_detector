import pandas as pd
import numpy as np
from scipy.sparse import hstack
from preprocess_input import preprocess
import pickle as pkl
import gzip
import re
from nltk.corpus import stopwords

# Define helpers for text normalization
stopwords = {x: 1 for x in stopwords.words('english')}
non_alphanums = re.compile(u'[^A-Za-z0-9]+')

def normalize_text(text):
    return u" ".join(
        [x for x in [y for y in non_alphanums.sub(' ', text).lower().strip().split(" ")] \
         if len(x) > 1 and x not in stopwords])

print("Loading models")
pickle_model = "./data/models/models.pkl"
wb, clf= pkl.load(gzip.open(pickle_model, 'rb'))

print("Preprocessing")
d = {'title': ["Title of the news"],
     'text': ["This is the body of the news since it's not a real news let's see if day it's true or not"],
     'author': ["Danilo Canivel"]}
df_test = pd.DataFrame(data=d)
print(df_test.head())


df = preprocess(df_test)
print(df.head())
print("Tranforming with WB")

X_title = wb.transform(df['stemmed_title'])
X_title = X_title[:, np.array(np.clip(X_title.getnnz(axis=0) - 1, 0, 1), dtype=bool)]

X_text = wb.transform(df['stemmed_text'])
X_text = X_text[:, np.array(np.clip(X_text.getnnz(axis=0) - 1, 0, 1), dtype=bool)]

X_author = df['author_cat'].values
X_author = X_author.reshape(-1, 1)

sparse_merge = hstack((X_title, X_text, X_author)).tocsr()

# Remove features with document frequency <= 100
mask100 = np.array(np.clip(sparse_merge.getnnz(axis=0) - 100, 0, 1), dtype=bool)
X = sparse_merge[:, mask100]
print(X.shape)
print('Loading model to predict...')
# # load model to predict
# bst = lgb.Booster(model_file=clf)
# # can only predict with the best iteration (or the saving iteration)
# y_pred = bst.predict(X)

y = clf.predict(X)

print("The score of truth from 0 to 1 for this news is {}".format(round(y, 5)))