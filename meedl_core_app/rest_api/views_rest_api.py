__author__ = 'PerminovMA@live.ru'

from meedl_core_app.rest_api.serializers import AdvCampaignSerializer
from meedl_core_app.models import AdvCampaign
from rest_framework import generics
from rest_framework import permissions


class AdvCampaignsList(generics.ListAPIView):
    queryset = AdvCampaign.objects.all()
    serializer_class = AdvCampaignSerializer
    permission_classes = (permissions.IsAuthenticated,)