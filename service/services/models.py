from typing import Any, Iterable
from django.db import models
from django.core.validators import MaxValueValidator
from django.db.models.signals import post_delete


from clients.models import Client
from services.recievers import delete_cache_total_sum
from services.tasks import set_comment, set_price


class Service(models.Model):
    name = models.CharField(max_length=50)
    full_price = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f'{self.name}'

    def __init__(self, *args: Any, **kwargs: Any): # Решение плохое, но оно работает :)
        super().__init__(*args, **kwargs)
        self.__full_price = self.full_price # В момент создания сохранили значение текущего состояния скидки

    def save(self, *args, **kwargs):
        if self.full_price != self.__full_price: # Если текущий процент скидки не равен прошлому то меняется
            for subscuprion in self.subscriptions.all():
                set_price.delay(subscuprion.id)
                set_comment.delay(subscuprion.id)


        return super().save(*args, **kwargs)
class Plan(models.Model):
    PLAN_TYPES = (
        ('full', 'Full'),
        ('student', 'Student'),
        ('discount', 'Discount')
    )

    plan_type = models.CharField(choices=PLAN_TYPES, max_length=10)
    discount_percent = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])

    def __str__(self) -> str:
        return f'{self.plan_type}'
    
    def __init__(self, *args: Any, **kwargs: Any): # Решение плохое, но оно работает :)
        super().__init__(*args, **kwargs)
        self.__discount_percent = self.discount_percent # В момент создания сохранили значение текущего состояния скидки

    def save(self, *args, **kwargs):
        if self.discount_percent != self.__discount_percent: # Если текущий процент скидки не равен прошлому то меняется
            for subscuprion in self.subscriptions.all():
                set_price.delay(subscuprion.id)
                set_comment.delay(subscuprion.id)

        return super().save(*args, **kwargs)

class Subscription(models.Model):
    client = models.ForeignKey(Client, related_name='subscriptions', on_delete=models.PROTECT)
    service = models.ForeignKey(Service, related_name='subscriptions', on_delete=models.PROTECT)
    plan = models.ForeignKey(Plan, related_name='subscriptions', on_delete=models.PROTECT)
    price = models.PositiveIntegerField(default=0)
    comment = models.CharField(max_length=55, default='', db_index=True)

    def __str__(self) -> str:
        return f'Client: {self.client} | Service: {self.service} | Plan: {self.plan}'

    def save(self, *args, **kwargs):
        creating = not bool(self.id)
        result = super().save(*args, **kwargs)
        if creating:
          set_price.delay(self.id)
        return result
    
post_delete.connect(delete_cache_total_sum, sender=Subscription)