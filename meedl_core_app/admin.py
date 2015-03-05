from django.contrib import admin
from meedl_core_app.models import Client, Offer

admin.site.register(Client)


class OfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'client')

admin.site.register(Offer, OfferAdmin)