from django.contrib import admin
from meedl_core_app.models import Client, Offer, AdvCampaign, AdvPlatform, DirectionAdv, Hit, Conversion, TestTable

admin.site.register(Client)
admin.site.register(AdvPlatform)
admin.site.register(DirectionAdv)
admin.site.register(Hit)
admin.site.register(Conversion)

admin.site.register(TestTable)

class OfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'client',)


class CampaignAdvAdmin(admin.ModelAdmin):
    readonly_fields = ('offer_url',)


admin.site.register(Offer, OfferAdmin)
admin.site.register(AdvCampaign, CampaignAdvAdmin)
