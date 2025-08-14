from django.contrib import admin
from .models import BotUser

@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", "username", "language_code", "created_at")
    list_filter = ("language_code", "created_at")
    search_fields = ("telegram_id", "username")
    ordering = ("-created_at",)
