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

import django

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
