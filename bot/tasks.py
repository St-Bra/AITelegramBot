from asgiref.sync import async_to_sync
from celery import shared_task
from django.utils import timezone
from bot.models import BotUser
from core.models import Currency
from forecast.models import Forecast
from telegram import Bot
from django.conf import settings

@shared_task
def send_daily_forecast():
    """
    Отправка прогноза всем пользователям, которые подписаны на EUR.
    """
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    eur = Currency.objects.get(code='EUR')
    today = timezone.localdate()
    forecasts = Forecast.objects.filter(currency=eur, forecast_date__gte=today).order_by('forecast_date')[:7]

    if not forecasts:
        return "Прогнозы на сегодня не найдены"

    text = "Прогноз курса евро на ближайшие дни:\n"
    for f in forecasts:
        text += f"{f.forecast_date}: 1 EUR = {f.predicted_rate:.4f} USD\n"

    users = BotUser.objects.filter(is_subscribed=True)
    for user in users:
        try:
            async_to_sync(bot.send_message)(chat_id=user.telegram_id, text=text)
        except Exception as e:
            print(f"Ошибка отправки пользователю {user.telegram_id}: {e}")
