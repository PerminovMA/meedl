__author__ = 'PerminovMA@live.ru'

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from meedl_core_app.rest_api.views_rest_api import AdvCampaignsList

urlpatterns = [
    url(r'^adv_campaigns/$', AdvCampaignsList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)