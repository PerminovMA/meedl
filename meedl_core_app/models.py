from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse


class Client(models.Model):
    DIRECT_TYPE = 'DIRECT'
    PARTNER_TYPE = 'PARTNER'
    CLIENT_TYPE_CHOICES = (
        (DIRECT_TYPE, 'Direct client'),
        (PARTNER_TYPE, 'partner'),
    )

    manager = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100, unique=True)
    site_url = models.URLField(blank=True, null=True)
    type = models.CharField(max_length=7, choices=CLIENT_TYPE_CHOICES, default=DIRECT_TYPE)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % self.name


class OfferManager(models.Manager):
    """ Forbids use update method
    """
    def update(self, **kwargs):
        return None


class Offer(models.Model):
    USD_TYPE = 'USD'
    RUBLE_TYPE = 'RUB'
    EURO_TYPE = 'EUR'

    CURRENCY_TYPE_CHOICES = (  # learn more about currency codes: https://en.wikipedia.org/wiki/ISO_4217
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

    objects = OfferManager()  # OfferManager forbids use update method, because update didn't dispatch post_save signal

    @staticmethod
    def offer_url_copier(sender, instance, created, **kwargs):
        """ when Offer is updated, copies offer_url from Offer to all related CampaignAdv
        """
        if not created:
            campaign_adv_list = instance.advcampaign_set.all()
            if campaign_adv_list.count() > 0:
                for campaign in campaign_adv_list:
                    if campaign.offer_url != instance.offer_url:
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
    rules = models.TextField(blank=True, null=True, default=None)  # rules are written in JSON format
    offer_url = models.URLField(blank=True, null=True,
                                default=None)  # field copies from the model Offer when CampaignAdv is created
    creation_date = models.DateTimeField(auto_now_add=True)

    def get_tracking_url(self):
        return reverse("control_panel:detail_campaign_url", args=[self.id])

    @staticmethod
    def offer_url_copier(sender, instance, **kwargs):
        """ copies offer_url from Offer to CampaignAdv when CampaignAdv is created
        """
        if instance.offer:
            instance.offer_url = instance.offer.offer_url
        else:
            print "WARNING! str(CampaignAdv.id) without offer"  # will be writing to the log.  # temporarily

    def __unicode__(self):
        return u'%s' % self.name


class Hit(models.Model):
    adv_campaign = models.ForeignKey(AdvCampaign)
    redirect_to_offer = models.ForeignKey(Offer, blank=True, null=True)  # if was redirecting under AdvCampaign.rules
    user_lang = models.CharField(max_length=50, blank=True, null=True)
    user_country = models.CharField(max_length=50, blank=True, null=True)
    user_city = models.CharField(max_length=50, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % self.adv_campaign


pre_save.connect(AdvCampaign.offer_url_copier, sender=AdvCampaign, weak=False,
                 dispatch_uid="copy_offer_url_when_CampaignAdv.save")

post_save.connect(Offer.offer_url_copier, sender=Offer, weak=False,
                  dispatch_uid="copy_offer_url_when_Offer.save")