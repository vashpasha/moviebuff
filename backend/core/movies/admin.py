# admin.py
from django.contrib import admin
from .models import FeaturedMovie

@admin.register(FeaturedMovie)
class FeaturedMovieAdmin(admin.ModelAdmin):
    list_display = ('movie_id', 'added_at')
    search_fields = ('movie_id',)