# CS410 - Final Project - Fake News Dectector

Let's create a classifier that returns the probability for a news to be fake or not.

The classifier use news from the only two main stream media that provide a open API to fetch news from them: NYT and The Guardian

With this method you are going to achieve .995% Accuracy base on a Kaggle competition for fake news hosted months ago, which would be the first place.

![Kaggle First Place Fake News](https://github.com/canivel/cs410_fake_news_detector/blob/master/imgs_readme/sub-kaggle.png)


Requirements:
* Python3.6+, MongoDB and some libs(pip install -r requirements.txt)
* Kaggle Fake news competition data https://www.kaggle.com/c/fake-news/data (Train and Test)
* Kaggle Fake News data https://www.kaggle.com/mrisdal/fake-news 


Steps to run it:

1. create a MongoDB database, fake_news, and 2 collections tg_articles, nyt_articles
2. run the nyt_spyder and the the_guardian_spyder
3. run the clean_news_data to transform the data from NYT and The Guardian into a better format for python
4. run the dataset_builder, so we merge with Kaggle datasets from https://www.kaggle.com/c/fake-news/data
5. run the training and generate the models
6. run the flask api server
7. send a post request with the news title, news text and author to the endpoint http://cs410.canivel.com/api/isfakenews
8. A Json with the probability of fake will return if you should look for further news on the matter

You can test the Client or Api direct from the Swagger docs

# Client Example
### http://cs410.canivel.com/
# Api - POST endpoint
### http://cs410.canivel.com/api/isfakenews
# Apidocs - Swagger
### http://cs410.canivel.com/apidocs

