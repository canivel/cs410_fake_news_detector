import pandas as pd

def remove_by_world (author):
    return author.replace('By ', '')

if __name__ == "__main__":
    print("Loading Datasets")
    kaggle_train = pd.read_csv('data/kaggle/train.csv')
    kaggle_fake = pd.read_csv('data/kaggle/fake.csv', parse_dates=['published'])
    df_nyt_tg = pd.read_csv('data/nyt_tg.csv', parse_dates=['pub_date'])


    kaggle_fake = kaggle_fake[kaggle_fake['language'] == 'english']

    # fill nans
    print("Fill Missing Data at Kaggles Dataset 1")
    kaggle_fake['author'].fillna('No author', inplace=True)
    kaggle_fake['title'].fillna('No title', inplace=True)
    kaggle_fake['text'].fillna('No text', inplace=True)

    kaggle_fake.drop(['domain_rank', 'thread_title', 'main_img_url'], axis=1, inplace=True)

    kaggle_fake['label'] = 1

    kaggle_fake_slice = kaggle_fake[['title', 'author', 'text', 'label']]

    kaggle_train.drop('id', axis=1, inplace=True)

    print("Appending Both kaggle datasets")

    kaggle_df = kaggle_train.append(kaggle_fake_slice)

    df_nyt_tg['label'] = 0
    df_nyt_tg_slice = df_nyt_tg[['headline', 'author', 'body', 'label']]

    df_nyt_tg_slice.columns = ['title', 'author', 'text', 'label']

    print("Fill Missing Data at NYT and TG Dataset")
    # fill nans
    df_nyt_tg_slice['author'].fillna('No author', inplace=True)
    df_nyt_tg_slice['title'].fillna('No title', inplace=True)
    df_nyt_tg_slice['author'] = df_nyt_tg_slice['author'].apply(remove_by_world)

    print("Appending Both kaggle datasets")
    df_final = kaggle_df.append(df_nyt_tg_slice)
    df_final.dropna(inplace=True)

    print("Saving final Dataset for preprocessing and training")

    df_final.to_csv('data/df_final_v1.csv', index=False)

    print("Done")