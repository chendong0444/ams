from django.conf.urls import patterns, url
from tendenci.apps.site_settings.utils import get_setting


urlpath = get_setting('module', 'associations', 'url')
if not urlpath:
    urlpath = "associations"

urlpatterns = patterns('tendenci.apps.associations.views',
    url(r'^%s/add/$' % urlpath, 'add', name="associations.add"),
    # url(r'^%s/delete/$' % urlpath, 'delete', name="associations.delete"),

)
