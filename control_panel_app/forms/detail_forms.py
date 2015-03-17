__author__ = 'PerminovMA@live.ru'

from django.forms import ModelForm, ValidationError
from meedl_core_app.models import AdvCampaign
from django.forms import TextInput, CharField


class DetailAdvCampaignForm(ModelForm):
    tracking_url = CharField(label="tracking url", required=False,
                             widget=TextInput(attrs={'size': '50rem;', 'readonly': True}))
    postback_url = CharField(label="postback url", required=False,
                             widget=TextInput(attrs={'size': '50rem;', 'readonly': True}))

    class Meta:
        model = AdvCampaign
        fields = ['name', 'adv_platform', 'direction', 'campaign_cost', 'offer', 'is_active', 'count_clicks',
                  'count_leads', 'offer_url', 'tracking_url', 'postback_url']
        widgets = {
            'offer_url': TextInput(attrs={'readonly': True, 'size': '50rem;'}),
        }
        labels = {
            'offer_url': "offer URL",
        }

    def clean_campaign_cost(self):
        cost = self.cleaned_data.get('campaign_cost')

        if cost is not None:
            if cost < 0:
                raise ValidationError("Campaign cost must be positive!", code="incorrect_data")
        else:
            raise ValidationError("Internal Error! Unable to get campaign_cost.", code="internal_error")

        return cost