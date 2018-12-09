import re
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import pickle as pkl
import numpy as np
import lightgbm as gbm
from model import FakeNewsModel
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords

stemmer = SnowballStemmer("english")

# Define helpers for text normalization
stopwords = {x: 1 for x in stopwords.words('english')}
non_alphanums = re.compile(u'[^A-Za-z0-9]+')

app = Flask(__name__)
api = Api(app)

def normalize_text(text):
    return u" ".join(
        [x for x in [y for y in non_alphanums.sub(' ', text).lower().strip().split(" ")] \
         if len(x) > 1 and x not in stopwords])

model = FakeNewsModel(lightgbm_model_file='./models/lgb_model_best_iter_5.txt',
                      wb_model_file='./models/wb_transform_5.pkl')

# argument parsing
parser = reqparse.RequestParser()
parser.add_argument('title')
parser.add_argument('author')
parser.add_argument('text')

class PredictFakeNews(Resource):
    def post(self):
        # use parser and find the user's query
        args = parser.parse_args()
        title = args['title']
        author = model.encode_author(args['author'])
        text = args['text']

        X = model.vector_and_stack(title=title, text=text, author=author)

        prediction = model.predict(X)

        # Output either 'Negative' or 'Positive' along with the score
        if round(prediction[0]) == 0:
            pred_text = 'Reliable News'
        else:
            pred_text = 'Unreliable News'

        # round the predict proba value and set to new variable
        confidence = round(prediction[0], 3)

        # create JSON object
        output = {'prediction': pred_text, 'fake_rate': confidence}

        return output


# Setup the Api resource routing here
# Route the URL to the resource
api.add_resource(PredictFakeNews, '/isfakenews')

if __name__ == '__main__':
    app.run()