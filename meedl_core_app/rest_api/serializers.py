__author__ = 'PerminovMA@live.ru'

from rest_framework import serializers
from meedl_core_app.models import AdvCampaign, Offer, AdvPlatform, DirectionAdv, Client
from django.contrib.auth.models import User


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class ClientSerializer(serializers.ModelSerializer):
    manager = ManagerSerializer()

    class Meta:
        model = Client
        fields = ('id', 'manager', 'name', 'site_url', 'type')


class DirectionAdvSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectionAdv
        fields = ('id', 'name')


class AdvPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvPlatform
        fields = ('id', 'name', 'site_url')


class OfferSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    manager = ManagerSerializer()

    class Meta:
        model = Offer
        fields = (
            'id', 'name', 'client', 'manager', 'offer_url', 'revenue_per_lead', 'currency_type', 'limit_number_leads',
            'is_active')


class AdvCampaignSerializer(serializers.ModelSerializer):
    offer = OfferSerializer()
    adv_platform = AdvPlatformSerializer()
    direction = DirectionAdvSerializer()

    class Meta:
        model = AdvCampaign
        fields = ('id', 'name', 'adv_platform', 'offer', 'direction', 'campaign_cost', 'is_active', 'count_clicks',
                  'count_leads')