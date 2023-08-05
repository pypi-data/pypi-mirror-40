# -*- coding: utf-8 -*-
"""
EmailHub email utils
"""

from __future__ import unicode_literals

import time
import logging
import importlib

from django.conf import settings
from django.contrib.auth import get_user_model
from django.template import Context, Template
from django.utils import timezone

from emailhub.models import EmailMessage, EmailTemplate
from emailhub.conf import settings as emailhub_settings
from emailhub.signals import on_email_process, on_email_out

log = logging.getLogger('emailhub')
User = get_user_model()

resolve_user_language = getattr(
    importlib.import_module(
        '.'.join(emailhub_settings.USER_LANGUAGE_RESOLVER.split('.')[:-1])),
    emailhub_settings.USER_LANGUAGE_RESOLVER.split('.')[-1:].pop())


def send_unsent_emails():
    """
    Look for pending EmailMessage and send them
    """
    log.debug('Sending unsent emails')
    unsent_emails = EmailMessage.objects.filter(
        state__in=['pending', 'error'],
        send_retries__lte=emailhub_settings.SEND_MAX_RETRIES
    )[:emailhub_settings.SEND_BATCH_SIZE]
    unset_email_ids = [unsent_email.id for unsent_email in unsent_emails]
    EmailMessage.objects.filter(id__in=unset_email_ids).update(state='locked')
    batch = 0
    for msg in unsent_emails:
        batch += 1
        # flood control
        if batch == emailhub_settings.SEND_BATCH_SIZE:
            log.debug('Sleeping for % seconds',
                      emailhub_settings.SEND_BATCH_SLEEP)
            batch = 0
            time.sleep(emailhub_settings.SEND_BATCH_SLEEP)
        msg.send(force=True)


class EmailFromTemplate(object):
    """
    Creates an EmailMessage from template

    Args:
        slug: The template slug used to lookup the template
        extra_context: A context dictionary to inject into the template with
            the bse context
        lang: The template language, is not provided the user language will be
            resolved and if it cannot be resolved, the global language settings
            will be used.
    """
    slug = None
    extra_context = None
    user = None

    def __init__(self, slug, extra_context=None, lang=None):
        self.slug = slug
        self.language = lang
        self.extra_context = extra_context

    def get_template(self):
        """ Returns the template in the right language """
        kw = {'slug': self.slug}
        if hasattr(self, 'user'):
            kw['language'] = self.language
        try:
            tpl = EmailTemplate.objects.get(**kw)
        except EmailTemplate.DoesNotExist:
            tpl = None
        except EmailTemplate.MultipleObjectsReturned:
            log.error('Multiple templates returned for %, using first ' +
                      'object. THIS IS A CONFIGURATION ERROR.', kw)
            tpl = EmailTemplate.objects.filter(**kw).first()
        return tpl

    def _force_i18n(self, i):  # pylint: disable=no-self-use
        """
        fix because we have no request context, so date templatetags cannot
        determine the correct language
        """
        return '{% load i18n %}{% language lang|default:"fr" %}' + \
               i + '{% endlanguage %}'

    def get_context(self, user=None):
        """ Returns the context used to render the email template """
        context = {
            'user': user,
            'email': {
                'template_slug': self.slug,
            },
            # 'base_url': settings.BASE_URL,
            'lang': self.language,
        }
        if self.extra_context:
            context.update(self.extra_context)
        return context

    def render(self, content, context):
        """ Performs the template rendering """
        try:
            return Template(self._force_i18n(content)).render(Context(context))
        except Exception as e:  # pylint: disable=broad-except
            log.exception('Exception while rendering template %s: %s',
                          self.slug, e)
            return ''

    def send_to(self, user, force=False, from_email=None, reply_to=None):
        """
        This method does not actually send any email, it just create the message
        object in the database. A cron process then send message flagged
        is_sent=False at regular interval.

        Args:
            user: User to send email to
            force: Sends email right away without going throught CRON job
            from_email: The sender’s address
            reply_to: A list or tuple of recipient addresses used
                in the “Reply-To” header when sending the email
        """
        msg = None
        if self.language is None:
            self.language = resolve_user_language(user)
        tpl = self.get_template()
        if tpl is None:
            log.critical(
                'COULD NOT CREATE EMAIL: Missing %s email template for %s',
                dict(settings.LANGUAGES).get(self.language), self.slug)
        else:
            send_from = (from_email
                         or tpl.email_from
                         or emailhub_settings.DEFAULT_FROM)
            ctx = self.get_context(user=user)
            signature = tpl.signature
            ctx['signature'] = signature
            if signature is not None:
                ctx.update(
                    {'signature_text': self.render(signature.text_content, ctx),
                     'signature_html': self.render(signature.html_content, ctx),
                    })
            if emailhub_settings.DRAFT_MODE:
                if tpl.is_auto_send:
                    initial_state = 'pending'
                else:
                    initial_state = 'draft'
            else:
                initial_state = 'pending'

            kw = {
                'from_email': send_from,
                'subject': self.render(tpl.subject, ctx),
                'state': initial_state,
                'from_template': self.slug,
            }
            tags = ' '.join(emailhub_settings.PRELOADED_TEMPLATE_TAGS)
            if tpl.text_content:
                kw['body_text'] = emailhub_settings.TEXT_TEMPLATE.format(
                    content=self.render(tpl.text_content, ctx),
                    template_tags=tags)
            if tpl.text_content:
                kw['body_html'] = emailhub_settings.HTML_TEMPLATE.format(
                    content=self.render(tpl.html_content, ctx),
                    template_tags=tags)

            msg = EmailMessage(**kw)
            msg.save()
            msg.lock()
            msg.add_to(user=user)
            msg.add_recipients(reply_to=reply_to)
            msg.unlock()

            # In dev we send email directly without waiting for a cron job
            if settings.DEBUG or force is True:
                msg.send()

        return msg


class SystemEmailFromTemplate(EmailFromTemplate):
    """
    This might be deprecated
    """
    slug = None
    extra_context = None
    user = None

    def __init__(self, slug, extra_context=None):
        self.slug = slug
        self.extra_context = extra_context or {}
        super(SystemEmailFromTemplate, self).__init__(
            slug, extra_context=extra_context)

    def get_template(self):
        """ Returns the template in the right language """
        kw = {'slug': self.slug}
        kw['language'] = self.language
        try:
            tpl = EmailTemplate.objects.get(**kw)
        except EmailTemplate.DoesNotExist:
            tpl = None
        except EmailTemplate.MultipleObjectsReturned:
            msg = 'Multiple templates returned for %s, using first object. ' + \
                  'THIS IS A CONFIGURATION ERROR.'
            log.error(msg, kw)
            tpl = EmailTemplate.objects.filter(**kw).first()
        return tpl

    def send(self, force=True, to_email=None, from_email=None,  # pylint: disable=too-many-arguments
             lang=None, reply_to=None):
        """
        This method does not actually send any email, it just create the message
        object in the database. A cron process then send message flagged
        is_sent=False at regular interval.
        """
        msg = None
        if lang is None:
            lang = settings.LANGUAGE_CODE.split("-")[0]
        self.language = lang
        ctx = self.get_context()
        tpl = self.get_template()
        if not to_email:
            log.debug('No notification email set, not sending any notification')
        elif tpl is None:
            log.critical(
                'COULD NOT CREATE EMAIL: Missing %s email template for %s',
                dict(settings.LANGUAGES).get(self.language), self.slug)
        else:
            send_from = (from_email
                         or tpl.email_from
                         or emailhub_settings.DEFAULT_FROM)
            signature = tpl.signature
            ctx['signature'] = signature
            if signature is not None:
                ctx.update(
                    {'signature_text': self.render(signature.text_content, ctx),
                     'signature_html': self.render(signature.html_content, ctx),
                    })
            if emailhub_settings.DRAFT_MODE:
                if tpl.is_auto_send:
                    initial_state = 'pending'
                else:
                    initial_state = 'draft'
            else:
                initial_state = 'pending'
            kw = {
                'from_email': send_from,
                'subject': self.render(tpl.subject, ctx),
                'state': initial_state,
                'from_template': self.slug,
            }
            tags = ' '.join(emailhub_settings.PRELOADED_TEMPLATE_TAGS)
            if tpl.text_content:
                kw['body_text'] = emailhub_settings.TEXT_TEMPLATE.format(
                    content=self.render(tpl.text_content, ctx),
                    template_tags=tags)
            if tpl.text_content:
                kw['body_html'] = emailhub_settings.HTML_TEMPLATE.format(
                    content=self.render(tpl.html_content, ctx),
                    template_tags=tags)
            msg = EmailMessage(**kw)
            msg.save()
            msg.lock()
            msg.add_recipients(to=to_email, reply_to=reply_to)
            msg.unlock()
            # In dev we send email directly without waiting for a cron job
            if settings.DEBUG or force:
                msg.send()

        return msg


def get_template_choices(lang):
    """ Returns a list of available email tempaltes """
    qs = EmailTemplate.objects.filter(language=lang)
    values_dict = qs.values('slug', 'subject')
    unique_slugs = set()
    unique_choices = []

    for v in values_dict:
        if v['slug'] not in unique_slugs:
            unique_choices.append((v['slug'], v['subject']))
            unique_slugs.add(v['slug'])

    return unique_choices


def process_outgoing_email(message):
    """ Archive outgoing email if needed (used by email backends) """
    if 'X-EmailHub-UUID' not in message.extra_headers.keys():
        on_email_process.send(sender=message.__class__, email=message)
        kw = {
            'from_email': message.from_email,
            'subject': message.subject,
            'body_text': message.body,
            'state': 'sent',
            'date_sent': timezone.now()
        }
        if hasattr(message, 'alternatives') \
                and message.alternatives \
                and message.alternatives[0]:
            kw['body_html'] = message.alternatives[0][0]

        msg = EmailMessage(**kw)
        msg.save()
        msg.add_recipients(
            to=message.to, cc=message.cc, bcc=message.bcc,
            reply_to=message.reply_to)

    on_email_out.send(sender=message.__class__, email=message)
