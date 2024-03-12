from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from clients.models import Client
from services.serializers import SubscriptionSerializer
from django.db.models import Prefetch
from services.models import Subscription


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        'service',
        Prefetch('client', 
                queryset=Client.objects.all().select_related('user').only(
                    'company_name', 'user__email'
                    ))
        ) # do 3 requests to db

    # Do 1 request but with JOIN
    # queryset = Subscription.objects.all().select_related('plan', 'client', 'client__user').only(
    #     'client__user__email',
    #     'client__company_name',
    #     'plan_id',
    # )
    serializer_class = SubscriptionSerializer
    