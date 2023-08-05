# -*- coding: utf-8 -*-
"""
EmailHub management command
"""

from __future__ import unicode_literals

import six

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _

from emailhub.conf import settings as emailhub_settings
from emailhub.utils.email import send_unsent_emails
from emailhub.models import EmailTemplate, EmailMessage

User = get_user_model()


class Command(BaseCommand):
    """
    EmailHub management command
    """
    help = 'EmailHub management command'

    def add_arguments(self, parser):
        parser.add_argument(
            '--send',
            dest='send',
            action='store_true',
            default=False,
            help='Send unsent emails')
        parser.add_argument(
            '--status',
            dest='status',
            action='store_true',
            default=False,
            help='EmailHub system status')
        parser.add_argument(
            '--create-template',
            dest='create_template',
            action='store_true',
            default=False,
            help='Create a new template')
        parser.add_argument(
            '--list-templates',
            dest='list_templates',
            action='store_true',
            default=False,
            help='List templates')
        parser.add_argument(
            '--send-test',
            dest='send_test',
            action='store',
            help='Send test email')

    def handle(self, *args, **opts):

        if opts.get('send'):
            send_unsent_emails()

        elif opts.get('send_test'):
            if '@' in opts.get('send_test'):
                to = opts.get('send_test')
            else:
                to = User.objects.get(pk=int(opts.get('send_test'))).email

            send_mail('Test email', 'This is a test.',
                      emailhub_settings.DEFAULT_FROM, [to], fail_silently=False)

        elif opts.get('status'):
            qs = EmailMessage.objects.all()
            unsent = qs.filter(is_sent=False).count()
            drafts = qs.filter(is_draft=True, is_sent=False).count()
            issent = qs.filter(is_sent=True, is_draft=False).count()
            errors = qs.filter(is_error=True).count()
            self.stdout.write('\n')
            self.stdout.write("\t{}{}".format(_('Unsent').ljust(30), unsent))
            self.stdout.write("\t{}{}".format(_('Drafts').ljust(30), drafts))
            self.stdout.write("\t{}{}".format(_('Is sent').ljust(30), issent))
            self.stdout.write("\t{}{}".format(_('Errors').ljust(30), errors))
            self.stdout.write('\n')

        elif opts.get('create_template'):
            slug = six.input('{}: '.format(_('Slug')))
            for lang in dict(settings.LANGUAGES).keys():
                subject = '{} ({}): '.format(_('Title'), lang.lower())
                et = EmailTemplate(slug=slug, language=lang, subject=subject)
                et.save()
            self.stdout.write('Created template "{}"'.format(slug))
