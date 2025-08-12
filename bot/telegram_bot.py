from telegram.ext import ApplicationBuilder, CommandHandler
from django.conf import settings
from bot.handlers import start, eur, forecast
def run_bot():
    app = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("eur", eur))
    app.add_handler(CommandHandler("forecast", forecast))

    print("Бот запущен")
    app.run_polling()
