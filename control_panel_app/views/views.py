from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from control_panel_app.forms.create_forms import AdvCampaignForm
from control_panel_app.forms.detail_forms import DetailAdvCampaignForm
from meedl_core_app.models import AdvCampaign
from django.http import Http404


@login_required()
def index_page(request):
    context = {}
    return render(request, 'control_panel_app/control_panel_main.html', context)


@login_required()
def create_campaign_page(request):
    if request.method == "POST":
        form = AdvCampaignForm(request.POST)

        if form.is_valid():
            new_campaign = form.save()
            context = {"new_campaign": new_campaign}
            return render(request, 'control_panel_app/create_campaign.html', context)
        else:
            return render(request, 'control_panel_app/create_campaign.html', {'campaign_form': form})
    else:
        form = AdvCampaignForm()
        return render(request, 'control_panel_app/create_campaign.html', {'campaign_form': form})


@login_required()
def detail_campaign_page(request, campaign_id):
    campaign = get_object_or_404(AdvCampaign, id=campaign_id)

    if request.method == "POST":
        form = DetailAdvCampaignForm(request.POST, instance=campaign)

        if form.is_valid():
            new_campaign = form.save()
            context = {"new_campaign": new_campaign}
            return render(request, 'control_panel_app/detail_campaign.html', context)
        else:
            return render(request, 'control_panel_app/detail_campaign.html',
                          {'campaign_form': form, 'campaign_id': campaign_id})
    else:
        form = DetailAdvCampaignForm(instance=campaign)
        tracking_url = form.fields.get('tracking_url')
        if tracking_url:
            tracking_url.initial = campaign.get_tracking_url()  # put text to form textfield
        return render(request, 'control_panel_app/detail_campaign.html',
                      {'campaign_form': form, 'campaign_id': campaign_id})
