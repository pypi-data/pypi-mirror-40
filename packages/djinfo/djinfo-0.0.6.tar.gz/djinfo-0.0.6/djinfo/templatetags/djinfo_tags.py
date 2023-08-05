"""
djinfo templatetgs
"""
from django import template
from django.conf import global_settings, settings

register = template.Library()


@register.filter
def type_name(v):
    """
    Returns the type name of a variable (ex: list, str, dict...)
    """
    return str(type(v).__name__).replace('__proxy__', 'unicode')


@register.filter
def is_list(v):
    """
    Returns True if variable is a list
    """
    return isinstance(v, list)


@register.filter
def is_tuple(v):
    """
    Returns True if variable is a tuple
    """
    return isinstance(v, tuple)


@register.filter
def is_set(v):
    """
    Returns True if variable is a set
    """
    return isinstance(v, set)


@register.filter
def is_boolean(v):
    """
    Returns True if variable is a boolean
    """
    return isinstance(v, bool)


@register.filter
def is_dict(v):
    """
    Returns True if variable is a dictionary
    """
    return isinstance(v, dict)


@register.filter
def is_none(v):
    """
    Returns True if variable is None
    """
    return v is None


@register.filter
def is_link(v):
    """
    Returns True if variable is a string that begins as a valid URL
    """
    try:
        return 'http://' in v or 'https://' in v
    except TypeError:
        return False


@register.filter
def is_core(k):
    """
    Returns True if provided django setting name is part of core django
    """
    return hasattr(global_settings, k)


@register.filter
def is_default(k, v):
    """
    Returns True if provided variable is the default value
    """
    if not hasattr(global_settings, k):
        return False
    elif getattr(global_settings, k) == v:
        return True
    elif not is_core(k) and getattr(settings, k) == v:
        return False
    return False
