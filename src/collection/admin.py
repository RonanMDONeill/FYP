from django.contrib import admin
from .models import Collection, Publication, Author, ItemList, PubRating

# Register the models for the Collection app
admin.site.register(Collection)
admin.site.register(Publication)
admin.site.register(Author)
admin.site.register(ItemList)
admin.site.register(PubRating)