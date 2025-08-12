from django.core.management.base import BaseCommand
from core.services.forecast import make_and_save_forecast

class Command(BaseCommand):
    help = "Сделать прогноз курса евро и сохранить его в базу"

    def handle(self, *args, **kwargs):
        make_and_save_forecast()
