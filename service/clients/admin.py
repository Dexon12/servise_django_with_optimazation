from django.contrib import admin

from clients.models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    fields = ['user', 'company_name', 'full_address']
    list_display = ['user', 'id', 'company_name', 'full_address']