import pandas as pd
from prophet import Prophet
from core.models import Currency, HistoricalRate
from forecast.models import Forecast
from news.models import NewsArticle  # модель новостей
from datetime import timedelta
from django.db import transaction

def get_average_sentiment_for_date(date_):
    """Возвращает средний compound score новостей по USD за дату (или 0 если нет новостей)."""
    news_items = NewsArticle.objects.filter(
        related_currencies__code='USD',
        published_at__date=date_
    )
    if not news_items.exists():
        return 0.0
    # берем сохраненный sentiment_score, если он уже посчитан
    scores = [n.sentiment_score for n in news_items if n.sentiment_score is not None]
    return sum(scores) / len(scores) if scores else 0.0

def get_usd_historical_data_with_sentiment():
    """Берём исторические курсы USD и добавляем регрессор sentiment."""
    usd = Currency.objects.get(code='USD')
    rates = HistoricalRate.objects.filter(currency=usd).order_by('date')
    data = []
    for r in rates:
        sentiment = get_average_sentiment_for_date(r.date)
        data.append((r.date, float(r.rate), sentiment))
    df = pd.DataFrame(data, columns=['ds', 'y', 'sentiment'])
    return df

def train_and_forecast(df, days=7):
    """Обучаем модель Prophet с регрессором sentiment и делаем прогноз на days вперед."""
    model = Prophet()
    model.add_regressor('sentiment')
    model.fit(df)

    future = model.make_future_dataframe(periods=days)
    last_sentiment = df['sentiment'].tail(3).mean()
    future['sentiment'] = [last_sentiment] * len(future)

    forecast = model.predict(future)
    return forecast[['ds', 'yhat']].tail(days)

@transaction.atomic
def save_forecasts(forecast_df):
    """Сохраняем прогнозы в базу для евро."""
    eur = Currency.objects.get(code='EUR')
    for _, row in forecast_df.iterrows():
        Forecast.objects.update_or_create(
            currency=eur,
            forecast_date=row['ds'].date(),
            defaults={'predicted_rate': row['yhat']}
        )

def make_and_save_forecast():
    """Главная функция — берёт данные, строит прогноз и сохраняет."""
    df = get_usd_historical_data_with_sentiment()
    if df.empty:
        print("Нет данных для прогноза")
        return
    forecast_df = train_and_forecast(df)
    save_forecasts(forecast_df)
    print(f"Прогноз на {len(forecast_df)} дней сохранён")
