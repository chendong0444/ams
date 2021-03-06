"""Views"""
import logging
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, \
                        HttpResponseServerError
from django.core.urlresolvers import reverse
from django.db import transaction
from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from tendenci.apps.social_auth.backends import get_backend
from tendenci.apps.social_auth.models import UserSocialAuth
from tendenci.apps.social_auth.utils import sanitize_redirect

handler = logging.StreamHandler()
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

DEFAULT_REDIRECT = getattr(settings, 'SOCIAL_AUTH_LOGIN_REDIRECT_URL', '') or \
                   getattr(settings, 'LOGIN_REDIRECT_URL', '')


def auth(request, backend):
    """Start authentication process"""
    complete_url = getattr(settings, 'SOCIAL_AUTH_COMPLETE_URL_NAME',
                           'complete')
    return auth_process(request, backend, complete_url)


@transaction.atomic
def complete(request, backend):
    """Authentication complete view, override this view if transaction
    management doesn't suit your needs."""
    return complete_process(request, backend)


def complete_process(request, backend):
    """Authentication complete process"""
    backend_name = backend
    backend = get_backend(backend, request, request.path)
    if not backend:
        return HttpResponseServerError(_('Incorrect authentication service'))

    try:
        user = backend.auth_complete()
        logger.info('complete_process.user=%s' % user)
        if not isinstance(user, User):

            # wechat login bind in profile page, use wechat redirct's state param deliver username
            username = request.GET.get('state')
            if username:
                logger.info('complete_process.username=%s' % username)
                users = User.objects.filter(username=username)
                if users and len(users) > 0:
                    usa = UserSocialAuth.objects.create(provider=backend_name, uid=user, extra_data='', user_id=users[0].id)
                    usa.save()
                    return HttpResponseRedirect(reverse('profile.index'))

            return HttpResponseRedirect(reverse('accounts.bind_email') + '?openid=%s&provider=%s' % (user, backend_name))
    except ValueError as e:  # some Authentication error ocurred
        user = None
        error_key = getattr(settings, 'SOCIAL_AUTH_ERROR_KEY', None)
        if error_key:  # store error in session
            request.session[error_key] = str(e)

    if user and getattr(user, 'is_active', True):
        login(request, user)
        if getattr(settings, 'SOCIAL_AUTH_SESSION_EXPIRATION', True):
            # Set session expiration date if present and not disabled by
            # setting
            backend_name = backend.AUTH_BACKEND.name
            social_users = user.social_auth.filter(user_id=user.id)
            if social_users and len(social_users) > 0:
                social_user = social_users[0]
                if social_user.expiration_delta():
                    request.session.set_expiry(social_user.expiration_delta())

        url = request.session.pop(REDIRECT_FIELD_NAME, '') or DEFAULT_REDIRECT

        if hasattr(request.user, 'profile'):
            association = request.user.profile.current_association
            if association is None or association.id == 0:
                url = reverse('associations.join')
            else:
                if association.custom_domain:
                    url = 'https://%s' % association.custom_domain
                elif association.subdomain:
                    url = 'https://%s.ams365.cn' % association.subdomain

    else:
        url = getattr(settings, 'LOGIN_ERROR_URL', settings.LOGIN_URL)

    return HttpResponseRedirect(url)


@login_required
def associate(request, backend):
    """Authentication starting process"""
    complete_url = getattr(settings, 'SOCIAL_AUTH_ASSOCIATE_URL_NAME',
                           'associate_complete')
    return auth_process(request, backend, complete_url)


@login_required
def associate_complete(request, backend):
    """Authentication complete process"""
    backend = get_backend(backend, request, request.path)
    if not backend:
        return HttpResponseServerError(_('Incorrect authentication service'))
    backend.auth_complete(user=request.user)
    url = request.session.pop(REDIRECT_FIELD_NAME, '') or DEFAULT_REDIRECT
    return HttpResponseRedirect(url)


@login_required
def disconnect(request, backend):
    """Disconnects given backend from current logged in user."""
    backend = get_backend(backend, request, request.path)
    if not backend:
        return HttpResponseServerError('Incorrect authentication service')
    backend.disconnect(request.user)
    url = request.GET.get(REDIRECT_FIELD_NAME, '')
    if request.method == 'POST':
        url = request.POST.get(REDIRECT_FIELD_NAME, url)
    url = url or DEFAULT_REDIRECT
    return HttpResponseRedirect(url)


def auth_process(request, backend, complete_url_name):
    """Authenticate using social backend"""
    redirect = reverse(complete_url_name, args=(backend,))
    backend = get_backend(backend, request, redirect)
    if not backend:
        return HttpResponseServerError(_('Incorrect authentication service'))
    # Check and sanitize a user-defined GET/POST redirect_to field value.
    redirect = request.GET.get(REDIRECT_FIELD_NAME)
    if request.method == 'POST':
        redirect = request.POST.get(REDIRECT_FIELD_NAME, redirect)
    redirect = sanitize_redirect(request.get_host(), redirect)
    request.session[REDIRECT_FIELD_NAME] = redirect or DEFAULT_REDIRECT
    if backend.uses_redirect:
        return HttpResponseRedirect(backend.auth_url())
    else:
        return HttpResponse(backend.auth_html(),
                            content_type='text/html;charset=UTF-8')


def unbind(request):
    if request.method == 'GET':
        provider = request.GET.get('provider', '')
        openid = request.GET.get('openid', '')
        userid = request.GET.get('userid', '')
        usas = UserSocialAuth.objects.filter(provider=provider, uid=openid, user_id=userid)
        if usas and len(usas) > 0:
            usas[0].delete()
            return HttpResponse('success', content_type='text/plain;charset=UTF-8')

    return HttpResponse('unbind error', content_type='text/plain;charset=UTF-8')



