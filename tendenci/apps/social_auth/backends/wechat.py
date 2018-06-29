"""
WeChat OAuth support.

This contribution adds support for WeChat OAuth service. The Settings
WeChat_APP_ID and WeChat_API_SECRET must be defined with the values
given by WeChat application registration process.

Extended permissions are supported by defining WeChatEXTENDED_PERMISSIONS
setting, it must be a list of values to request.

By default account id and token expiration time are stored in extra_data
field, check OAuthBackend class for details on how to extend it.
"""
import cgi
import urllib
import logging
from uuid import uuid4

from django.conf import settings
import simplejson
from django.contrib.auth import authenticate

from tendenci.apps.social_auth.backends import BaseOAuth, OAuthBackend, USERNAME, USERNAME_MAX_LENGTH

from tendenci.apps.site_settings.models import Setting
from tendenci.apps.site_settings.utils import get_setting

handler = logging.StreamHandler()
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)


logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# Facebook configuration
WECHAT_SERVER = 'api.weixin.qq.com'
WECHAT_AUTHORIZATION_URL = 'https://%s/sms/oauth2/auth' % WECHAT_SERVER
WECHAT_ACCESS_TOKEN_URL = 'https://%s/sns/oauth2/access_token' % WECHAT_SERVER
WECHAT_CHECK_AUTH = 'https://%s/sns/userinfo' % WECHAT_SERVER
EXPIRES_NAME = getattr(settings, 'SOCIAL_AUTH_EXPIRATION', 'expires')


class WeChatBackend(OAuthBackend):
    """WeChat OAuth authentication backend"""
    name = 'wechat'
    # Default extra data to store
    EXTRA_DATA = [('id', 'id'), ('expires', EXPIRES_NAME), ('nickname', 'nickname'), ('openid', 'openid'),
                  ('sex', 'sex'), ('province', 'province'), ('city', 'city'), ('country', 'country'),
                   ('headimgurl', 'headimgurl'), ('privilege', 'privilege'), ('unionid', 'unionid')]

    def get_user_id(self, details, response):
        id = response.get('unionid', '')
        logger.info('get_user_id=%s' % id)
        return id

    def get_user_details(self, response):
        """Return user details from WeChat account"""
        username = response.get('unionid', uuid4().get_hex()[:USERNAME_MAX_LENGTH])
        detail = {USERNAME: username,
                'email': '%s@ams365.cn' % username,
                'fullname': response.get('nickname', ''),
                'first_name': response.get('nickname', ''),
                'last_name': ''}
        logger.info('get_user_details=%s' % detail)
        return detail


class WeChatAuth(BaseOAuth):
    """Facebook OAuth mechanism"""
    AUTH_BACKEND = WeChatBackend

    def __init__(self, request, redirect):
        self.WECHAT_APP_ID = get_setting(scope='module', scope_category='users', name='wechat_login_app_id')
        self.WECHAT_API_SECRET = get_setting(scope='module', scope_category='users', name='wechat_login_app_secret')
        self.code = request.GET.get('code', '')          # 023XXcCh2x6jYI0H7EBh23CvCh2XXcC5
        self.state = request.GET.get('state', '')        # xxxxxx
        super(WeChatAuth, self).__init__(request, redirect)


    def auth_url(self):
        """Returns redirect url"""
        logger.info('auth_url start')
        args = {'app_id': self.WECHAT_APP_ID,
                'secret': self.WECHAT_API_SECRET,
                'code': self.code,
                'grant_type': 'authorization_code'}
        logger.info('auth_url end')

        return WECHAT_ACCESS_TOKEN_URL + '?' + urllib.urlencode(args)

    def auth_complete(self, *args, **kwargs):
        """Returns user, might be logged in"""
        logger.info('auth_complete start')
        if 'code' in self.data:
            url = WECHAT_ACCESS_TOKEN_URL + '?' + \
                  urllib.urlencode({'appid': self.WECHAT_APP_ID,
                                'grant_type': 'authorization_code',
                                'secret': self.WECHAT_API_SECRET,
                                'code': self.data['code']})
            response = simplejson.load(urllib.urlopen(url))
            access_token = response.get('access_token', '')
            openid = response.get('openid', '')
            data = self.user_data(access_token, openid)
            if data is not None:
                if 'errcode' in data:
                    error = self.data.get('errcode') or 'unknown error'
                    raise ValueError('Authentication error: %s' % error)
                data['access_token'] = access_token
                data['id'] = response.get('unionid', '')
                # expires will not be part of response if offline access
                # premission was requested
                data['expires'] = response.get('expires_in', '')
                logger.info('data=%s' % data)

            kwargs.update({'response': data, WeChatBackend.name: True})
            logger.info('code end')
            return authenticate(*args, **kwargs)
        else:
            error = self.data.get('errcode') or 'unknown error'
            logger.info('errcode=%s' % error)
            raise ValueError('Authentication error: %s' % error)

    def user_data(self, access_token, openid):
        """Loads user data from service"""
        params = {'access_token': access_token, 'openid': openid}
        url = WECHAT_CHECK_AUTH + '?' + urllib.urlencode(params)
        try:
            data = simplejson.load(urllib.urlopen(url))
            logger.info('user_data=%s' % data)
            return data
        except ValueError:
            return None

    @classmethod
    def enabled(cls):
        """Return backend enabled status by checking Setting Model"""
        try:
            WECHAT_APP_ID = get_setting(scope='module', scope_category='users', name='wechat_login_app_id')
            WECHAT_API_SECRET = get_setting(scope='module', scope_category='users', name='wechat_login_app_secret')
        except Setting.DoesNotExist:
            return False
        return True

# Backend definition
BACKENDS = {
    'wechat': WeChatAuth,
}
