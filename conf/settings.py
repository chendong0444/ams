import os
from sys import platform

from tendenci.settings import *

PROJECT_NAME = 'KunShanShiDiaoYuXieHui'
# dev OS X
if platform == "darwin":
    PROJECT_NAME = 'KunShanShiDiaoYuXieHui_dev'

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

# use s3 and cloudfront
if USE_S3_STORAGE:
    # ----------------------------------------- #
    # s3 storeage example
    # set this up at https://console.aws.amazon.com/console/home
    # deploy script will ignore and use local if not configured.
    # It's all good.
    # ----------------------------------------- #
    AWS_ACCESS_KEY_ID = 'xxxxxxxxxxxxxxxxxxxxxxx'
    AWS_SECRET_ACCESS_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    AWS_STORAGE_BUCKET_NAME = 'ams365'
    AWS_CLOUDFRONT_DOMAIN = 'd1xv83ait126ax.cloudfront.net'
    AWS_S3_REGION_NAME = 'ap-northeast-1'  # Tokyo
    AWS_S3_CUSTOM_DOMAIN = AWS_CLOUDFRONT_DOMAIN
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_LOCATION = PROJECT_NAME

    USE_S3_STORAGE = all([
        AWS_LOCATION,
        AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY,
        AWS_STORAGE_BUCKET_NAME
    ])


    INSTALLED_APPS += (
                       'storages',
                       's3_folder_storage',
                       )
    # media
    DEFAULT_S3_PATH = "%s/media" % AWS_LOCATION
    DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'

    # static
    STATIC_S3_PATH = "%s/static" % AWS_LOCATION
    STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage'

    # theme
    S3_ROOT_URL = '//%s' % AWS_CLOUDFRONT_DOMAIN
    # ORIGINAL_THEMES_DIR = '//%s/themes' % AWS_CLOUDFRONT_DOMAIN













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
