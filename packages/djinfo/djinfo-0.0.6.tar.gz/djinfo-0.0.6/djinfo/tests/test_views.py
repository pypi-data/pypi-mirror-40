# -*- coding: utf-8 -*-
"""
djinfo email backends tests
"""

import json

from django.conf import settings
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from djinfo.utils import TEST_CLIENT_CLASS

User = get_user_model()


class DjinfoViewTestCase(TestCase):
    """ djinfo view tests """
    client_class = TEST_CLIENT_CLASS

    @classmethod
    def setUpTestData(cls):
        cls.superuser = User.objects.create(
            username='testsuperuser', email='test@user.com', is_active=True,
            password='temp1234', is_staff=True, is_superuser=True)
        cls.manager = User.objects.create(
            username='testmanager', email='test2@user.com', is_active=True,
            password='temp1234', is_staff=True, is_superuser=False)
        cls.user = User.objects.create(
            username='testuser', email='test3@user.com', is_active=True,
            password='temp1234', is_staff=False, is_superuser=False)

    def test_view_superuser(self):
        self.client.force_login(self.superuser)
        rs = self.client.get(reverse('djinfo:index'))
        self.assertEqual(rs.status_code, 200)

    def test_view_manager(self):
        self.client.force_login(self.manager)
        rs = self.client.get(reverse('djinfo:index'))
        self.assertEqual(rs.status_code, 302)

    def test_view_user(self):
        self.client.force_login(self.user)
        rs = self.client.get(reverse('djinfo:index'))
        self.assertEqual(rs.status_code, 302)

    def test_view_anonymous(self):
        rs = self.client.get(reverse('djinfo:index'))
        self.assertEqual(rs.status_code, 302)
        self.assertTrue(rs.url.endswith('{}?next=/djinfo/'.format(
            settings.LOGIN_URL)))

    def test_json_view_superuser(self):
        self.client.force_login(self.superuser)
        rs = self.client.get(reverse('djinfo:index'), {'json': True})
        try:
            data = json.loads(str(rs.content, encoding='utf8'))
        except TypeError:  # python 2.7
            data = json.loads(str(rs.content))
        except Exception as e:
            data = {}
        self.assertEqual(data.get('settings', {}).get('SITE_ID'), 1)

    def test_json_view_manager(self):
        self.client.force_login(self.manager)
        rs = self.client.get(reverse('djinfo:index'), {'json': True})
        self.assertEqual(rs.status_code, 302)

    def test_json_view_user(self):
        self.client.force_login(self.user)
        rs = self.client.get(reverse('djinfo:index'), {'json': True})
        self.assertEqual(rs.status_code, 302)

    def test_json_view_anonymous(self):
        rs = self.client.get(reverse('djinfo:index'), {'json': True})
        self.assertEqual(rs.status_code, 302)
