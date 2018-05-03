# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from tendenci.apps.upload_avatar.views import upload_avatar,crop_avatar

urlpatterns = patterns('tendenci.apps.upload_avatar.views',
    url(r'^uploadavatar_upload/?$', upload_avatar, name="uploadavatar_upload"),
    url(r'^uploadavatar_crop/?$', crop_avatar, name="uploadavatar_crop"),
)