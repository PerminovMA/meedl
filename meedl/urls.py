from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'meedl_core_app.views.index', name='index'),
    url(r'^control_panel/', include('control_panel_app.urls', namespace='control_panel', app_name='control_panel_app')),

    url(r'^rest_api/', include('meedl_core_app.rest_api.rest_urls', namespace='rest_api', app_name='meedl_core_app')),

    url(r'^admin/', include(admin.site.urls)),
)
