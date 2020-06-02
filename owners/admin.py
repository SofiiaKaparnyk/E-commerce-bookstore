from django.contrib import admin

# Register your models here.
from owners.models import Owner


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    exclude = ['rate']
    list_display = ['id', 'user', 'phone', 'city', 'rate']
    list_display_links = ['id', 'user']
    search_fields = ['city', 'user']
    list_per_page = 25
