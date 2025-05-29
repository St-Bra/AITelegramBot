# 📈 AI Telegram Bot: Прогноз курса валют и криптовалют

Проект дипломной работы: интеллектуальный Telegram-бот, который прогнозирует курс USD, EUR и BTC на неделю вперёд, используя анализ новостей и исторических данных.

---

## 🚀 Функционал

- 🔮 Прогноз на 7 дней по USD, EUR и BTC (`/predict usd`)
- 📊 График прогноза (`/chart eur`)
- 📰 Анализ новостей и их влияние на прогноз (`/news`)
- 🤖 Объяснение прогноза (на основе тренда и новостей)
- ⏱️ Подписка на ежедневные прогнозы (`/subscribe btc`)
- 📈 История точности прогнозов (`/history usd`)
- 🛠️ Панель администратора (Django Admin)

---

## 🧠 Используемые технологии

### Backend
- [Python 3.10+](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Celery](https://docs.celeryq.dev/en/stable/) + Redis

### Анализ данных и прогноз
- [Prophet (Meta)](https://facebook.github.io/prophet/)
- [pandas](https://pandas.pydata.org/)
- [matplotlib / plotly](https://plotly.com/python/)
- [spaCy](https://spacy.io/) / [TextBlob](https://textblob.readthedocs.io/) / [transformers](https://huggingface.co/transformers/)

### Telegram-бот
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
