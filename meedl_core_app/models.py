from django.db import models
from django.contrib.auth.models import User


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

    def __unicode__(self):
        return u'%s' % self.name


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

    def __unicode__(self):
        return u'%s' % self.name


