from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from .views import StyleguideView

urlpatterns = [
    url(_(r'^$'), StyleguideView.as_view(), name='styleguide'),
    url(_(r'^mockups/(?P<template>.*)/$'), StyleguideView.as_view(), name='styleguide'),
]
