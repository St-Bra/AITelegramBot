from django.db import models
from django.utils import timezone

class BotUser(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    language_code = models.CharField(
        max_length=2,
        choices=[
            ('ru', 'Russian'),
            ('en', 'English'),
            ('pl', 'Polish'),

        ],
        default='en'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username or str(self.telegram_id)