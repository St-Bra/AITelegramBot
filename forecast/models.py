from django.db import models
from core.models import Currency


class Forecast(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    forecast_date = models.DateField()
    predicted_rate = models.DecimalField(max_digits=20, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('currency', 'forecast_date')
        ordering = ['forecast_date']

    def __str__(self):
        return f"Forecast {self.currency} for {self.forecast_date}: {self.predicted_rate}"


class ForecastAccuracy(models.Model):
    forecast = models.ForeignKey(Forecast, on_delete=models.CASCADE)
    actual_rate = models.DecimalField(max_digits=20, decimal_places=6)
    accuracy = models.FloatField()
    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Accuracy for {self.forecast} = {self.accuracy}%"
