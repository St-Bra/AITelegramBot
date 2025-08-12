import requests
from datetime import datetime, timedelta, date
from core.models import HistoricalRate, Currency
from django.conf import settings

BASE_URL = "https://api.apilayer.com/exchangerates_data"
BASE_CURRENCY = "EUR"
SYMBOLS = ["USD", "BTC"]
HEADERS = {
    "apikey": settings.EXCHANGE_API_KEY
}

def fetch_and_save_latest_rates(base_currency='EUR', symbols=['USD', 'BTC']):
    url = "https://api.exchangeratesapi.io/v1/latest"
    params = {
        "access_key": settings.EXCHANGE_API_KEY,
        "base": base_currency,
        "symbols": ','.join(symbols)
    }

    print(f"Requesting rates for base={base_currency} symbols={symbols}")
    response = requests.get(url, params=params)
    data = response.json()
    print(f"Received response: {data}")

    rates = data.get("rates", {})

    if not rates:
        print("No rates found in response.")
        return

    for code, rate in rates.items():
        currency, _ = Currency.objects.get_or_create(code=code)
        HistoricalRate.objects.update_or_create(
            currency=currency,
            date=date.today(),
            defaults={'rate': rate}
        )
        print(f"Saved rate: {code} = {rate} on {date.today()}")


def fetch_and_save_historical_rates(days=30, base_currency='EUR', symbols=['USD']):
    for i in range(days):
        day = date.today() - timedelta(days=i+1)
        day_str = day.isoformat()
        url = f"https://api.frankfurter.app/{day_str}"
        params = {
            "from": base_currency,
            "to": ','.join(symbols)
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            rates = data.get("rates", {})
            if rates:
                for code, rate in rates.items():
                    currency, _ = Currency.objects.get_or_create(code=code)
                    HistoricalRate.objects.update_or_create(
                        currency=currency,
                        date=day,
                        defaults={"rate": rate}
                    )
                print(f"Saved rates for {day_str}: {rates}")
            else:
                print(f"No rates data for {day_str}")
        else:
            print(f"Failed to fetch data for {day_str}, status code {response.status_code}")

