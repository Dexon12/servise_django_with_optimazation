from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from clients.models import Client
from services.serializers import SubscriptionSerializer
from django.db.models import Prefetch
from services.models import Subscription
from django.db.models import F, Sum


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        'service',
        Prefetch('client', 
                queryset=Client.objects.all().select_related('user').only(
                    'company_name', 'user__email'
                    ))
        ).annotate(price=F('service__full_price') - F('service__full_price') * F('plan__discount_percent') / 100.00) # add price field on the db lvl. It`s better to annotate something, then send request to db 

    # Do 1 request but with JOIN
    # queryset = Subscription.objects.all().select_related('plan', 'client', 'client__user').only(
    #     'client__user__email',
    #     'client__company_name',
    #     'plan_id',
    # )
    serializer_class = SubscriptionSerializer
    

    def list(self, request, *args, **kwargs): # По дефолту тут обрабатывается запрос и формируется ответ нашему клиенту
        queryset = self.filter_queryset(self.get_queryset())

        response = super().list(request, *args, **kwargs)

        response_data = {'result': response.data} # Better not to do that 
        response_data['total_amount'] = queryset.aggregate(total=Sum('price')).get('total') # It`s better to aggregate on db lvl. We can do that on this lvl because we annotate on the db lvl too
        response.data = response_data

        return response 
        