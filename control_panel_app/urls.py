__author__ = 'PerminovMA@live.ru'

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r'^$', 'control_panel_app.views.views.index_page', name='index_url'),

                       url(r'^login$', 'control_panel_app.views.views_authorization.login_page', name='login_url'),
                       url(r'^logout$', 'control_panel_app.views.views_authorization.logout_view', name='logout_url'),

                       url(r'^campaigns$', 'control_panel_app.views.views.campaigns_page', name='campaigns_url'),
                       url(r'^create_campaign$', 'control_panel_app.views.views.create_campaign_page',
                           name='create_campaign_url'),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)