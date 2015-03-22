from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from control_panel_app.forms.create_forms import AdvCampaignForm, OfferForm
from control_panel_app.forms.detail_forms import DetailAdvCampaignForm
from meedl_core_app.models import AdvCampaign
from django.core.urlresolvers import reverse


@login_required()
def index_page(request):
    context = {}
    return render(request, 'control_panel_app/control_panel_main.html', context)


@login_required()
def create_offer_page(request):
    title_page = "Create offer"
    form_action_url = reverse("control_panel:create_offer_url")

    if request.method == "POST":
        form = OfferForm(request.POST)

        if form.is_valid():
            new_campaign = form.save()
            context = {"created_object": new_campaign, 'title': title_page, 'action_url': form_action_url}
            return render(request, 'control_panel_app/pages/pages_to_create/universal_page_to_create.html', context)
        else:
            return render(request, 'control_panel_app/pages/pages_to_create/universal_page_to_create.html',
                          {'form': form, "title": title_page, 'action_url': form_action_url})
    else:
        form = OfferForm()
        return render(request, 'control_panel_app/pages/pages_to_create/universal_page_to_create.html',
                      {'form': form, 'title': title_page, 'action_url': form_action_url})


@login_required()
def create_campaign_page(request):
    title_page = "Create campaign"
    form_action_url = reverse("control_panel:create_campaign_url")

    if request.method == "POST":
        form = AdvCampaignForm(request.POST)

        if form.is_valid():
            new_campaign = form.save()
            context = {"created_object": new_campaign, 'title': title_page, 'action_url': form_action_url}
            return render(request, 'control_panel_app/pages/pages_to_create/universal_page_to_create.html', context)
        else:
            return render(request, 'control_panel_app/pages/pages_to_create/universal_page_to_create.html',
                          {'form': form, "title": title_page, 'action_url': form_action_url})
    else:
        form = AdvCampaignForm()
        return render(request, 'control_panel_app/pages/pages_to_create/universal_page_to_create.html',
                      {'form': form, 'title': title_page, 'action_url': form_action_url})


@login_required()
def edit_campaign_page(request, campaign_id):
    campaign = get_object_or_404(AdvCampaign, id=campaign_id)

    if request.method == "POST":
        form = DetailAdvCampaignForm(request.POST, instance=campaign)

        if form.is_valid():
            updated_campaign = form.save()
            context = {"campaign_form": form, "campaign": updated_campaign, "is_updated": True}
            return render(request, 'control_panel_app/edit_campaign.html', context)
        else:
            context = {'campaign_form': form, 'campaign': campaign}
            return render(request, 'control_panel_app/edit_campaign.html', context)
    else:
        form = DetailAdvCampaignForm(instance=campaign)

        tracking_url = form.fields.get('tracking_url')
        postback_url = form.fields.get('postback_url')
        if tracking_url and postback_url:
            tracking_url.initial = campaign.get_tracking_url()  # put text to form textfield
            postback_url.initial = campaign.get_postback_url()

        context = {'campaign_form': form, 'campaign': campaign}
        return render(request, 'control_panel_app/edit_campaign.html', context)
