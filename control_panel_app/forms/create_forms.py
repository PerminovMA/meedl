__author__ = 'PerminovMA@live.ru'

from django.forms import ModelForm
from meedl_core_app.models import AdvCampaign


class AdvCampaignForm(ModelForm):
    class Meta:
        model = AdvCampaign
        fields = ['name', 'adv_platform', 'direction', 'campaign_cost', 'offer']