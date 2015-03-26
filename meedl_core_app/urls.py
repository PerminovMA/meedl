__author__ = 'PerminovMA@live.ru'

from django.conf.urls import patterns, url


urlpatterns = patterns('',
                       url(r'^click', 'meedl_core_app.views.tracking_url_onclick', name='tracking_url_onclick_url'),
                       url(r'^postback', 'meedl_core_app.views.postback_url_handler', name='postback_url'),
                       )