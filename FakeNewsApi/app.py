import re
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flasgger import Swagger
import pickle as pkl
import numpy as np
import lightgbm as gbm
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from models.model import FakeNewsModel

app = Flask(__name__)
#api = Api(app)
api = Api(app)
swagger = Swagger(app)

stemmer = SnowballStemmer("english")

# Define helpers for text normalization
stopwords = {x: 1 for x in stopwords.words('english')}
non_alphanums = re.compile(u'[^A-Za-z0-9]+')

#app = Flask(__name__)
#api = Api(app)
def normalize_text(text):
    return u" ".join(
        [x for x in [y for y in non_alphanums.sub(' ', text).lower().strip().split(" ")] \
        if len(x) > 1 and x not in stopwords])

model = FakeNewsModel(lightgbm_model_file='./models/lgb_model_best_iter_5.txt',
                      wb_model_file='./models/wb_transform_5a.pkl')

# argument parsing
parser = reqparse.RequestParser()
parser.add_argument('title')
parser.add_argument('author')
parser.add_argument('text')

class PredictFakeNews(Resource):

    def post(self):
        """
        This examples uses FlaskRESTful Resource
        ---
        tags:
          - "is fake news?"
        summary: "Check if news is fake"
        description: ""
        operationId: "isfakenews"
        consumes:
          - "application/json"
          - "application/x-www-form-urlencoded"
        produces:
          - "application/json"
        parameters:
          - in: "body"
            name: "body"
            description: "Check if News is fake"
            required: true
            schema:
              $ref: "#/definitions/News"
        responses:
          '200':
            description: 'news checked'
          '400':
            description: 'invalid input, object invalid'
        definitions:
          News:
            type: object
            required:
              - "title"
              - "author"
              - "text"
            properties:
              title:
                type: "string"
                description: "Title of the news"
              author:
                type: "string"
                description: "Author of the news"
              text:
                type: "string"
                description: "Body of the news"
         """
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

        return output, 200


# Setup the Api resource routing here
# Route the URL to the resource
api.add_resource(PredictFakeNews, '/isfakenews')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
