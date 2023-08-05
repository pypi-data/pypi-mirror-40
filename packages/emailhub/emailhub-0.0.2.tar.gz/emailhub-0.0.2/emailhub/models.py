# -*- coding: utf-8 -*-
"""
EmailHub models
"""

from __future__ import unicode_literals

import re
import uuid
import logging

from smtplib import SMTPResponseException

from django.db import models
from django.utils import six, timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.datastructures import MultiValueDict
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage as CreateEmailMessage

try:
    from django.urls import reverse  # noqa Django >= 1.10
except ImportError:
    from django.core.urlresolvers import reverse  # noqa Django <= 1.9

from emailhub.conf import settings as emailhub_settings
from emailhub.constants import TO, CC, BCC, REPLY_TO
from emailhub.utils.html import icon
from emailhub.utils.formats import as_list, format_lazy

log = logging.getLogger('emailhub')
User = settings.AUTH_USER_MODEL


class EmailMessageQueryset(models.QuerySet):
    """ EmailMessage Queryset Manager """

    def with_recipients(self):
        """ Automatically prefetch recipients and users of EmailMessage """
        return self.prefetch_related(models.Prefetch(
            'recipients',
            queryset=EmailRecipient.objects.with_users()))


@python_2_unicode_compatible  # pylint: disable=R0904,R0902
class EmailMessage(models.Model):
    """ Model used to store email messages """
    STATE_CHOICES = (
        ('draft', _('Draft')),
        ('pending', _('Pending')),
        ('locked', _('Locked')),
        ('sent', _('Sent')),
        ('error', _('Error')),
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    subject = models.TextField(_('Subject'))
    body_text = models.TextField(_('Body (text)'))
    body_html = models.TextField(_('Body (HTML)'), blank=True, null=True)
    from_email = models.EmailField(_('From'))
    date_created = models.DateTimeField(_('Date created'), auto_now_add=True)
    date_modified = models.DateTimeField(_('Date modified'), auto_now=True)
    date_sent = models.DateTimeField(_('Date sent'), blank=True, null=True)
    state = models.CharField(_('State'), max_length=20, default='draft')
    send_retries = models.SmallIntegerField(_('Send retries'), default=0)
    send_error_message = models.TextField(_('Send error message'),
                                          blank=True, null=True)
    send_error_code = models.SmallIntegerField(_('Send error code'),
                                               blank=True, null=True)
    from_template = models.CharField(_('From template'), max_length=100,
                                     blank=True, null=True)

    objects = models.Manager.from_queryset(EmailMessageQueryset)()

    @property
    def is_sent(self):
        """ Returns True if is sent, otherwhise False """
        return self.state == 'sent'

    @property
    def is_error(self):
        """ Returns True if is error, otherwhise False """
        return self.state == 'error'

    @property
    def is_draft(self):
        """ Returns True if is draft, otherwhise False """
        return self.state == 'draft'

    @property
    def is_pending(self):
        """ Returns True if is pending, otherwhise False """
        return self.state == 'pending'

    @property
    def is_locked(self):
        """ Returns True if is locked, otherwhise False """
        return self.state == 'locked'

    def _prepare_censor_patterns(self):  # pylint: disable=no-self-use
        """ Returns censor patterns """
        return [(re.compile(pattern), replace)
                for pattern, replace in emailhub_settings.CENSOR_PATTERNS]

    @property
    def body_text_censored(self):
        """ Returns censored body text """
        result = self.body_text
        for regex, sub in self._prepare_censor_patterns():
            result = regex.sub(sub, result)
        return result

    @property
    def body_html_censored(self):
        """ Returns censored body html """
        result = self.body_html
        for regex, sub in self._prepare_censor_patterns():
            result = regex.sub(sub, result)
        return result

    def lock(self):
        """ Lock a message for sending (only from pending state) """
        if self.is_pending:
            self.state = 'locked'
            self.save(update_fields=('state', ))

    def unlock(self):
        """ Unlock a message for sending (only from lock state) """
        if self.is_locked:
            self.state = 'pending'
            self.save(update_fields=('state', ))

    def sent(self):
        """ Mark message as sent """
        self.date_sent = timezone.now()
        self.state = 'sent'
        self.save(update_fields=('date_sent', 'state'))

    def error(self, code=None, message=None):
        """ Used to flag a send error"""
        update_fields = {'state', 'date_sent', 'send_retries'}
        self.state = 'error'
        self.date_sent = None
        self.send_retries += 1
        if message:
            update_fields.add('send_error_message')
            self._update_error_message(message)
        if code:
            update_fields.add('send_error_code')
            self.send_error_code = code
        self.save(update_fields=update_fields)

    @cached_property
    def recipients_context(self):
        """ Return recipients for context """
        result_dict = {
            'users': MultiValueDict(),
            'recipients': MultiValueDict()
        }
        users = result_dict['users']
        recipients = result_dict['recipients']
        for recipient_obj in self.recipients.all():
            recipients.appendlist(recipient_obj.type, recipient_obj.address)
            for user_obj in recipient_obj.users.all():
                users.appendlist(recipient_obj.type, user_obj)
        return result_dict

    @property
    def to(self):
        """ Returns recipients in "to" field """
        return self.recipients_context['recipients'].getlist(TO)

    @property
    def cc(self):
        """ Returns recipients in "cc" field """
        return self.recipients_context['recipients'].getlist(CC)

    @property
    def bcc(self):
        """ Returns recipients in "bcc" field """
        return self.recipients_context['recipients'].getlist(BCC)

    @property
    def reply_to(self):
        """ Returns recipients in "reply-to" field """
        return self.recipients_context['recipients'].getlist(REPLY_TO)

    def email_kwargs(self):
        """ Returns dict with kwargs for EmailMessage object """
        kwargs = {
            'subject': self.subject,
            'body': self.body_text,
            'from_email': self.from_email,
            'to': self.to,
            'cc': self.cc,
            'bcc': self.bcc,
            'headers': {'X-EmailHub-UUID': self.uuid},
            'reply_to': self.reply_to,
        }
        if self.body_html:
            kwargs['alternatives'] = [(self.body_html, 'text/html')]
        return kwargs

    def _add_recipient(self, _type=TO, address=None, user=None,
                       refresh_cache=True):
        """
        Base method for adding recipient to message

        - Message must be present in database
        - Address and/or user must be provided
        - If user is provided then it's linked to created EmailRecipient
        - If user is provided and address not provided user's email is used
        - If address and user are provided then address is used

        :param _type: type of recipient (to, cc, bcc, reply-to)
        :param address: email address to send email to
        :param user: user instance
        :return created EmailRecipient instance
        """
        if not self.pk:
            raise ValueError('Message must be saved to database')
        if not any((address, user)):
            return None

        address = address or user.email

        if not address:
            return None

        recipient_obj = EmailRecipient(
            message=self, type=_type, address=address)
        recipient_obj.save()

        if user:
            recipient_obj.users.add(user)

        if refresh_cache:
            self.refresh_cache()

        return recipient_obj

    def refresh_cache(self):
        """ refreshes the recipients cache """
        # reload prefetched recipients
        if hasattr(self, '_prefetched_objects_cache'):
            qs_obj = self.recipients.get_prefetch_queryset(
                instances=[self],
                queryset=EmailRecipient.objects.with_users())[0]
            self._prefetched_objects_cache['recipients'] = qs_obj

        # recalculate recipients_context attribute
        try:
            delattr(self, 'recipients_context')
            self.recipients_context  # noqa pylint: disable=pointless-statement
        except AttributeError:
            pass

    def add_to(self, address=None, user=None):
        """ Adds `to` recipient to message """
        return self._add_recipient(TO, address=address, user=user)

    def add_cc(self, address=None, user=None):
        """ Adds `cc` recipient to message """
        return self._add_recipient(CC, address=address, user=user)

    def add_bcc(self, address=None, user=None):
        """ Adds `bcc` recipient to message """
        return self._add_recipient(BCC, address=address, user=user)

    def add_reply_to(self, address=None, user=None):
        """ Adds `reply-to` recipient to message """
        return self._add_recipient(REPLY_TO, address=address, user=user)

    def add_recipients(self, to=None, cc=None, bcc=None, reply_to=None):
        """
        Add recipients to email message

        :param to: list of `to` addresses
        :param cc: list of `cc` addresses
        :param bcc: list of `bcc` addresses
        :param reply_to: list of `reply-to` addresses
        """
        if not any((to, cc, bcc, reply_to)):
            return
        um = get_user_model()
        to = as_list(to)
        cc = as_list(cc)
        bcc = as_list(bcc)
        reply_to = as_list(reply_to)
        recipients = to + cc + bcc
        users = MultiValueDict()
        qs = um.objects.filter(email__in=recipients)
        for u in qs:
            users.appendlist(u.email, u)

        for a in to:
            r = self._add_recipient(TO, a, refresh_cache=False)
            if r:
                r.users.add(*users.getlist(a))
        for a in cc:
            r = self._add_recipient(CC, a, refresh_cache=False)
            if r:
                r.users.add(*users.getlist(a))
        for a in bcc:
            r = self._add_recipient(BCC, a, refresh_cache=False)
            if r:
                r.users.add(*users.getlist(a))
        for a in reply_to:
            self._add_recipient(REPLY_TO, a, refresh_cache=False)
        self.refresh_cache()

    def get_color(self):
        """ Get color according to state """
        return ({
            'draft': 'blue',
            'pending': 'yellow',
            'sent': 'green',
            'locked': 'orange',
            'error': 'red',
        }).get(self.state)

    def get_icon(self):
        """ Get icon according to state """
        i = 'drafts' if self.is_draft else 'email'
        _kwargs = {'tooltip': self.get_state_label(),
                   'css_class': '{}-text'.format(self.get_color())}
        return mark_safe(icon(i, **_kwargs))

    def get_absolute_url(self):
        """ Returns detail URL """
        return reverse('emailhub:emailmessage_detail', args=[self.pk])

    def get_update_url(self):
        """ Returns update URL """
        return reverse('emailhub:emailmessage_update', args=[self.pk])

    def get_admin_url(self):
        """ Returns admin URL """
        return reverse('admin:emailhub_emailmessage_change', args=[self.pk])

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """ Saves the message """
        # force remove new lines & spaces from begining and end of the message
        self.body_text = re.sub(r'^(\n|\r|\s)+|(\n|\r|\s)+$', '',
                                self.body_text)
        return super(EmailMessage, self).save(force_insert=force_insert,
                                              force_update=force_update,
                                              using=using,
                                              update_fields=update_fields)

    def _update_error_message(self, new_error_message):
        """
        Extends existing error message with new one. This way we don't lose
        information about sending errors in database.

        :param new_error_message: New error message to append
        :return: None. Changes are not saved to database.
        """
        if self.send_error_message:
            self.send_error_message = '{}\n{}'.format(
                self.send_error_message, six.text_type(new_error_message))
        else:
            self.send_error_message = new_error_message

    def send(self, force=False):
        """
        Sends a given EmailMessage object
        """
        if force is False:
            self.state = 'pending'
            self.save(update_fields=('state', ))
        elif force is True and self.state in ['draft', 'pending', 'error']:
            kwargs = self.email_kwargs()

            if 'alternatives' in kwargs:
                email = EmailMultiAlternatives(**kwargs)
            else:
                email = CreateEmailMessage(**kwargs)

            max_retries = emailhub_settings.SEND_MAX_RETRIES
            if self.send_retries > max_retries:
                self.error(
                    message='Max retries reached ({})'.format(max_retries))
                log.debug('Not seding email (max retry of % reached)',
                          emailhub_settings.SEND_MAX_RETRIES)
            else:
                try:
                    email.send()
                    self.sent()
                    log.debug('EMAIL SENT > "%s" to %s',
                              six.text_type(self.subject), self.to)
                except SMTPResponseException as e:
                    self.error(code=e.smtp_code, message=e.smtp_error)
                    log.debug('EMAIL SMTP ERROR > "%s" to %s (%s)',
                              six.text_type(self.subject), self.to, self)
                    log.error(e, exc_info=True)
                except Exception as e:  # pylint: disable=broad-except
                    self.error(message=six.text_type(e))
                    log.debug('EMAIL ERROR > "%s" to %s (%s)',
                              six.text_type(self.subject), self.to, self)
                    log.error(e, exc_info=True)

    def __str__(self):  # pylint: disable=C0111
        return six.text_type(
            '<{to}> {subject}'.format(to=','.join(self.to),
                                      subject=self.subject))

    class Meta:  # pylint: disable=C0111,C1001,C0321,no-init
        verbose_name = _('Email message')
        verbose_name_plural = _('Email messages')
        ordering = ['-date_created', '-date_sent']


# @python_2_unicode_compatible
# class EmailMessageBody(models.Model):
#     """ Model used to store email messages bodies """
#     message = models.ForeignKey(
#         EmailMessage, related_name='bodies', on_delete=models.CASCADE)
#     body_text = models.TextField(_('Text'))
#     body_html = models.TextField(_('HTML'), blank=True, null=True)
#
#     class Meta:  # pylint: disable=C0111,C1001,C0321,no-init
#         verbose_name = _('Email message body')
#         verbose_name_plural = _('Email message bodies')


class EmailRecipientQueryset(models.QuerySet):
    """ EmailRecipient Queryset Manager """

    def with_users(self):
        """ Automatically prefetch users linked to recipient """
        return self.prefetch_related('users')


@python_2_unicode_compatible
class EmailRecipient(models.Model):
    """ Model used to store email recipients """

    TYPE_CHOICES = (
        (TO, _('To')),
        (CC, _('C.C.')),
        (BCC, _('B.C.C.')),
        (REPLY_TO, _('Reply-To')),
    )

    message = models.ForeignKey(
        EmailMessage, related_name='recipients', on_delete=models.CASCADE)
    type = models.CharField(
        _('Recipient type'), max_length=10, default=TO, choices=TYPE_CHOICES)
    address = models.EmailField(_('Recipient email address'))

    users = models.ManyToManyField(
        User, related_name='emailhub', blank=True)

    objects = models.Manager.from_queryset(EmailRecipientQueryset)()

    def __str__(self):  # pylint: disable=C0111
        return six.text_type(
            '{type}: {address}'.format(type=self.get_type_display(),
                                       address=self.address))

    class Meta:  # pylint: disable=C0111,C1001,C0321,no-init
        verbose_name = _('Email recipient')
        verbose_name_plural = _('Email recipients')


@python_2_unicode_compatible
class EmailSignature(models.Model):
    """ Model used to store email signatures """
    slug = models.SlugField(_('Slug'), max_length=80, blank=False, null=False,
                            unique=False)
    language = models.CharField(_('Language'), max_length=6, default='en',
                                choices=settings.LANGUAGES)
    text_content = models.TextField(_('Text content'))
    html_content = models.TextField(_('HTML content'), blank=True, null=True)

    def __str__(self):  # pylint: disable=C0111
        return six.text_type(
            '{slug} ({lang})'.format(slug=self.slug, lang=self.language))

    class Meta:  # pylint: disable=C0111,C1001,C0321,no-init
        verbose_name = _('Email signature')
        verbose_name_plural = _('Email signatures')
        ordering = ['slug']


@python_2_unicode_compatible
class EmailTemplate(models.Model):
    """ Model used to store email templates """
    SIGNATURE_CHOICES = (
        ('none', _('No signature')),
        ('default', _('Default')),
    )
    language = models.CharField(_('Language'), max_length=6, default='en',
                                choices=settings.LANGUAGES)
    slug = models.SlugField(_('Slug'), max_length=80, blank=False, null=False,
                            unique=False)
    subject = models.TextField(_('Subject'))
    text_content = models.TextField(_('Text content'))
    html_content = models.TextField(_('HTML content'))
    email_from = models.EmailField(
        _('Email from'), blank=True, null=True,
        help_text=format_lazy(_('Will be sent from "{}" if left blank.'),
                              emailhub_settings.DEFAULT_FROM))
    is_active = models.BooleanField(_('Is active'), default=True)
    is_auto_send = models.BooleanField(
        _('Auto send'), default=False,
        help_text=_('If checked, email will be sent ' +
                    'without going through a "draft" state.'))
    signature = models.ForeignKey(
        EmailSignature, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):  # pylint: disable=C0111
        return six.text_type('{} ({})'.format(self.subject, self.language))

    class Meta:  # pylint: disable=C0111,C1001,C0321,no-init
        verbose_name = _('Email template')
        verbose_name_plural = _('Email templates')
