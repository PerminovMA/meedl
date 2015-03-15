__author__ = 'PerminovMA@live.ru'

from django.forms import ModelForm, ValidationError
from meedl_core_app.models import AdvCampaign


class AdvCampaignForm(ModelForm):
    class Meta:
        model = AdvCampaign
        fields = ['name', 'adv_platform', 'direction', 'campaign_cost', 'offer']

    def clean_campaign_cost(self):
        cost = self.cleaned_data.get('campaign_cost')

        if cost is not None:
            if cost < 0:
                raise ValidationError("Campaign cost must be positive!", code="incorrect_data")
        else:
            raise ValidationError("Internal Error! Unable to get campaign_cost.", code="internal_error")

        return cost

    def clean_offer(self):
        offer = self.cleaned_data.get('offer')
        if offer:
            if not offer.is_active:
                raise ValidationError("It's offer is not active!", code="relation_object_not_active")
        else:
            raise ValidationError("Internal Error! Unable to get offer.", code="internal_error")

        return offer