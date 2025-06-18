from celery import shared_task
from core.services.news.news_loader import NewsLoader

@shared_task
def fetch_and_save_news_task():
    loader = NewsLoader()
    loader.fetch_and_save_articles()