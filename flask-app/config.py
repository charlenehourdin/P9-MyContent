
from os import environ, path
from dotenv import load_dotenv
import os

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, '.env'))


class Config:
    # Global
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')
    SECRET_KEY = environ.get('SECRET_KEY')
    # Assets
    STATIC_FOLDER = 'app/static'
    TEMPLATES_FOLDER = 'app/templates'
    COMPRESSOR_DEBUG = environ.get('COMPRESSOR_DEBUG')


    #storage_account_name = os.environ["AzureWebJobsStorage"]
    #clicks_csv_url = os.environ["CLICKS_CSV_URL"]
    #recommender_model_url = os.environ["RECOMMENDER_MODEL_URL"]
