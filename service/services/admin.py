from django.contrib import admin

from .models import Subscription, Plan, Service

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['client', 'id', 'service', 'plan']


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['plan_type', 'id', 'discount_percent']
    

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'full_price']
    