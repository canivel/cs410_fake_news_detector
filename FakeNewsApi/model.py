import re
import lightgbm as lgb
import pickle as pkl
import numpy as np
from scipy.sparse import hstack
import pandas as pd
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords


# X_test_title = wb.transform([d['stemmed_title']])
# X_test_text = wb.transform([d['stemmed_text']])
# X_test_author = np.array(d['author_cat'])
# X_test_author = X_test_author.reshape(-1, 1)
# sparse_merge_test = hstack((X_test_title, X_test_text, X_test_author)).tocsr()

class FakeNewsModel(object):

    def __init__(self, lightgbm_model_file, wb_model_file):
        self.gbm = lgb.Booster(model_file=lightgbm_model_file)
        self.wb = pkl.load(open(wb_model_file, 'rb'))
        self.stemmer = SnowballStemmer("english")

        # Define helpers for text normalization
        self.stopwords = {x: 1 for x in stopwords.words('english')}
        self.non_alphanums = re.compile(u'[^A-Za-z0-9]+')
        self.authors_df = pd.read_csv('./models/authors.csv')

    def rmsle(self, y, y0):
        """Calculate Root mean square Logarithmic error
        """
        assert len(y) == len(y0)
        return np.sqrt(np.mean(np.power(np.log1p(y) - np.log1p(y0), 2)))

    def normalize_text(self, text):
        """Normalize text, removing non alpha, lowering case, and passing stopword to remove low idf words
        """
        return u" ".join(
            [x for x in [y for y in self.non_alphanums.sub(' ', text).lower().strip().split(" ")] \
             if len(x) > 1 and x not in stopwords])

    def vectorizer_transform(self, text):
        """Transform the text data to a sparse TFIDF matrix using WordBatch transformation model
        """
        return self.wb.transform([text])

    def encode_author(self, author="No author"):
        a = self.authors_df[(self.authors_df['author'] == author)]['author_cat']

        if a.values.size > 0:
            return a.values[0]
        else:
            return self.authors_df['author_cat'].max()+1

    def vector_and_stack(self, title="No title", text="No text", author="No author"):
        X_title = self.vectorizer_transform(title)
        X_text = self.vectorizer_transform(text)
        X_author = np.array(author)
        X_author = X_author.reshape(-1, 1)

        return hstack((X_title, X_text, X_author)).tocsr()


    def predict(self, X):
        """Returns the predicted class in an array
        """
        y_pred = self.gbm.predict(X)
        return y_pred
