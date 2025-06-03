from django.contrib import admin
from .models import Currency, HistoricalRate, Forecast, ForecastAccuracy

admin.site.register(Currency)
admin.site.register(HistoricalRate)
admin.site.register(Forecast)
admin.site.register(ForecastAccuracy)
