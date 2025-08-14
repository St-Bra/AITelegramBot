from celery import shared_task
from news.models import NewsArticle
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from core.services.forecast import make_and_save_forecast


@shared_task
def analyze_news_with_vader():
    analyzer = SentimentIntensityAnalyzer()

    unprocessed_news = NewsArticle.objects.filter(sentiment_score__isnull=True)[:20]

    for article in unprocessed_news:
        text = f"{article.title}\n{article.content}"
        try:
            sentiment = analyzer.polarity_scores(text)
            score = sentiment["compound"]

            article.sentiment_score = score
            article.save()
        except Exception as e:
            print(f"Ошибка анализа новости {article.id}: {e}")

@shared_task
def daily_forecast_task():
    make_and_save_forecast()
