# -*- coding:utf-8 -*-

import os
from sys import platform
from tendenci.settings import *

PROJECT_NAME = 'kunshanfa'
# dev OS X
if platform == "darwin":
    PROJECT_NAME = 'kunshanfa_dev'

# go one level up
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

ROOT_URLCONF = 'conf.urls'

INSTALLED_APPS += (
    'gunicorn',
)

SITE_ADDONS_PATH = os.path.join(PROJECT_ROOT, 'addons')

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh'

SITE_ID = 1

# -------------------------------------- #
# THEMES
# -------------------------------------- #
TEMPLATES[0]['DIRS'] += (os.path.join(PROJECT_ROOT, "themes"),)
TEMPLATES[0]['OPTIONS']['debug'] = True

THEMES_DIR = os.path.join(PROJECT_ROOT, 'themes')
ORIGINAL_THEMES_DIR = THEMES_DIR


LOCALE_PATHS = (os.path.join(PROJECT_ROOT, 'themes'),)

# -------------------------------------- #
# STATIC MEDIA
# -------------------------------------- #
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'

# Stock static media files and photos from the URL below
# are licensed by Ed Schipul as Creative Commons Attribution
# http://creativecommons.org/licenses/by/3.0/
#
# The full image set is available online at
# http://tendenci.com/photos/set/3/

STOCK_STATIC_URL = '//d15jim10qtjxjw.cloudfront.net/master-90/'

TEMPLATES[0]['OPTIONS']['context_processors'] += (
    'django.core.context_processors.static',
    'tendenci.apps.base.context_processors.newrelic',)

USE_S3_STORAGE = False
# use qiniu cloud storage  # s3 and cloudfront
if USE_S3_STORAGE:
    # ----------------------------------------- #
    # s3 storeage example
    # set this up at https://console.aws.amazon.com/console/home
    # deploy script will ignore and use local if not configured.
    # It's all good.
    # ----------------------------------------- #
    # AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    # AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    # AWS_STORAGE_BUCKET_NAME = 'ams365'
    # AWS_CLOUDFRONT_DOMAIN = 'd1xv83ait126ax.cloudfront.net'     # 'cdn.ams365.cn'
    # AWS_S3_REGION_NAME = 'ap-northeast-1'  # Tokyo
    # AWS_S3_CUSTOM_DOMAIN = AWS_CLOUDFRONT_DOMAIN
    # AWS_S3_OBJECT_PARAMETERS = {
    #     'CacheControl': 'max-age=86400',
    # }
    AWS_LOCATION = PROJECT_NAME
    #
    # USE_S3_STORAGE = all([
    #     AWS_LOCATION,
    #     AWS_ACCESS_KEY_ID,
    #     AWS_SECRET_ACCESS_KEY,
    #     AWS_STORAGE_BUCKET_NAME
    # ])
    #
    #
    # INSTALLED_APPS += (
    #                    'storages',
    #                    's3_folder_storage',
    #                    )
    # # media
    # DEFAULT_S3_PATH = "%s/media" % AWS_LOCATION
    # DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
    # MEDIA_URL = '//%s/%s/' % (AWS_CLOUDFRONT_DOMAIN, DEFAULT_S3_PATH)
    #
    # # static
    # STATIC_S3_PATH = "%s/static" % AWS_LOCATION
    # STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage'
    #
    # # theme
    # S3_ROOT_URL = '//%s' % AWS_CLOUDFRONT_DOMAIN

    ############################    use qiniu replace s3  ###############################
    # http://www.cnblogs.com/wj5633/p/6562624.html

    QINIU_ACCESS_KEY = 'uQAT-yHW39LkMrCG11sUaWx4MyQvrKu7ZBMUR7_1'
    QINIU_SECRET_KEY = os.environ['QINIU_SECRET_KEY']
    QINIU_BUCKET_DOMAIN = 'p5mlwp2oe.bkt.clouddn.com' # 'cdn.ams365.cn'   # 'idv1li2.qiniudns.com'  # 'p5mlwp2oe.bkt.clouddn.com'
    QINIU_BUCKET_NAME = 'ams365'

    DEFAULT_FILE_STORAGE = 'qiniustorage.backends.QiniuMediaStorage'
    STATICFILES_STORAGE = 'qiniustorage.backends.QiniuStaticStorage'

    # media
    MEDIA_URL = "//%s/%s/media/" % (QINIU_BUCKET_DOMAIN, PROJECT_NAME)
    MEDIA_ROOT = '%s/media/' % PROJECT_NAME

    # static
    STATIC_URL = "//%s/%s/static/" % (QINIU_BUCKET_DOMAIN, PROJECT_NAME)
    STATIC_ROOT = '%s/static' % PROJECT_NAME

    # tinymce js url
    LOCAL_STATIC_URL = STATIC_URL
    TINYMCE_JS_URL = LOCAL_STATIC_URL + 'tiny_mce/tinymce.min.js'

    # themes
    THEMES_DIR = "//%s/%s/themes/" % (QINIU_BUCKET_DOMAIN, PROJECT_NAME)
    S3_ROOT_URL = '//%s' % QINIU_BUCKET_DOMAIN


# -------------------------------------- #
# HAYSTACK SEARCH INDEX
# -------------------------------------- #
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(PROJECT_ROOT, 'index.whoosh'),
    }
}


# -------------------------------------- #
# CACHE
# -------------------------------------- #
LOCAL_CACHE_PATH = os.path.join(PROJECT_ROOT, "cache")


# CAMPAIGN MONITOR
CAMPAIGNMONITOR_URL = ''
CAMPAIGNMONITOR_API_KEY = ''
CAMPAIGNMONITOR_API_CLIENT_ID = ''

# ------------------------------------ #
# IMPERSONATION ADDON
# ------------------------------------ #

if os.path.exists(os.path.join(PROJECT_ROOT, 'addons/impersonation/')):
    MIDDLEWARE_CLASSES += (
        'addons.impersonation.middleware.ImpersonationMiddleware',
    )

# local settings for development
try:
    from local_settings import *
except ImportError:
    pass


# -------------------------------------- #
# DEBUG OPTIONS
# -------------------------------------- #
if DEBUG_TOOLBAR_INSTALLED:
    INSTALLED_APPS += ('debug_toolbar',)
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)


# THIS MUST BE AT THE END!
# -------------------------------------- #
# ADDONS
# -------------------------------------- #

DEFAULT_INSTALLED_APPS = INSTALLED_APPS
from tendenci.apps.registry.utils import update_addons
INSTALLED_APPS = update_addons(INSTALLED_APPS, SITE_ADDONS_PATH)


# wechat pay config
WECHATPAY_CONFIG = {

    'wechatpay_appid': 'wx5ffdd61764dc7066',  # 必填,微信分配的公众账号ID

    'wechatpay_key': 'bdc635k2283d4a2ca477339ea8881234',  # 必填,appid 密钥

    'wechatpay_mchid': '1494664902',  # 必填,微信支付分配的商户号

    'wechatpay_appsecret': os.environ['WECHATPAY_APPSECRET']

}
