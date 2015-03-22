__author__ = 'PerminovMA@live.ru'

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, url
from django.views.generic import TemplateView


urlpatterns = patterns('',
                       url(r'^$', 'control_panel_app.views.views.index_page', name='index_url'),

                       url(r'^login$', 'control_panel_app.views.views_authorization.login_page', name='login_url'),
                       url(r'^logout$', 'control_panel_app.views.views_authorization.logout_view', name='logout_url'),

                       url(r'^clients', TemplateView.as_view(template_name='control_panel_app/pages/clients.html'),
                           name='clients_url'),
                       url(r'^offers', TemplateView.as_view(template_name='control_panel_app/pages/offers.html'),
                           name='offers_url'),
                       url(r'^campaigns', TemplateView.as_view(template_name='control_panel_app/pages/campaigns.html'),
                           name='campaigns_url'),
                       url(r'^create_campaign$', 'control_panel_app.views.views.create_campaign_page',
                           name='create_campaign_url'),
                        url(r'^create_offer$', 'control_panel_app.views.views.create_offer_page',
                           name='create_offer_url'),
                       url(r'^edit_campaign/(?P<campaign_id>\d+)/$', 'control_panel_app.views.views.edit_campaign_page',
                           name='edit_campaign_url'),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)