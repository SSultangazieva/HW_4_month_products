from django.contrib import admin
from products.models import *

# Register your models here.

admin.site.register(Products)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Hashtag)
