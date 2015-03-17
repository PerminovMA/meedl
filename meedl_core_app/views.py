from django.shortcuts import render, HttpResponse, get_object_or_404, Http404
from django.http import HttpResponse, HttpResponseRedirect
from meedl_core_app.models import AdvCampaign, Hit
from django.db.models import F
from meedl_core_app.tools.http_meta_info_parsers import UserAgentParser
from meedl_core_app.tools.tools import get_client_ip


def index(request):
    return HttpResponse("Hello world!")


def tracking_url_onclick(request):
    campaign_id = request.GET.get("cid")
    if campaign_id is None:
        return HttpResponse("Bad request", status=400)
    try:
        campaign_id = int(campaign_id)
    except ValueError:
        return HttpResponse("Bad request", status=400)

    campaign = get_object_or_404(AdvCampaign, id=campaign_id)
    campaign.count_clicks = F('count_clicks') + 1
    campaign.save(update_fields=['count_clicks'])

    target_url = campaign.offer_url
    if not target_url:
        # TODO write to log about situation
        target_url = campaign.offer.offer_url
        if not target_url:
            raise Http404("Failed to find target_url")

    # get data about os, device and browser
    user_device, user_os, user_browser = (None,) * 3
    user_device_is_mobile = False
    user_agent_data = request.META.get('HTTP_USER_AGENT')
    if user_agent_data:
        ua_obj = UserAgentParser(user_agent_data)
        user_device, user_os, user_browser = ua_obj.get_data()
        user_device_is_mobile = ua_obj.is_mobile

    user_ip = get_client_ip(request)

    Hit.objects.create(adv_campaign=campaign, user_device=user_device, user_os=user_os, user_browser=user_browser,
                       is_mobile=user_device_is_mobile, user_ip=user_ip)

    return HttpResponseRedirect(target_url)


def postback_url_onclick(request):
    campaign_id = request.GET.get("cid")
    if campaign_id is None:
        return HttpResponse("Bad request", status=400)
    try:
        campaign_id = int(campaign_id)
    except ValueError:
        return HttpResponse("Bad request", status=400)

    campaign = get_object_or_404(AdvCampaign, id=campaign_id)
    campaign.count_leads = F('count_leads') + 1
    campaign.save(update_fields=['count_leads'])

    return HttpResponse(campaign.name)