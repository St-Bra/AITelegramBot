from django.contrib import admin
from .models import NewsSource, NewsArticle

@admin.register(NewsSource)
class NewsSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    search_fields = ('name', 'url')

@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'source')
    list_filter = ('source', 'published_at')
    search_fields = ('title',)
