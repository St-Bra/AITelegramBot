import pandas as pd
from prophet import Prophet
from core.models import Currency, HistoricalRate
from datetime import date, timedelta
from django.db import transaction
from forecast.models import Forecast

def get_eur_historical_data():
    """Берём исторические курсы евро из базы, подготавливаем DataFrame для Prophet."""
    usd = Currency.objects.get(code='USD')
    rates = HistoricalRate.objects.filter(currency=usd).order_by('date')
    data = [(r.date, float(r.rate)) for r in rates]
    df = pd.DataFrame(data, columns=['ds', 'y'])
    return df

def train_and_forecast(df, days=7):
    """Обучаем модель Prophet и делаем прогноз на days вперёд."""
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=days)
    forecast = model.predict(future)
    return forecast[['ds', 'yhat']].tail(days)

@transaction.atomic
def save_forecasts(forecast_df):
    """Сохраняем прогнозы в базу (для евро)."""
    eur = Currency.objects.get(code='EUR')
    for _, row in forecast_df.iterrows():
        Forecast.objects.update_or_create(
            currency=eur,
            forecast_date=row['ds'].date(),
            defaults={'predicted_rate': row['yhat']}
        )

def make_and_save_forecast():
    """Главная функция — берёт данные, строит прогноз и сохраняет."""
    df = get_eur_historical_data()
    if df.empty:
        print("Нет данных для прогноза")
        return
    forecast_df = train_and_forecast(df)
    save_forecasts(forecast_df)
    print(f"Прогноз на {len(forecast_df)} дней сохранён")
