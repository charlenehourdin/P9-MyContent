import pandas as pd
from scipy.sparse import csr_matrix
import pickle
import pickle
import urllib

clicks = pd.read_csv("https://recop9.blob.core.windows.net/fonctionp9/clicks.csv")
f = urllib.request.urlopen(clicks)
clicks = pickle.load(f)

with open('https://recop9.blob.core.windows.net/fonctionp9/recommender.LMF', 'rb') as handle:
    f = urllib.request.urlopen(handle)
    model = pickle.load(f)

def recommend_articles_LMF(data, user_id, n_reco=5):
    # compute interaction matrix
    interactions = data.groupby(['user_id', 'article_id']).size().reset_index(name='count')
    csr_item_user = csr_matrix((interactions['count'].astype(float),
                                (interactions['article_id'], interactions['user_id'])))
    csr_user_item = csr_matrix((interactions['count'].astype(float),
                                (interactions['user_id'], interactions['article_id'])))


    # obtenir des recommandations
    recommendations = model.recommend(user_id, csr_user_item[user_id], N=n_reco, filter_already_liked_items=True)

    # créer un dataframe avec les éléments recommandés et leurs scores
    rec_df = pd.DataFrame({'article_id': recommendations[0], 'score': recommendations[1]})
    rec_df['score'] = rec_df['score']

    # trier par score et sélectionner les meilleures recommandations
    rec_df = rec_df.sort_values(by='score', ascending=False).head(n_reco).round(4)

    return rec_df
