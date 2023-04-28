from django.contrib import admin
from .models import MenuItem


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'menu_name', 'parent')
    list_filter = ('menu_name', 'parent')
    search_fields = ('name', 'url', 'menu_name')
    ordering = ('menu_name', 'parent__id', 'id')

admin.site.register(MenuItem, MenuItemAdmin)
