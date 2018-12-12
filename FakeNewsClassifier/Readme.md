# CS410 - Final Project - Fake News Classifier

Before you begin lest create a folder /data at the root of your project, where we are going to store our generated files

##nyt_spyder.py
* Scrap data from NYT and save it to a MongoDB database, you just need to set the initial end date (scraper starts at this date and moves back in
time sequentially)
* Code for each function is commented in the code
##tg_spyder.py
* Scrap data from The Guardian and save it to a MongoDB database, you just need to set the initial end date (scraper starts at this date and moves back in
time sequentially)
* Code for each function is commented in the code

##clean_news_data.py
* This script will merge both scrapped sites in a single dataset
* Run this script after scrapy the data from the two news sites
* It will connect to your local MongoDB, select both collections, if you created with the exact names in the instructions, clean, merge it and convert it to csv
* Only the columns that exist in both dataset will be used for this task
* 3 files will be generated at the end of it:
    * data/tg_articles_v2.csv
    * data/nyt_articles_v2.csv
    * data/nyt_tg.csv (this is the merged file)

##dataset_builder.py
* this script will add Kaggle datasets and our generated file in a single dataset
* We start by loading all 3 datasets
* fill the Nans for author, title and text, since that are the only 3 features that Kaggle has in one of the datasets
* we add the Value 1 to all labels to the file kaggle/fake.csv, this is explained in details on the video presentation
* we add the Value 0 to all news scrapped from NYT and The Guardian, we are going to suppose that the main stream media are not fake
* With that we are going to have a much more balanced dataset
* a final dataset is generated and saved at data/df_final_v1.csv


##training.py
*Before running this file, make sure to change the flag inside the __main__ if you want to generate a kaggle submission, is_kaggle = False
*We load our datasets and our kaggle/test.csv file to generate the submission
*save the dimensions of the training, the labels and the ids from the test
*if is the time you are running it, it will generate a news dataset: data/df_stemmed_kaggle.csv after preprocessing the data
* the preprocessing is called with the training data and the testing data
    ### preprocessing function:
    * we start filling the Nans for the testing data, the same way we filled in the training
    * we remove the ids from the test and append it to the training, so everything we do in the data we do for all the data
    * encode the Author, since it's a category feature
    * we save the authors mapping so we can check it later in for a client call for example
    * next we stemm the title and the text and save it as new features, stemmed_title and stemmed_text
    * we drop the old author, title and text, and save the new data/df_stemmed_kaggle.csv
* after the preprocessing we go to the feature extraction, powered by Wordbatch, ( you can check more about it at my technical Review folder)
    * we are going to generate 2 ** 23 number of features, using a ngram of 2 and a idf of 10
* after done the transformation for the , stemmed_title and stemmed_text we create a sparse vector withe the title, text and author features
* we split back to train and test and create our validation set.
* we pass the train and the validation to our model Lightgbm classifier, with a objective of binary classification, and a learning rate of 0.1
* it will run and validate each run til the number of rounds or the early stopping is trigger
* when this happen we save the model for further use, along with the transformation model created with wordbatch
* if kaggle is True, the Test data is passed to the model and the predictions are generated and saved at data/kaggle/submission_lgb.csv


