from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from control_panel_app.forms.create_forms import AdvCampaignForm


@login_required()
def index_page(request):
    context = {}
    return render(request, 'control_panel_app/control_panel_main.html', context)


@login_required()
def campaigns_page(request):
    context = {}
    return render(request, 'control_panel_app/campaigns.html', context)


@login_required()
def create_campaign_page(request):
    if request.method == "POST":
        form = AdvCampaignForm(request.POST)

        if form.is_valid():
            campaign_cost = form.cleaned_data.get("campaign_cost")
            if campaign_cost is None or campaign_cost < 0:
                context = {"invalid_form": True}
            else:
                new_campaign = form.save()
                context = {"new_campaign": new_campaign}
                return render(request, 'control_panel_app/create_campaign.html', context)
        else:
            context = {"invalid_form": True}
    else:
        context = {}

    form = AdvCampaignForm()
    context["campaign_form"] = form
    return render(request, 'control_panel_app/create_campaign.html', context)


    context = {}
    return render(request, 'control_panel_app/create_campaign.html', context)