from django.contrib import admin

from menu.models import MenuItem


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("title", "url", "parent")
    list_filter = ("parent",)


admin.site.register(MenuItem, MenuItemAdmin)
