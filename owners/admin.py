from django.contrib import admin

from owners.models import Owner


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'phone', 'city']
    list_display_links = ['id', 'user']
    search_fields = ['city', 'user']
    list_per_page = 25
