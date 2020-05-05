from django.contrib import admin
from collection.models import Collection, Publication, ItemList

# Register your models here.
admin.site.register(Collection)
admin.site.register(Publication)
admin.site.register(ItemList)