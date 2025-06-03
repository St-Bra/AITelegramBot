from django.db import models

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.code

class HistoricalRate(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    date = models.DateField()
    rate = models.DecimalField(max_digits=20, decimal_places=6)

    class Meta:
        unique_together = ('currency', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.currency} - {self.date}: {self.rate}"

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

