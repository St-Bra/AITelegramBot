from celery import shared_task
from core.services.exchange import fetch_and_save_latest_rates

@shared_task
def update_exchange_rates_task():
    fetch_and_save_latest_rates()