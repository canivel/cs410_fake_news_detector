import requests, pymongo, json, time
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup

MY_API_KEY = open("config/THE_GUARDIAN.key").read().strip()
API_ENDPOINT = 'http://content.guardianapis.com/search'
PAGE_SIZE = 50

def call_api(url, payload):
    # Get the requested url. Error handling for bad requests should be done in
    # the calling function.
    return requests.get(url, params=payload)


def get_response(r):
    # Use json.loads to read the response text
    raw = json.loads(r.text)

    # Return the meta (hits, etc.) and docs (containing urls'n'stuff) back
    return raw


def get_soup(url):
    # Header to be passed in to NYT when scraping article text.
    agent = 'DataWrangling/1.1 (http://canivel.com; '
    agent += 'contact@canivel.com)'
    headers = {'user_agent': agent}

    # Wrap in a try-except to prevent a maxTry connection error from erroring
    # out the program. Return None if there are any issues.
    try:
        r = requests.get(url, headers=headers)
    except:
        return None

    # Just in case there was a normal error returned. Pass back None.
    if r.status_code != 200: return None

    # Otherwise return a soupified object containing the url text encoded in
    # utf-8. Will toss back errors on some pages without the encoding in place.
    return BeautifulSoup(r.text.encode('utf-8'), features="lxml")


def get_body_text(docs):
    # Grab the url from each document, if it exists, then scrape each url for
    # its body text. If we get any errors along the way, continue on to the
    # next document / url to be scraped.
    result = []
    for d in docs:
        # article_dict = {}
        # Make a copy of the doc's dictionary
        doc = d.copy()
        # If there's no url (not sure why this happens sometimes) then ditch it
        if not doc['web_url']:
            continue

        # Scrape the doc's url, return a soup object with the url's text.
        soup = get_soup(doc['web_url'])
        if not soup:
            continue

        # article_dict['headline'] = doc['headline']['main']
        # article_dict['source'] = doc['source']
        # article_dict['pub_date'] = doc['pub_date']

        # Find all of the paragraphs with the correct class.
        # This class tag is specific to NYT articles.
        body = soup.find_all('div', class_="StoryBodyCompanionColumn")
        if not body:
            continue

        # Join the resulting body paragraphs' text (returned in a list).
        doc['body'] = '\n'.join([x.get_text() for x in body])

        print(doc['web_url'])
        result.append(doc)

    return result


def remove_previously_scraped(coll, docs):
    # Check to see if the mongo collection already contains the docs returned
    # from NYT. Return back a list of the ones that aren't in the collection to
    # be scraped.
    new_docs = []
    for doc in docs:
        # Check fo the document id in mongo. If it finds none, append to
        # new_docs
        # cursor = articles.find({'_id': doc['_id']}).limit(1)
        if not articles.count_documents(filter={'_id': doc['_id']}) > 0:
            new_docs.append(doc)

    if new_docs == []:
        return None

    return new_docs


def get_end_date(dt):
    # String-ify the datetime object to YYYMMDD, which the NYT likes.
    yr = str(dt.year)
    mon = '0' * (2 - len(str(dt.month))) + str(dt.month)
    day = '0' * (2 - len(str(dt.day))) + str(dt.day)
    return yr + mon + day


def scrape_articles(coll, psize=20):
    # Request all of the newest articles matching the search term
    start_date = date(2018, 1, 1)
    end_date = date(2018,11, 1)
    dayrange = range((end_date - start_date).days + 1)
    for daycount in dayrange:
        dt = start_date + timedelta(days=daycount)
        print(dt)
        dstr = dt.strftime('%Y-%m-%d')
        payload = {
            'from-date': dstr,
            'to-date': dstr,
            'order-by': "newest",
            'show-fields': 'all',
            'page-size': psize,
            'api-key': MY_API_KEY
        }

        r = call_api(API_ENDPOINT, payload)

        if r.status_code != 200:
            return "Fail {}".format(r.status_code)

        # Get the meta data & documents from the request
        docs = get_response(r)

        for doc in docs['response']['results']:
            try:
                # Insert each doc into Mongo
                #doc
                coll.insert_one(doc)
            except:
                # If there's any error writing it in the db, just move along.
                continue

    #return "Done"

    # # Check if docs are already in the database
    # new_docs = remove_previously_scraped(coll, docs)
    # if not new_docs: continue
    #
    # # Grab only the docs that have these tags
    # docs_with_body = get_body_text(new_docs)
    #
    # for doc in docs:
    #     try:
    #         # Insert each doc into Mongo
    #         coll.insert_one(doc)
    #     except:
    #         # If there's any error writing it in the db, just move along.
    #         continue


if __name__ == "__main__":
    # Initiate Mongo client
    client = pymongo.MongoClient()


    # Access database created for these articles
    db = client.fake_news

    articles = db.tg_articles

    # Set the initial end date (scraper starts at this date and moves back in
    # time sequentially)
    last_date = datetime.now() + relativedelta(days=-2)
    # print(last_date)

    # Pass the database collection and initial end date into main function
    scrape_articles(articles, PAGE_SIZE)
