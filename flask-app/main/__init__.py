import logging
import azure.functions as func
import flask
from flask import Flask, render_template, request
import pandas as pd
import urllib
import time
import pickle
from scipy.sparse import csr_matrix
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os
import io
import requests
import gzip

load_dotenv()  # charge les variables d'environnement depuis .env

url = 'https://mycontentstockage.blob.core.windows.net/recop9/clicks_sample.csv'
clicks=requests.get(url).content
clicks=pd.read_csv(io.StringIO(clicks.decode('utf-8')))

#url = 'https://mycontentstockage.blob.core.windows.net/recop9/recommender.LMF.pickle.gz'
#f = urllib.request.urlopen(url)
#model = pickle.#

url = 'https://mycontentstockage.blob.core.windows.net/recop9/recommender.LMF.pickle.gz'
with urllib.request.urlopen(url) as response:
    with gzip.GzipFile(fileobj=response) as uncompressed:
        model = pickle.load(uncompressed)

logging.info('Python HTTP trigger function processed a request.')

app = Flask(__name__)

# Load data and model
#clicks = pd.read_csv("/Users/charlenehourdin/Documents/Openclassrooms/Projet/p9/api/flask-app/main/data/clicks.csv")
#with open('/Users/charlenehourdin/Documents/Openclassrooms/Projet/p9/api/flask-app/main/model/recommender.LMF', 'rb') as handle:
#   model = pickle.load(handle)

# Routes
@app.route("/")
def home():
    return render_template('home.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    user_id = int(request.form['user_id'])
    n_reco = int(request.form['n_reco'])
    recommendations = recommend_articles_LMF(clicks, user_id, n_reco)
    result = recommendations.to_dict('records')
    return render_template('recommendation.html', result=result, user_id=user_id)

    
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
    rec_df['score'] = rec_df['score'].round(2)

    # trier par score et sélectionner les meilleures recommandations
    rec_df = rec_df.sort_values(by='score', ascending=False).head(n_reco)

    return rec_df


# Azure Functions
def main(req: func.HttpRequest) -> func.HttpResponse:
    return func.WsgiMiddleware(app).handle(req)


