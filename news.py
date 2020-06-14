"""news api config/setup file, instantiates newsapi instance for import"""

import os
from os import environ, path
from dotenv import load_dotenv

from newsapi import NewsApiClient
from datetime import datetime, timedelta

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

newsapi = NewsApiClient(api_key=os.environ.get('NEWSAPI_API_KEY'))

def get_articles(search_term):
    """pass search_term into newsapi.get_everything request and return response (2 pages of articles from the past 24 hours)"""
    now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    yesterday = (datetime.utcnow() - timedelta(hours = 24)).strftime('%Y-%m-%dT%H:%M:%S')
    all_articles = newsapi.get_everything(q=search_term, qintitle=search_term, language='en', from_param=yesterday, to=now, sort_by='relevancy', page=2)
    return all_articles