from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse
from urllib import urlencode
from django.db.models.query import QuerySet
from meedl_core_app.tools.cpa_networks import CPA_NETWORKS, get_cpa_network_out_of_label


class Client(models.Model):
    DIRECT_TYPE = 'DIRECT'
    PARTNER_TYPE = 'PARTNER'
    CLIENT_TYPE_CHOICES = (
        (DIRECT_TYPE, 'Direct client'),
        (PARTNER_TYPE, 'partner'),
    )

    CPA_NETWORK_CHOICES = ((cpa.LABEL, cpa.NAME) for cpa in CPA_NETWORKS)

    manager = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100, unique=True)
    site_url = models.URLField(blank=True, null=True)
    type = models.CharField(max_length=7, choices=CLIENT_TYPE_CHOICES, default=DIRECT_TYPE)
    creation_date = models.DateTimeField(auto_now_add=True)

    # if CPA network not used then = Null
    cpa_network_label = models.CharField(max_length=20, choices=CPA_NETWORK_CHOICES, null=True, blank=True)

    @property
    def cpa_network(self):
        return get_cpa_network_out_of_label(self.cpa_network_label)

    def __unicode__(self):
        return u'%s' % self.name


class OfferManager(models.Manager):
    """ Forbids use update method
    """

    def get_queryset(self):
        return self.model.QuerySet(self.model)


class Offer(models.Model):
    USD_TYPE = 'USD'  # learn more about currency codes: https://en.wikipedia.org/wiki/ISO_4217
    RUBLE_TYPE = 'RUB'
    EURO_TYPE = 'EUR'

    CURRENCY_TYPE_CHOICES = (
        (USD_TYPE, 'United States dollar'),
        (RUBLE_TYPE, 'Russian ruble'),
        (EURO_TYPE, 'Euro'),
    )

    client = models.ForeignKey(Client)
    manager = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100)
    offer_url = models.URLField()
    revenue_per_lead = models.FloatField()
    currency_type = models.CharField(max_length=3, choices=CURRENCY_TYPE_CHOICES)  # currency of payment
    limit_number_leads = models.PositiveIntegerField(null=True, blank=True)  # limit leads per day
    is_active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    use_sub_id = models.BooleanField(default=False)

    objects = OfferManager()  # OfferManager forbids use update method, because update didn't dispatch post_save signal

    class QuerySet(QuerySet):
        def update(self, **kwargs):
            return None

    @staticmethod
    def offer_url_copier(sender, instance, created, **kwargs):
        """ when Offer is updated, copies offer_url from Offer to all related CampaignAdv
        """
        if not created:
            campaign_adv_list = instance.advcampaign_set.all()
            if campaign_adv_list.count() > 0:
                for campaign in campaign_adv_list:
                    if campaign.offer_url != instance.offer_url or instance.use_sub_id:
                        campaign.save()

    def __unicode__(self):
        return u'%s' % self.name


class AdvPlatform(models.Model):
    name = models.CharField(max_length=100, unique=True)
    site_url = models.URLField(blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.name


class DirectionAdv(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return u'%s' % self.name


class AdvCampaign(models.Model):
    name = models.CharField(max_length=100)
    adv_platform = models.ForeignKey(AdvPlatform)
    direction = models.ForeignKey(DirectionAdv)
    campaign_cost = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)
    offer = models.ForeignKey(Offer)
    count_clicks = models.PositiveIntegerField(default=0)
    count_leads = models.PositiveIntegerField(default=0)
    rules = models.TextField(blank=True, null=True, default=None)  # rules are written in JSON format
    offer_url = models.URLField(blank=True, null=True,
                                default=None)  # field copies from the model Offer when CampaignAdv is created
    creation_date = models.DateTimeField(auto_now_add=True)

    def get_tracking_url(self):
        params = {"cid": self.id}
        return reverse("meedl_core:tracking_url_onclick_url") + "?%s" % urlencode(params)  # , args=[self.id])


    @staticmethod
    def offer_url_copier(sender, instance, created, **kwargs):
        """ copies offer_url from Offer to CampaignAdv when CampaignAdv is created
        """
        if created:
            if instance.offer:
                if instance.offer.use_sub_id:
                    cpa_network = instance.offer.client.cpa_network
                    if cpa_network and not cpa_network.sub_id_is_added(instance.offer.offer_url):
                        offer_url = cpa_network.add_sub_id(instance.offer.offer_url, instance.id)
                        # for avoid recursion use update (update didn't dispatch post_save signal).
                        AdvCampaign.objects.filter(id=instance.id).update(offer_url=offer_url)
                        return
                offer_url = instance.offer.offer_url
                AdvCampaign.objects.filter(id=instance.id).update(offer_url=offer_url)
            else:
                print "WARNING! str(CampaignAdv.id) without offer"
                # TODO will be writing to the log

    def __unicode__(self):
        return u'%s' % self.name


class Hit(models.Model):
    adv_campaign = models.ForeignKey(AdvCampaign)
    redirect_to_offer = models.ForeignKey(Offer, blank=True, null=True)  # if was redirecting under AdvCampaign.rules
    user_lang = models.CharField(max_length=50, blank=True, null=True)
    user_country = models.CharField(max_length=50, blank=True, null=True)
    user_city = models.CharField(max_length=50, blank=True, null=True)
    user_device = models.CharField(max_length=50, blank=True, null=True)
    user_os = models.CharField(max_length=50, blank=True, null=True)
    user_browser = models.CharField(max_length=50, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    is_mobile = models.BooleanField(default=False)
    user_ip = models.GenericIPAddressField(blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.adv_campaign


class Conversion(models.Model):
    adv_campaign = models.ForeignKey(AdvCampaign, null=True, blank=True)  # it's sub_id
    payout = models.FloatField(null=True, blank=True)  # the amount of payment
    payout_currency = models.CharField(max_length=30, null=True, blank=True)
    conversion_time = models.DateTimeField(null=True, blank=True)
    user_ip = models.GenericIPAddressField(blank=True, null=True)
    user_country = models.CharField(max_length=50, blank=True, null=True)
    user_city = models.CharField(max_length=50, blank=True, null=True)
    user_browser = models.CharField(max_length=30, blank=True, null=True)
    user_os = models.CharField(max_length=30, blank=True, null=True)
    user_device = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(max_length=30, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    offer_id = models.CharField(max_length=30, blank=True, null=True)
    offer_name = models.CharField(max_length=30, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % str(self.conversion_time)


post_save.connect(AdvCampaign.offer_url_copier, sender=AdvCampaign, weak=False,
                  dispatch_uid="copy_offer_url_when_CampaignAdv.save")

post_save.connect(Offer.offer_url_copier, sender=Offer, weak=False,
                  dispatch_uid="copy_offer_url_when_Offer.save")


class TestTable(models.Model):
    some_text = models.CharField(max_length=250, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % str(self.some_text)