from django.contrib import admin
from favorites.models import DivisionFavorite, ReviewFavorite

admin.site.register(DivisionFavorite)
admin.site.register(ReviewFavorite)