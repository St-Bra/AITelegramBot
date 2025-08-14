from telegram import Update
from telegram.ext import ContextTypes, CallbackContext
from asgiref.sync import sync_to_async

from bot.models import BotUser
from core.models import Currency, HistoricalRate
from datetime import date, timezone
from forecast.models import Forecast, ForecastAccuracy


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
    await register_user(update)
    await update.message.reply_text("Привет! Я бот прогноза курсов валют. Что бы увидеть доступные команды используй /help.")


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

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Доступные команды:\n"
        "/start - приветствие\n"
        "/eur - текущий курс евро\n"
        "/forecast - прогноз курса евро на ближайшие дни\n"
        "/help - показать этот список команд\n"
        "/subscribe - подписаться на ежедневные прогнозы\n"
        "/unsubscribe - отписаться от ежедневных прогнозов\n"
        "/history - история точности прогнозов"
    )
    await update.message.reply_text(text)

@sync_to_async
def register_user(update):
    """Create or update BotUser when /start is received"""
    tg_user = update.effective_user
    BotUser.objects.update_or_create(
        telegram_id=tg_user.id,
        defaults={
            'username': tg_user.username,
            'language_code': tg_user.language_code or 'en'
        }
    )

# === Подписка ===
@sync_to_async
def set_subscription(telegram_id, subscribe=True):
    user, _ = BotUser.objects.get_or_create(
        telegram_id=telegram_id,
        defaults={
            "username": "",
            "language_code": "en"
        }
    )
    user.is_subscribed = subscribe
    user.save()
    return user

async def subscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_subscription(update.effective_user.id, True)
    await update.message.reply_text("✅ Вы подписались на ежедневные прогнозы по EUR!")

async def unsubscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_subscription(update.effective_user.id, False)
    await update.message.reply_text("❌ Вы отписались от ежедневных прогнозов.")

# === История точности ===
@sync_to_async
def get_last_accuracy_records(days=7):
    return list(
        ForecastAccuracy.objects
        .select_related('forecast')  # подгружаем связанный forecast сразу
        .order_by('-forecast__forecast_date')[:days]
    )

async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    records = await get_last_accuracy_records()
    if not records:
        await update.message.reply_text("📭 Данных о точности пока нет.")
        return

    text = "📊 История точности прогнозов за последние 7 дней:\n\n"
    for record in records:
        # Теперь record.forecast уже загружен, дополнительных запросов не будет
        text += f"{record.forecast.forecast_date}: {record.accuracy:.2f}%\n"

    await update.message.reply_text(text)