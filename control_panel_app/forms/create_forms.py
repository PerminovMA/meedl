__author__ = 'PerminovMA@live.ru'

from django.forms import ModelForm, ValidationError, BooleanField
from meedl_core_app.models import AdvCampaign, Offer


class OfferForm(ModelForm):
    class Meta:
        model = Offer
        fields = ['name', 'client', 'offer_url', 'revenue_per_lead', 'currency_type', 'limit_number_leads',
                  'use_sub_id']

    def clean_revenue_per_lead(self):
        revenue = self.cleaned_data.get('revenue_per_lead')

        if revenue is not None:
            if revenue < 0:
                raise ValidationError("Revenue_per_lead must be positive!", code="incorrect_data")
        else:
            raise ValidationError("Internal Error! Unable to get revenue_per_lead.", code="internal_error")

        return revenue

    def clean_use_sub_id(self):
        use_sub_id = self.cleaned_data.get('use_sub_id')
        client = self.cleaned_data.get('client')
        offer_url = self.cleaned_data.get('offer_url')

        if use_sub_id:
            if not offer_url:
                raise ValidationError("please, fill the offer url field", code="warning")

            if client:
                cpa_network = client.cpa_network
                if not cpa_network:
                    raise ValidationError("CPA network doesn't use for the Client of this Offer", code="warning")
                if cpa_network.sub_id_is_added(offer_url):
                    raise ValidationError("sub_id already added in offer_url", code="warning")
            else:
                raise ValidationError("please, choose client", code="warning")

        return use_sub_id


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