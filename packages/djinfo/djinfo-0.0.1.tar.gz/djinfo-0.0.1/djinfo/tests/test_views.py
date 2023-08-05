# -*- coding: utf-8 -*-
"""
djinfo email backends tests
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

# from djinfo import settings as djinfo_settings

User = get_user_model()


class ConsoleRawEmailBackendsTestCase(TestCase):
    """ djinfo console email backends tests """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='testuser', email='test@user.com', is_active=True,
            is_superuser=True)
        cls.user2 = User.objects.create(
            username='testuser2', email='test2@user.com', is_active=True,
            is_superuser=False)

    def test_tests(self):
        self.assertEqual(True, True)
       #with self.settings(EMAIL_BACKEND=BACKENDS.get('console')):
       #    self.assertEqual(msg.from_email, FROM)
