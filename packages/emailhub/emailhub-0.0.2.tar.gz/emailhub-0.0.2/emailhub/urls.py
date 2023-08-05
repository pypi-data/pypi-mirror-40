# -*- coding: utf-8 -*-
"""
EmailHub core URLs
"""
from django.conf.urls import url

from emailhub.views import (
    InboxListView, EmailMessageDetailView, EmailMessageUpdateView,
    process_message,
)

app_name = 'emailhub'  # pylint: disable=C0103
urlpatterns = [  # pylint: disable=C0103

    # Email messages list view
    url(r'^$', InboxListView.as_view(),
        name='emailmessage_list'),

    # Email messages detail view
    url(r'^(?P<pk>[^/]+)/$', EmailMessageDetailView.as_view(),
        name='emailmessage_detail'),

    # Email messages update view
    url(r'^(?P<pk>[^/]+)/edit/$', EmailMessageUpdateView.as_view(),
        name='emailmessage_update'),

    url(r'^process/(?P<pk>[0-9]+)/(?P<action>\w+)/$', process_message,
        name='emailmessage_process'),

]
