from django.contrib import admin
from .models import Forecast, ForecastAccuracy
from core.models import Currency, HistoricalRate

admin.site.register(Currency)
admin.site.register(HistoricalRate)
admin.site.register(Forecast)
admin.site.register(ForecastAccuracy)
