from django.contrib import admin
from .models import Author, PubRating

# Register your models here.
admin.site.register(Author)
admin.site.register(PubRating)