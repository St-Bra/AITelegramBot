from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from forecast.models import Currency

class NewsSource(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(unique=True)

    def __str__(self):
        return self.name


class NewsArticle(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    published_at = models.DateTimeField()
    url = models.URLField(unique=True)
    source = models.ForeignKey(NewsSource, on_delete=models.CASCADE, related_name='articles')
    related_currencies = models.ManyToManyField(Currency, related_name='news_articles')
    sentiment_score = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(-1.0), MaxValueValidator(1.0)]
    )
    def __str__(self):
        return self.title
