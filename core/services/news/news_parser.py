import requests
from datetime import datetime
from django.conf import settings

class NewsFetcher:
    BASE_URL = "https://newsapi.org/v2/everything"

    def __init__(self):
        self.api_key = settings.NEWS_API_KEY

    def fetch_news(self, query="USD OR EUR OR BTC", language="en", from_date=None, to_date=None, page_size=20):
        """
        Получает новости по ключевым словам.
        """
        params = {
            "q": query,
            "language": language,
            "sortBy": "publishedAt",
            "apiKey": self.api_key,
            "pageSize": page_size
        }

        if from_date:
            params["from"] = from_date.strftime('%Y-%m-%d')
        if to_date:
            params["to"] = to_date.strftime('%Y-%m-%d')

        response = requests.get(self.BASE_URL, params=params)

        if response.status_code == 200:
            return response.json().get("articles", [])
        else:
            raise Exception(f"News API error: {response.status_code} — {response.text}")