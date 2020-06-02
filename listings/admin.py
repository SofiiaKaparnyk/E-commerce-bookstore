from django.contrib import admin

# Register your models here.
from listings.models import Book, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    exclude = ['rate']
    list_display = ['id', 'title', 'author', 'price', 'owner', 'rate']
    list_display_links = ['id', 'title', 'owner']
    list_filter = ['price']
    search_fields = ['title', 'author', 'rate']
    list_per_page = 25
