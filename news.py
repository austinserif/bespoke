import os
from os import environ, path
from dotenv import load_dotenv

from newsapi import NewsApiClient

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

newsapi = NewsApiClient(api_key=os.environ.get('NEWSAPI_API_KEY'))