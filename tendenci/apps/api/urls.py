from django.conf.urls import patterns, url, include

urlpatterns = patterns('tendenci.apps.api',
    url(r'^api/rp/$', 'views.api_rp'),
    url(r'^api/dajidianyu/$', 'views.api_dajidianyu'),
    url(r'^api/open-weixin-callbak/$', 'views.api_open_weixin_callbak'),
    url(r'^api/open-weixin-auth/$', 'views.api_open_weixin_auth'),
    # url(r'^api/wechat_login_callback/$', 'views.api_wechat_login_callback'),
    # url(r'^api/wechat_login_refresh_token/$', 'views.api_wechat_login_refresh_token'),
)
