# -*- coding: utf-8 -*-
"""
djinfo email backends tests
"""

import json

from django.test import TestCase, Client
from django.contrib.auth import get_user_model

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from djinfo.utils import TEST_CLIENT_CLASS, MASK

User = get_user_model()


class DjinfoSettingsTestCase(TestCase):
    """ djinfo settings tests """
    client_class = TEST_CLIENT_CLASS

    @classmethod
    def setUpTestData(cls):
        cls.superuser = User.objects.create(
            username='testsuperuser', email='test@user.com', is_active=True,
            password='temp1234', is_staff=True, is_superuser=True)

    def test_default_masks(self):
        self.client.force_login(self.superuser)
        rs = self.client.get(reverse('djinfo:index'), {'json': True})
        try:
            data = json.loads(str(rs.content, encoding='utf8'))
        except TypeError:  # python 2.7
            data = json.loads(str(rs.content))
        except Exception as e:
            data = {}
        self.assertEqual(
            data.get('settings', {}).get('SECRET_KEY'), MASK)
