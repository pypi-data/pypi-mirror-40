# -*- coding: utf-8 -*-
"""
djinfo email backends tests
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

# from djinfo import settings as djinfo_settings

User = get_user_model()


class DjinfoViewTestCase(TestCase):
    """ djinfo view tests """

    @classmethod
    def setUpTestData(cls):
        cls.superuser = User.objects.create(
            username='testsuperuser', email='test@user.com', is_active=True,
            is_staff=True, is_superuser=True)
        cls.manager = User.objects.create(
            username='testmanager', email='test2@user.com', is_active=True,
            is_staff=True, is_superuser=False)
        cls.user= User.objects.create(
            username='testuser', email='test3@user.com', is_active=True,
            is_staff=False, is_superuser=False)

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
        self.assertEqual(rs.url, '/admin/login/?next=/djinfo/')
