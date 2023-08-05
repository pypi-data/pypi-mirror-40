# -*- coding: utf-8 -*-
"""
EmailHub email backends tests
"""
from django.test import TestCase
from django.core.mail import send_mail, EmailMessage as CreateEmailMessage
from django.contrib.auth import get_user_model

from emailhub.conf import settings as emailhub_settings

User = get_user_model()
SUBJECT, BODY, FROM = (
    'Test email', 'Test body', emailhub_settings.DEFAULT_FROM)

BACKENDS = {
    'smtp': 'emailhub.backends.smtp.EmailBackend',
    'console': 'emailhub.backends.console.EmailBackend',
    'filebased': 'emailhub.backends.filebased.EmailBackend',
    'locmem': 'emailhub.backends.locmem.EmailBackend',
    'dummy': 'emailhub.backends.dummy.EmailBackend',
}


class ConsoleRawEmailBackendsTestCase(TestCase):
    """ EmailHub console email backends tests """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='testuser', email='test@user.com', is_active=True)
        cls.user2 = User.objects.create(
            username='testuser2', email='test2@user.com', is_active=True)
        cls.user3 = User.objects.create(
            username='testuser3', email='test3@user.com', is_active=True)
        cls.user4 = User.objects.create(
            username='testuser4', email='test4@user.com', is_active=True)
        cls.user5 = User.objects.create(
            username='testuser5', email='test5@user.com', is_active=True)

    def test_console_backend(self):
        with self.settings(EMAIL_BACKEND=BACKENDS.get('console')):
            send_mail(SUBJECT, BODY, FROM, [self.user.email])
            self.assertEqual(self.user.emailhub.count(), 1)
            msg = self.user.emailhub.first().message
            self.assertEqual(msg.subject, SUBJECT)
            self.assertEqual(msg.body_text, BODY)
            self.assertEqual(msg.from_email, FROM)

    def test_to_recipients(self):
        with self.settings(EMAIL_BACKEND=BACKENDS.get('console')):
            recipients = [self.user.email, self.user2.email]
            send_mail(SUBJECT, BODY, FROM, recipients)
            self.assertEqual(self.user.emailhub.count(), 1)
            self.assertEqual(self.user2.emailhub.count(), 1)
            msg1 = self.user.emailhub.first().message
            self.assertEqual(msg1.recipients.first().pk, self.user.pk)
            self.assertEqual(msg1.recipients.last().pk, self.user2.pk)

    def test_reply_to(self):
        with self.settings(EMAIL_BACKEND=BACKENDS.get('console')):
            reply_to = ['test@test.com']
            recipients = [self.user.email, self.user2.email]
            CreateEmailMessage(SUBJECT, BODY, FROM, recipients,
                               reply_to=reply_to).send()
            self.assertEqual(self.user.emailhub.count(), 1)
            self.assertEqual(self.user2.emailhub.count(), 1)
            msg1 = self.user.emailhub.first().message
            self.assertEqual(reply_to, msg1.reply_to)
