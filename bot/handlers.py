from telegram import Update
from telegram.ext import ContextTypes
from asgiref.sync import sync_to_async
from core.models import Currency, HistoricalRate
from datetime import date
from forecast.models import Forecast

@sync_to_async
def get_eur_rates():
    try:
        usd = Currency.objects.get(code="USD")
        btc = Currency.objects.get(code="BTC")
    except Currency.DoesNotExist:
        return None

    today = date.today()

    usd_rate_obj = HistoricalRate.objects.filter(currency=usd, date=today).first()
    btc_rate_obj = HistoricalRate.objects.filter(currency=btc, date=today).first()

    if not usd_rate_obj or not btc_rate_obj:
        return None

    return usd_rate_obj.rate, btc_rate_obj.rate


@sync_to_async
def get_forecasts():
    eur = Currency.objects.get(code='EUR')
    today = date.today()
    return list(Forecast.objects.filter(currency=eur, forecast_date__gte=today).order_by('forecast_date')[:7])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот прогноза курсов валют.")


async def eur(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rates = await get_eur_rates()
    if rates:
        usd_rate, btc_rate = rates
        text = f"1 EUR = {usd_rate} USD\n1 EUR = {btc_rate} BTC"
        await update.message.reply_text(text)
    else:
        await update.message.reply_text("Курсы евро на сегодня не найдены.")


async def forecast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    forecasts = await get_forecasts()
    if not forecasts:
        await update.message.reply_text("Прогнозы на ближайшие дни пока не доступны.")
        return

    text = "Прогноз курса евро на ближайшие дни:\n"
    for f in forecasts:
        text += f"{f.forecast_date}: 1 EUR = {f.predicted_rate:.4f} USD\n"

    await update.message.reply_text(text)
