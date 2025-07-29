import os
import requests
from datetime import datetime, timedelta
from django.conf import settings
from core.models import HistoricalRate

API_KEY = os.environ.get('EXCHANGE_API_KEY')
BASE_URL = 'https://api.apilayer.com/exchangerates_data'

HEADERS = {
    "apikey": API_KEY
}

BASE_CURRENCY = "EUR"
SYMBOLS = ["USD", "BTC"]


def fetch_and_save_latest_rates():
    """Fetches and saves the latest exchange rates (used by Celery every hour)."""
    url = f"{BASE_URL}/latest"
    params = {
        "base": BASE_CURRENCY,
        "symbols": ",".join(SYMBOLS),
    }

    print(f"Requesting latest rates for base={BASE_CURRENCY}, symbols={SYMBOLS}...")
    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()
    print("Received response:", data)

    if not data.get("success"):
        print("Error:", data.get("error"))
        return

    date_str = data["date"]
    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

    for target_currency, rate in data["rates"].items():
        HistoricalRate.objects.update_or_create(
            date=date_obj,
            base_currency=BASE_CURRENCY,
            target_currency=target_currency,
            defaults={"rate": rate}
        )
        print(f"Saved rate: {target_currency} = {rate} on {date_str}")


def fetch_and_save_historical_rates(days_back=60):
    """Fetches and saves historical exchange rates for the last `days_back` days."""
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=days_back)

    url = f"{BASE_URL}/timeseries"
    params = {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "base": BASE_CURRENCY,
        "symbols": ",".join(SYMBOLS),
    }

    print(f"Requesting historical rates from {start_date} to {end_date}...")

    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()
    print("Received response:", data)

    if not data.get("success"):
        print("Error:", data.get("error"))
        return

    rates = data.get("rates", {})
    for date_str, rate_dict in rates.items():
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        for target_currency, rate in rate_dict.items():
            HistoricalRate.objects.update_or_create(
                date=date_obj,
                base_currency=BASE_CURRENCY,
                target_currency=target_currency,
                defaults={"rate": rate}
            )
            print(f"Saved rate: {target_currency} = {rate} on {date_str}")
