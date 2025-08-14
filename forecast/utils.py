from datetime import date
from django.db import transaction
from core.models import HistoricalRate
from .models import Forecast, ForecastAccuracy

def check_forecast_accuracy():
    """
    Проверяет прогнозы, для которых уже известен фактический курс, и сохраняет точность в ForecastAccuracy.
    """
    today = date.today()

    # Берём прогнозы, дата которых уже наступила или сегодня
    forecasts = Forecast.objects.filter(forecast_date__lte=today)

    for forecast in forecasts:
        # Берём фактический курс на дату прогноза
        historical = HistoricalRate.objects.filter(
            currency=forecast.currency,
            date=forecast.forecast_date
        ).first()

        if not historical:
            continue  # нет данных — пропускаем

        actual_rate = float(historical.rate)
        predicted_rate = float(forecast.predicted_rate)

        # Вычисляем точность
        accuracy = 100 - (abs(predicted_rate - actual_rate) / actual_rate * 100)

        # Сохраняем или обновляем запись
        with transaction.atomic():
            ForecastAccuracy.objects.update_or_create(
                forecast=forecast,
                defaults={
                    'actual_rate': actual_rate,
                    'accuracy': round(accuracy, 2)
                }
            )
