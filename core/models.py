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
