from .news_parser import NewsFetcher
from news.models import NewsArticle, NewsSource
from forecast.models import Currency
from datetime import datetime


class NewsLoader:
    def __init__(self):
        self.fetcher = NewsFetcher()  # создаём экземпляр fetcher'а

    def fetch_and_save_articles(self, **kwargs):
        """
        Получает и сохраняет статьи.
        """
        articles = self.fetcher.fetch_news(**kwargs)
        self.save_articles(articles)

    def save_articles(self, articles):
        for item in articles:
            url = item.get("url")
            if NewsArticle.objects.filter(url=url).exists():
                continue

            source_data = item.get("source", {})
            source, _ = NewsSource.objects.get_or_create(
                name=source_data.get("name", "Unknown"),
                defaults={"url": f"https://{source_data.get('name', 'unknown').lower()}.com"}
            )

            article = NewsArticle.objects.create(
                title=item.get("title", "")[:500],
                content=item.get("content", "") or "",
                published_at=datetime.fromisoformat(item["publishedAt"].replace("Z", "+00:00")),
                url=url,
                source=source
            )

            text = (item.get("title", "") + item.get("description", "")).lower()
            for currency in Currency.objects.all():
                if currency.code.lower() in text:
                    article.related_currencies.add(currency)

            article.save()