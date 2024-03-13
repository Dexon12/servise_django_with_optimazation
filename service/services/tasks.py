import time
from celery import shared_task
from django.db.models import F
from celery_singleton import Singleton


@shared_task(base=Singleton) # Для того чтобы если пользователь спамит однотипными задачами учитывалась только последняя
def set_price(subscription_id): # Нельзя просто передать объект Subscription, потому что за то время пока обхект хранится в очереди объект может уже измениться и в ьд будет уже в другом виде
    """
    При сохранении или создании объекта асинхронно считается поле price, для того чтобы избежать annotate и в следсвие двух JOIN
    """
    
    from services.models import Subscription # Решение такое себе, но это нужно чтобы избежать кроссимпортов

    time.sleep(5)
    
    # subscription = Subscription.objects.get(id=subscription_id) # Плохо что еще раз обращаемся к ьд, но это необходимо так что окей
    subscription = Subscription.objects.filter(id=subscription_id).annotate(annotated_price=F('service__full_price') - F('service__full_price') * F('plan__discount_percent') / 100.00).first() # add price field on the db lvl. It`s better to annotate something, then send request to db 
    # new_price = (subscription.service.full_price - subscription.service.full_price * subscription.plan.discount_percent / 100)
    subscription.price = subscription.annotated_price
    subscription.save()