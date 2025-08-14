from django.contrib import admin
from .models import Forecast, ForecastAccuracy
from core.models import Currency, HistoricalRate

admin.site.site_header = "CurrencyOracleBot administration"
admin.site.site_title = "CurrencyOracleBot Admin"
admin.site.index_title = "CurrencyOracleBot dashboard"
admin.site.register(Currency)
admin.site.register(HistoricalRate)
admin.site.register(Forecast)

@admin.register(ForecastAccuracy)
class ForecastAccuracyAdmin(admin.ModelAdmin):
    list_display = ('forecast', 'actual_rate', 'accuracy', 'checked_at')
    list_filter = ('checked_at', 'accuracy')
    search_fields = ('forecast__currency__code',)
