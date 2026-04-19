from django.contrib import admin
from .models import User


@admin.register(User)
class ShopConfigAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'is_staff')
    search_fields = ('first_name', 'last_name', 'email')


