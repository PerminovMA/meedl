__author__ = 'PerminovMA@live.ru'

from meedl_core_app.rest_api.serializers import AdvCampaignSerializer, OfferSerializer, ClientSerializer
from meedl_core_app.models import AdvCampaign, Offer, Client
from rest_framework import generics
from rest_framework import permissions


class ClientsList(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (permissions.IsAuthenticated,)


class OffersList(generics.ListAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = (permissions.IsAuthenticated,)


class AdvCampaignsList(generics.ListAPIView):
    queryset = AdvCampaign.objects.all()
    serializer_class = AdvCampaignSerializer
    permission_classes = (permissions.IsAuthenticated,)


# class AdvCampaignDetail(generics.RetrieveAPIView):
#     queryset = AdvCampaign.objects.all()
#     serializer_class = AdvCampaignSerializer
#     permission_classes = (permissions.IsAuthenticated,)