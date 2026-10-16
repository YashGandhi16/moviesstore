from django.contrib import admin
from .models import Movie, Review, Rating

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'movie', 'user', 'is_reported', 'date']
    list_filter = ['is_reported']

class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'movie', 'user', 'score']
    list_filter = ['score', 'movie']

admin.site.register(Movie, MovieAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Rating, RatingAdmin)