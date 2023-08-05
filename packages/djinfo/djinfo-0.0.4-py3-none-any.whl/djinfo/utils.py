# -*- coding: utf-8 -*-
"""
djinfo generic utils
"""
from __future__ import unicode_literals

import os
import re
import copy
import logging

from datetime import timedelta
from collections import OrderedDict
from importlib import import_module

import django

from django.conf import settings
from django.http import HttpRequest
from django.test import Client
from django.contrib.auth import (
    SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY, rotate_token,
    user_logged_in,
)

from djinfo.settings import SETTINGS_MASKS, ENV_MASKS, ENV_EXCLUDE

logger = logging.getLogger(__name__)


def is_masked(k, masks):
    """
    Returns True if provided value should be masked for provided key
    """
    masked = False
    for m in masks:
        if re.search(m, k):
            masked = True
    return masked


def is_excluded(k, excludes):
    """
    Returns True if provided value should be excluded for provided key
    """
    excluded = False
    for e in excludes:
        if re.search(e, k):
            excluded = True
    return excluded


def settings_as_dict():
    """
    Returns django settings as a representable dictionary, filtering
    and masking values
    """
    o = {}
    _settings = copy.deepcopy(
        django.conf.settings.__dict__['_wrapped'].__dict__)
    for k, v in _settings.items():
        if is_masked(k, SETTINGS_MASKS):
            o[k] = '*' * 15
        elif not k.startswith('_'):
            if isinstance(v, timedelta):
                o[k] = str(v)
            elif isinstance(v, (set, tuple)):
                o[k] = list(v)
            else:
                o[k] = v
    return OrderedDict(sorted(o.items(), key=lambda t: t[0]))


def env_as_dict():
    """
    Returns the env as a dict, filtering and masking values
    """
    o = {}
    for k, v in os.environ.items():
        if not is_excluded(k, ENV_EXCLUDE):
            if is_masked(k, ENV_MASKS):
                o[k] = '*' * 15
            else:
                o[k] = v
    return OrderedDict(sorted(o.items(), key=lambda t: t[0]))


def get_context():
    """
    Returns djinfo template context as dictionary
    """
    return {
        'settings': settings_as_dict(),
        'environment': env_as_dict(),
        'django': {
            'version': django.__version__,
        }
    }


def login(request, user, backend=None):
    """
    Persist a user id and a backend in the request. This way a user doesn't
    have to reauthenticate on every request. Note that data set during
    the anonymous session is retained when the user logs in.
    """
    session_auth_hash = ''
    if user is None:
        user = request.user
    if hasattr(user, 'get_session_auth_hash'):
        session_auth_hash = user.get_session_auth_hash()

    if SESSION_KEY in request.session:
        if _get_user_session_key(request) != user.pk or (
                session_auth_hash and
                not constant_time_compare(request.session.get(HASH_SESSION_KEY, ''), session_auth_hash)):
            # To avoid reusing another user's session, create a new, empty
            # session if the existing session corresponds to a different
            # authenticated user.
            request.session.flush()
    else:
        request.session.cycle_key()

    try:
        backend = backend or user.backend
    except AttributeError:
        backends = _get_backends(return_tuples=True)
        if len(backends) == 1:
            _, backend = backends[0]
        else:
            raise ValueError(
                'You have multiple authentication backends configured and '
                'therefore must provide the `backend` argument or set the '
                '`backend` attribute on the user.'
            )
    else:
        if not isinstance(backend, str):
            raise TypeError('backend must be a dotted import path string (got %r).' % backend)

    request.session[SESSION_KEY] = user._meta.pk.value_to_string(user)
    request.session[BACKEND_SESSION_KEY] = backend
    request.session[HASH_SESSION_KEY] = session_auth_hash
    if hasattr(request, 'user'):
        request.user = user
    rotate_token(request)
    user_logged_in.send(sender=user.__class__, request=request, user=user)


class DjinfoClient(Client):
    def force_login(self, user, backend=None):
        def get_backend():
            from django.contrib.auth import load_backend
            for backend_path in settings.AUTHENTICATION_BACKENDS:
                backend = load_backend(backend_path)
                if hasattr(backend, 'get_user'):
                    return backend_path
        if backend is None:
            backend = get_backend()
        user.backend = backend
        self._login(user, backend)

    def _login(self, user, backend=None):
        engine = import_module(settings.SESSION_ENGINE)

        # Create a fake request to store login details.
        request = HttpRequest()

        if self.session:
            request.session = self.session
        else:
            request.session = engine.SessionStore()
        login(request, user, backend)

        # Save the session values.
        request.session.save()

        # Set the cookie to represent the session.
        session_cookie = settings.SESSION_COOKIE_NAME
        self.cookies[session_cookie] = request.session.session_key
        cookie_data = {
            'max-age': None,
            'path': '/',
            'domain': settings.SESSION_COOKIE_DOMAIN,
            'secure': settings.SESSION_COOKIE_SECURE or None,
            'expires': None,
        }
        self.cookies[session_cookie].update(cookie_data)

    def login(self, **credentials):
        """
        Set the Factory to appear as if it has successfully logged into a site.
        Return True if login is possible; False if the provided credentials
        are incorrect.
        """
        from django.contrib.auth import authenticate
        user = authenticate(**credentials)
        if user:
            self._login(user)
            return True
        else:
            return False
