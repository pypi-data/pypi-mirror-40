# -*- coding: utf-8 -*-
"""
djinfo email backends tests
"""

import django

from django.test import TestCase, Client
from django.contrib.auth import get_user_model

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from djinfo.utils import DjinfoClient

User = get_user_model()

if django.VERSION[0] == 1 and django.VERSION[1] <= 8:
    CLIENT_CLASS = DjinfoClient
else:
    CLIENT_CLASS = Client


class DjinfoViewTestCase(TestCase):
    """ djinfo view tests """
    client_class = CLIENT_CLASS

    def _login(self, user):
        self.client.force_login(user)

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
        self._login(self.superuser)
        rs = self.client.get(reverse('djinfo:index'))
        self.assertEqual(rs.status_code, 200)

    def test_view_manager(self):
        self._login(self.manager)
        rs = self.client.get(reverse('djinfo:index'))
        self.assertEqual(rs.status_code, 302)

    def test_view_user(self):
        self._login(self.user)
        rs = self.client.get(reverse('djinfo:index'))
        self.assertEqual(rs.status_code, 302)

    def test_view_anonymous(self):
        rs = self.client.get(reverse('djinfo:index'))
        self.assertEqual(rs.status_code, 302)
        self.assertTrue(rs.url.endswith('/admin/login/?next=/djinfo/'))
