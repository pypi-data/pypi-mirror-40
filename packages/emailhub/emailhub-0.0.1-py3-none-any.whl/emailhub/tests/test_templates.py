# -*- coding: utf-8 -*-
"""
EmailHub email backends tests
"""
import re
from django.core import mail
from django.test import TestCase
from django.contrib.auth import get_user_model

from emailhub.conf import settings as emailhub_settings
from emailhub.models import EmailTemplate, EmailSignature
from emailhub.utils.email import (EmailFromTemplate, send_unsent_emails,
                                  SystemEmailFromTemplate)

User = get_user_model()

TEST_EMAIL = {
    'slug': 'test-template',
    'subject': 'Subject here!',
    'is_auto_send': True,
}
REPLY_TO = ['reply@test.com']

class EmailTemplateAutoSendTestCase(TestCase):
    """
    Test that email are send according to configuration rules
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='testuser',
            email='test@user.com',
            is_active=True)

    def test_force_auto_send_off(self):
            TEST_EMAIL['is_auto_send'] = False
            EmailTemplate.objects.create(**TEST_EMAIL)
            msg = EmailFromTemplate('test-template').send_to(
                self.user, force=True)
            self.assertEqual(msg.state, 'pending')
            self.assertEqual(msg.is_draft, False)
            self.assertEqual(msg.is_pending, True)
            self.assertEqual(msg.is_locked, False)
            self.assertEqual(msg.is_error, False)
            self.assertEqual(msg.is_sent, False)
            self.assertEqual(msg.from_template, 'test-template')

    def test_force_auto_send_on(self):
            TEST_EMAIL['is_auto_send'] = True
            EmailTemplate.objects.create(**TEST_EMAIL)
            msg = EmailFromTemplate('test-template').send_to(
                self.user, force=True)
            self.assertEqual(msg.state, 'pending')
            self.assertEqual(msg.is_draft, False)
            self.assertEqual(msg.is_pending, True)
            self.assertEqual(msg.is_locked, False)
            self.assertEqual(msg.is_error, False)
            self.assertEqual(msg.is_sent, False)
            self.assertEqual(msg.from_template, 'test-template')

    def test_auto_send_off(self):
            TEST_EMAIL['is_auto_send'] = False
            EmailTemplate.objects.create(**TEST_EMAIL)
            msg = EmailFromTemplate('test-template').send_to(self.user)
            send_unsent_emails()
            self.assertEqual(msg.state, 'draft')
            self.assertEqual(msg.is_draft, True)
            self.assertEqual(msg.is_pending, False)
            self.assertEqual(msg.is_locked, False)
            self.assertEqual(msg.is_error, False)
            self.assertEqual(msg.is_sent, False)
            self.assertEqual(msg.from_template, 'test-template')

    def test_auto_send_on(self):
            TEST_EMAIL['is_auto_send'] = True
            EmailTemplate.objects.create(**TEST_EMAIL)
            msg = EmailFromTemplate('test-template').send_to(self.user)
            send_unsent_emails()
            self.assertEqual(msg.state, 'pending')
            self.assertEqual(msg.is_draft, False)
            self.assertEqual(msg.is_pending, True)
            self.assertEqual(msg.is_locked, False)
            self.assertEqual(msg.is_error, False)
            self.assertEqual(msg.is_sent, False)
            self.assertEqual(msg.from_template, 'test-template')

    def test_from_email_parameter(self):
        EmailTemplate.objects.create(**TEST_EMAIL)
        msg = EmailFromTemplate('test-template').send_to(
            self.user, from_email='test@test.com')
        self.assertEqual('test@test.com', msg.from_email)

    def test_from_email_default(self):
        EmailTemplate.objects.create(**TEST_EMAIL)
        msg = EmailFromTemplate('test-template').send_to(self.user)
        self.assertEqual(emailhub_settings.DEFAULT_FROM, msg.from_email)

    def test_from_email_template(self):
        template_kwargs = TEST_EMAIL.copy()
        template_kwargs['email_from'] = 'test-template@test.com'
        EmailTemplate.objects.create(**template_kwargs)
        msg = EmailFromTemplate('test-template').send_to(self.user)
        self.assertEqual('test-template@test.com', msg.from_email)


class EmailTemplateContextTestCase(TestCase):
    """
    Test that variables are correctly injected in templates
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='testuser',
            email='test@user.com',
            is_active=True)

    def wrap_text(self, i):
        return emailhub_settings.TEXT_TEMPLATE.format(
            template_tags=' '.join(emailhub_settings.PRELOADED_TEMPLATE_TAGS),
            content=i)

    def wrap_html(self, i):
        return emailhub_settings.HTML_TEMPLATE.format(
            template_tags=' '.join(emailhub_settings.PRELOADED_TEMPLATE_TAGS),
            content=i)

    def test_context_user(self):
        with self.settings(EMAIL_BACKEND='emailhub.backends.smtp.EmailBackend'):
            TEST_EMAIL['text_content'] = "Hello {{ user }}"
            TEST_EMAIL['html_content'] = "Hello <b>{{ user }}</b>"
            EmailTemplate.objects.create(**TEST_EMAIL)
            msg = EmailFromTemplate('test-template').send_to(self.user)

            self.assertEqual(msg.body_text, self.wrap_text('Hello testuser'))
            self.assertEqual(msg.body_html,
                             self.wrap_html('Hello <b>testuser</b>'))

    def test_context_language(self):
        with self.settings(EMAIL_BACKEND='emailhub.backends.smtp.EmailBackend'):
            TEST_EMAIL['text_content'] = "Hello {{ lang }}"
            TEST_EMAIL['html_content'] = "Hello <b>{{ lang}}</b>"
            EmailTemplate.objects.create(**TEST_EMAIL)
            msg = EmailFromTemplate('test-template').send_to(self.user)

            self.assertEqual(msg.body_text, self.wrap_text('Hello en'))
            self.assertEqual(msg.body_html,
                             self.wrap_html('Hello <b>en</b>'))

    def test_context_email(self):
        with self.settings(EMAIL_BACKEND='emailhub.backends.smtp.EmailBackend'):
            TEST_EMAIL['text_content'] = "Hello {{ email.template_slug }}"
            TEST_EMAIL['html_content'] = \
                "Hello <b>{{ email.template_slug }}</b>"
            EmailTemplate.objects.create(**TEST_EMAIL)
            msg = EmailFromTemplate('test-template').send_to(self.user)

            self.assertEqual(msg.body_text,
                             self.wrap_text('Hello test-template'))
            self.assertEqual(msg.body_html,
                             self.wrap_html('Hello <b>test-template</b>'))

    def test_context_extra(self):
        with self.settings(EMAIL_BACKEND='emailhub.backends.smtp.EmailBackend'):
            TEST_EMAIL['text_content'] = "Hello {{ extra }}"
            TEST_EMAIL['html_content'] = "Hello <b>{{ extra }}</b>"
            EmailTemplate.objects.create(**TEST_EMAIL)
            msg = EmailFromTemplate('test-template', extra_context={
                'extra': 'TEST'}).send_to(self.user)

            self.assertEqual(msg.body_text, self.wrap_text('Hello TEST'))
            self.assertEqual(msg.body_html, self.wrap_html('Hello <b>TEST</b>'))

    def test_subject_interpolation(self):
        with self.settings(EMAIL_BACKEND='emailhub.backends.smtp.EmailBackend'):
            TEST_EMAIL['subject'] = "Hello {{ extra }}"
            TEST_EMAIL['text_content'] = "Hello {{ extra }}"
            TEST_EMAIL['html_content'] = "Hello <b>{{ extra }}</b>"
            EmailTemplate.objects.create(**TEST_EMAIL)
            msg = EmailFromTemplate('test-template', extra_context={
                'extra': 'TEST'}).send_to(self.user)
            self.assertEqual(msg.subject, 'Hello TEST')
    
    def test_signature(self):
        with self.settings(EMAIL_BACKEND='emailhub.backends.smtp.EmailBackend'):
            signature_kwargs = {'slug': 'test-signature',
                                'text_content': 'Test',
                                'html_content': '<p>Test</p>'}
            signature = EmailSignature.objects.create(**signature_kwargs)
            template_kwargs = TEST_EMAIL.copy()
            template_kwargs['subject'] = "Hello"
            template_kwargs['text_content'] = "{{ signature_text }}"
            template_kwargs['html_content'] = "{{ signature_html }}"
            template_kwargs['signature'] = signature
            EmailTemplate.objects.create(**template_kwargs)
            msg = EmailFromTemplate('test-template').send_to(self.user)
            self.assertEqual(msg.body_text, self.wrap_text('Test'))
            self.assertEqual(msg.body_html, self.wrap_html('<p>Test</p>'))
    
    def test_signature_interpolation(self):
        with self.settings(EMAIL_BACKEND='emailhub.backends.smtp.EmailBackend'):
            with self.settings(
                    EMAIL_BACKEND='emailhub.backends.smtp.EmailBackend'):
                signature_kwargs = {'slug': 'test-signature',
                                    'text_content': 'Test {{ extra }}',
                                    'html_content': '<p>Test {{ extra }}</p>'}
                signature = EmailSignature.objects.create(**signature_kwargs)
                template_kwargs = TEST_EMAIL.copy()
                template_kwargs['subject'] = "Hello"
                template_kwargs['text_content'] = "{{ signature_text }}"
                template_kwargs['html_content'] = "{{ signature_html }}"
                template_kwargs['signature'] = signature
                EmailTemplate.objects.create(**template_kwargs)
                msg = EmailFromTemplate('test-template', extra_context={
                    'extra': 'TEST'}).send_to(self.user)
                self.assertEqual(msg.body_text, 
                                 self.wrap_text('Test TEST'))
                self.assertEqual(msg.body_html, 
                                 self.wrap_html('<p>Test TEST</p>'))


class EmailCensorshipTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='testuser',
            email='test@user.com',
            is_active=True)

    def wrap_text(self, i):
        return emailhub_settings.TEXT_TEMPLATE.format(
            template_tags=' '.join(emailhub_settings.PRELOADED_TEMPLATE_TAGS),
            content=i)

    def wrap_html(self, i):
        return emailhub_settings.HTML_TEMPLATE.format(
            template_tags=' '.join(emailhub_settings.PRELOADED_TEMPLATE_TAGS),
            content=i)

    def test_censorship(self):
        with self.settings(EMAIL_BACKEND='emailhub.backends.smtp.EmailBackend'):
            censor_regexes_before = emailhub_settings.CENSOR_PATTERNS
            try:
                emailhub_settings.CENSOR_PATTERNS = [
                    ('<censored>', '<kitten>'), ]
                TEST_EMAIL['text_content'] = \
                    "Hello {{ email.template_slug }} <censored>"
                TEST_EMAIL['html_content'] = \
                    "Hello <b>{{ email.template_slug }}</b> <censored>"
                EmailTemplate.objects.create(**TEST_EMAIL)
                msg = EmailFromTemplate('test-template').send_to(self.user)

                self.assertEqual(msg.body_text_censored,
                                 self.wrap_text('Hello test-template <kitten>'))
                self.assertEqual(msg.body_html_censored,
                                 self.wrap_html('Hello <b>test-template</b> '
                                                '<kitten>'))
            finally:
                emailhub_settings.CENSOR_PATTERNS = censor_regexes_before

    def test_censorship_regexes(self):
        with self.settings(EMAIL_BACKEND='emailhub.backends.smtp.EmailBackend'):
            censor_regexes_before = emailhub_settings.CENSOR_PATTERNS
            try:
                emailhub_settings.CENSOR_PATTERNS = [
                    (re.compile('<censored>'), '<kitten>'), ]
                TEST_EMAIL['text_content'] = \
                    "Hello {{ email.template_slug }} <censored>"
                TEST_EMAIL['html_content'] = \
                    "Hello <b>{{ email.template_slug }}</b> <censored>"
                EmailTemplate.objects.create(**TEST_EMAIL)
                msg = EmailFromTemplate('test-template').send_to(self.user)

                self.assertEqual(msg.body_text_censored,
                                 self.wrap_text('Hello test-template <kitten>'))
                self.assertEqual(msg.body_html_censored,
                                 self.wrap_html('Hello <b>test-template</b> '
                                                '<kitten>'))
            finally:
                emailhub_settings.CENSOR_PATTERNS = censor_regexes_before


class EmailTemplateRecipientsTestCase(TestCase):
    """
    Test that email are sent to all recipients
    """
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='testuser',
            email='test@user.com',
            is_active=True)

    def test_reply_to(self):
        TEST_EMAIL['is_auto_send'] = False
        EmailTemplate.objects.create(**TEST_EMAIL)
        msg = EmailFromTemplate('test-template').send_to(
            self.user, force=True, reply_to=REPLY_TO)
        self.assertEqual(REPLY_TO, msg.reply_to)

    def test_reply_to_system(self):
        TEST_EMAIL['is_auto_send'] = False
        EmailTemplate.objects.create(**TEST_EMAIL)
        msg = SystemEmailFromTemplate('test-template').send_to(
            self.user, force=True, reply_to=['reply@test.com'])
        self.assertEqual(REPLY_TO, msg.reply_to)

    def test_reply_to_send(self):
        TEST_EMAIL['is_auto_send'] = False
        EmailTemplate.objects.create(**TEST_EMAIL)
        msg = SystemEmailFromTemplate('test-template').send_to(
            self.user, force=True, reply_to=['reply@test.com'])
        with self.settings(EMAIL_BACKEND='emailhub.backends.locmem.EmailBackend'):
            msg.send(force=True)
            self.assertEqual(REPLY_TO, mail.outbox[0].reply_to)
