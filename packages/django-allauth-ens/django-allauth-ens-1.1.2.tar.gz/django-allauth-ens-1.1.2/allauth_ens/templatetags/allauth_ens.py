import django
from django import template
from django.conf import settings
from django.shortcuts import resolve_url

from allauth.account.adapter import get_adapter

register = template.Library()

if django.VERSION >= (1, 9):
    simple_tag = register.simple_tag
else:
    simple_tag = register.assignment_tag


@simple_tag
def get_home_url():
    home_url = getattr(settings, 'ACCOUNT_HOME_URL', None)
    if home_url is None:
        return None
    return resolve_url(home_url)


@simple_tag
def get_profile_url():
    profile_url = getattr(settings, 'ACCOUNT_DETAILS_URL', None)
    if profile_url is None:
        return None
    return resolve_url(profile_url)


@simple_tag(takes_context=True)
def is_open_for_signup(context):
    request = context['request']
    return get_adapter(request).is_open_for_signup(request)


@simple_tag
def is_clipper_highlighted():
    installed_apps = getattr(settings, 'INSTALLED_APPS', [])
    return ('allauth_ens.providers.clipper' in installed_apps) \
        and getattr(settings, 'ALLAUTH_ENS_HIGHLIGHT_CLIPPER', True)
