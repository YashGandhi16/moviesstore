from django.contrib import admin
from movies.models import Movie
from .models import Order, Item

admin.site.register(Order)
admin.site.register(Item)


