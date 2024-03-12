
from rest_framework import serializers

from services.models import Plan, Subscription

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ('__all__')

class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer() # Wrapped Serializer

    client_name = serializers.CharField(source='client.company_name')
    email = serializers.CharField(source='client.user.email')
    price = serializers.SerializerMethodField()

    def get_price(self, instance): # instance == Subscription
        return (instance.service.full_price - instance.service.full_price * (instance.plan.discount_percent / 100))

    class Meta:
        model = Subscription
        """
        If we need to show only plan id we dont need to do wrapped serializer, 
        because model Subscription already contains plan`s id becouse it have a Foreign field 
        """
        fields = ['id', 'plan_id', 'client_name', 'email', 'plan', 'price']
        