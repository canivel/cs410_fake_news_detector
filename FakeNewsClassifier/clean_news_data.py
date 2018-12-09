import pymongo
import pandas as pd

if __name__ == "__main__":
    client = pymongo.MongoClient()
    print("Connected to MongoDB")
    db = client.fake_news
    nyt_coll = db.nyt_articles
    tg_coll = db.tg_articles

    # TG
    print("Loading The Guardian news")
    tg_cursor = tg_coll.find({})
    df_tg = pd.DataFrame(list(tg_cursor))

    cursor = tg_coll.find({})

    dfj = pd.io.json.json_normalize(df_tg['fields'])
    dfj_slice = dfj[['bodyText', 'charCount', 'wordcount', 'firstPublicationDate', 'byline', 'publication']]
    df_tg_slice = df_tg[['webTitle', 'webUrl', 'sectionName', 'webPublicationDate']]

    df_tg_bothslices = pd.concat([df_tg_slice, dfj_slice], axis=1)

    print("Saving TG dataset")
    df_tg_bothslices.to_csv('data/tg_articles_v2.csv', index=False)

    #NYT
    print("Loading NYT news")
    nyt_cursor = nyt_coll.find({})
    df_nyt = pd.DataFrame(list(nyt_cursor))

    df_nyt_byline = pd.io.json.json_normalize(df_nyt['byline'])
    df_nyt_headline = pd.io.json.json_normalize(df_nyt['headline'])
    df_nyt_slice = df_nyt[['body', 'pub_date', 'section_name', 'source', 'web_url', 'word_count']]
    df_nyt_b_h_concat = pd.concat([df_nyt_headline, df_nyt_byline], axis=1)
    df_nyt_slices = pd.concat([df_nyt_slice, df_nyt_b_h_concat], axis=1)

    df_nyt_slices.drop(['person', 'content_kicker', 'kicker', 'name', 'seo', 'sub'], axis=1, inplace=True)

    print("Saving NYT dataset")
    df_nyt_slices.to_csv('data/nyt_articles_v2.csv', index=False)

    #LETS MERGE
    print("Merging both datasets")
    df_nyt_slices.rename(index=str, columns={"original": "author", "print_headline": "headline"}, inplace=True)
    df_nyt_slices.drop(['main', 'source'], axis=1, inplace=True)

    df_tg_bothslices.rename(index=str, columns={"bodyText": "body",
                                                "webTitle": "headline",
                                                "firstPublicationDate": "pub_date",
                                                "sectionName": "section_name",
                                                "webUrl": "web_url",
                                                "wordcount": "word_count",
                                                "publication": "organization",
                                                "byline": "author"
                                                }, inplace=True)

    df_tg_bothslices.rename(index=str, columns={"webTitle": "print_headline"
                                                }, inplace=True)

    df_tg_bothslices.drop(['webPublicationDate', 'charCount'], axis=1, inplace=True)

    df_nyt_slices['source'] = "NEW_YORK_TIMES"
    df_tg_bothslices['source'] = "THE_GUARDIAN"

    result_df = pd.concat([df_nyt_slices, df_tg_bothslices], axis=0, join='inner')

    print("Saving Merged Dataset")

    result_df.to_csv('data/nyt_tg.csv', index=False)

    print("Done")

