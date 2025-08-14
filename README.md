# AI Telegram Bot: Прогноз курса EUR

Интеллектуальный Telegram-бот, который прогнозирует курс евро на неделю вперёд, используя анализ новостей и исторических данных.

---

Функционал:

- Прогноз на 7 дней по евро
- Анализ новостей и их влияние на прогноз
- Прогноз на основе тренда и новостей (/forecast)
- Подписка на ежедневные прогнозы (/subscribe)
- История точности прогнозов (/history)
- Панель администратора (Django Admin)

---

Используемые технологии:

Backend:
- [Python 3.12+](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Celery](https://docs.celeryq.dev/en/stable/) + [Redis](https://redis.io/)

Анализ данных и прогноз:
- [Prophet (Meta)](https://facebook.github.io/prophet/) — прогнозирование временных рядов с учётом дополнительных регрессоров
- [pandas](https://pandas.pydata.org/) — обработка и подготовка данных
- [VADER](https://github.com/cjhutto/vaderSentiment) — анализ тональности новостей

Источники данных:
- Курсы валют: [exchangeratesapi.io](https://exchangeratesapi.io/)
- Новости: [NewsAPI](https://newsapi.org/)

Telegram-бот:
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
