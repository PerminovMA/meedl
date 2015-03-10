__author__ = 'PerminovMA@live.ru'

from rest_framework import serializers
from meedl_core_app.models import AdvCampaign, Offer, AdvPlatform, DirectionAdv


class DirectionAdvSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectionAdv
        fields = ('id', 'name')


class AdvPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvPlatform
        fields = ('id', 'name', 'site_url')


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ('id', 'name')


class AdvCampaignSerializer(serializers.ModelSerializer):
    offer = OfferSerializer()
    adv_platform = AdvPlatformSerializer()
    direction = DirectionAdvSerializer()

    class Meta:
        model = AdvCampaign
        fields = ('id', 'name', 'adv_platform', 'offer', 'direction', 'campaign_cost', 'is_active', 'count_clicks')