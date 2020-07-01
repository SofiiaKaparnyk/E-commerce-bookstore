from django.contrib import admin

# Register your models here.
from listings.models import Book, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['id', 'title', 'author', 'rate']
    list_display_links = ['id', 'title']
    search_fields = ['title', 'author', 'rate']
    list_per_page = 25
    filter_horizontal = ('category',)
