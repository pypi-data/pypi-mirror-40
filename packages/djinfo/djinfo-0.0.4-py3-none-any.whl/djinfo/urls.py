# -*- coding: utf-8 -*-
"""
djinfo URLs
"""
from django.conf.urls import url
from djinfo.views import djinfo

app_name = 'djinfo'  # pylint: disable=C0103
urlpatterns = [  # pylint: disable=C0103
    url(r'^$', djinfo, name='index'),
]
