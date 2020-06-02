from django.contrib import admin

# Register your models here.
from listings.models import Book, Category

admin.site.register(Category)
admin.site.register(Book)
