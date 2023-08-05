# -*- coding: utf-8 -*-
"""
EmailHub Django admin configuration
"""

from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from emailhub.conf import settings as emailhub_settings
from emailhub.models import (
    EmailMessage, EmailTemplate, EmailRecipient, EmailSignature)


class EmailRecipientInline(admin.TabularInline):
    """ Inline Recipient """
    model = EmailRecipient
    extra = 0


class EmailMessageAdmin(admin.ModelAdmin):
    """ EmailMessage Admin """
    icon = '<i class="material-icons">mail</i>'
    list_display = (
        'subject', 'date_sent', 'state', 'date_created')
    readonly_fields = ('uuid', 'date_sent', 'state', 'from_email',
                       'date_created', 'date_modified')
    search_fields = ('subject', 'body_text')
    list_filter = ('state', 'send_error_code')
    date_hierarchy = 'date_created'
    fieldsets = (
        (None, {'fields': (
            ('from_email', ),
            'subject', 'body_text', 'body_html'
        )}),
        (_('Meta'), {
            'fields': (
                ('uuid', 'state', 'send_error_code'),
                ('date_created', 'date_modified', 'date_sent', 'send_retries'),
                'send_error_message',
            )
        }),
    )
    inlines = (EmailRecipientInline, )


admin.site.register(EmailMessage, EmailMessageAdmin)

if emailhub_settings.DRAFT_MODE is True:
    TPL_LIST_FILTER = ('language', 'is_auto_send')
    TPL_LIST_DISPLAY = (
        'subject', 'slug', 'language', 'is_active', 'is_auto_send')
    TPL_MAIN_FIELDS = (
        'subject',
        'slug',
        ('email_from', 'is_auto_send'),
        ('signature', 'language'),
    )
else:
    TPL_LIST_FILTER = ('language', )
    TPL_LIST_DISPLAY = (
        'subject', 'slug', 'language', 'is_active')
    TPL_MAIN_FIELDS = (
        'subject',
        'slug',
        'email_from',
        ('signature', 'language'),
    )


class EmailTemplateAdmin(admin.ModelAdmin):
    """ EmailTemplate Admin """
    icon = '<i class="material-icons">mail_outline</i>'
    list_display = TPL_LIST_DISPLAY
    list_filter = TPL_LIST_FILTER
    ordering = ('slug', 'language')
    search_fields = ('slug', 'subject', 'text_content')
    fieldsets = (
        (None, {'fields': TPL_MAIN_FIELDS}),
        (_('Text'), {
            'fields': (
                'text_content',
            )
        }),
        (_('HTML'), {
            'fields': (
                'html_content',
            )
        }),
    )
admin.site.register(EmailTemplate, EmailTemplateAdmin)


class EmailSignatureAdmin(admin.ModelAdmin):
    """EmailSignature Admin"""
    icon = '<i class="material-icons">border_color</i>'
    list_display = ('slug', 'language')
    list_filter = ('language', )
    ordering = ('slug', 'language')
    search_fields = ('slug', 'text_content', 'html_content')
    fieldsets = (
        (None, {'fields': ('slug', 'language')}),
        (_('Text'), {
            'fields': (
                'text_content',
            )
        }),
        (_('HTML'), {
            'fields': (
                'html_content',
            )
        }),
    )
admin.site.register(EmailSignature, EmailSignatureAdmin)
