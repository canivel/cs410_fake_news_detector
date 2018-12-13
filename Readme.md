# CS410 - Final Project - Fake News Dectector

Let's create a classifier that returns the probability for a news to be fake or not.

The classifier use news from  two main stream media, that provide a open API to fetch news from them: NYT and The Guardian

With this method you are going to achieve .995% Accuracy base on a Kaggle competition for fake news hosted this year(2018), which would give you the first place.

![Kaggle First Place Fake News](https://github.com/canivel/cs410_fake_news_detector/blob/master/imgs_readme/sub-kaggle.png)


## Presentation
[![Watch the video](http://img.youtube.com/vi/0.jpg)](https://youtu.be/N5gY9SXAHpI)

#### Requirements:
* Python3.6+, MongoDB and some libs(pip install -r requirements.txt)
* Kaggle Fake news competition data https://www.kaggle.com/c/fake-news/data (Train and Test)
* Kaggle Fake News data https://www.kaggle.com/mrisdal/fake-news 
* NYT API Key: https://developer.nytimes.com/signup
* The Guardian API Key: https://open-platform.theguardian.com/access/

#### Steps to run it:

1. Create your APi Keys and save it at /config folders (not included)
2. Download the datasets from kaggle and save it ata /data/kaggle folder
3. Install and Create a MongoDB database, fake_news, and 2 collections tg_articles, nyt_articles
4. run the nyt_spyder and the the_guardian_spyder
5. run the clean_news_data to transform the data from NYT and The Guardian into a better format for python
6. run the dataset_builder, so we merge with Kaggle datasets from https://www.kaggle.com/c/fake-news/data
7. run the training and generate the models
8. run the flask api server
9. send a post request with the news title, news text and author to the endpoint http://cs410.canivel.com/api/isfakenews
10. A Json with the probability of fake will return if you should look for further news on the matter
11. To run the simple React client just run npm start on the fake-news-client

#### To know more about each project, just go to one of the folders, and a simple documentation is in place for each of them.

You can test the Client or Api direct from the Swagger docs

# Client Example
### http://cs410.canivel.com/
# Api - POST endpoint
### http://cs410.canivel.com/api/isfakenews
# Apidocs - Swagger
### http://cs410.canivel.com/apidocs

