"""
djinfo settings
"""

from django.conf import settings

SENSIBLE = [
    r'.*PASSPHRASE.*',
    r'.*PASSWORD.*',
    r'.*SECRET.*',
]

SETTINGS_MASKS = getattr(settings, 'DJINFO_MASK_SETTINGS', SENSIBLE)
ENV_MASKS = getattr(settings, 'DJINFO_MASK_ENV', SENSIBLE)
ENV_EXCLUDE = getattr(settings, 'DJINFO_EXCLUDE_ENV', [
    # fzf pollutes the environment with all its
    # settings, we don't really need to see that.
    r'^_fzf.*',
])
