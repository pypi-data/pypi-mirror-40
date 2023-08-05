# -*- coding: utf-8 -*-
"""
EmailHub generic views
"""

from __future__ import unicode_literals

from django.conf import settings
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, Http404, HttpResponseBadRequest
from django.contrib.admin.views.decorators import staff_member_required

from emailhub.models import EmailMessage
from emailhub.conf import settings as emailhub_settings


class InboxListView(ListView):
    """ Inbox list view """
    model = EmailMessage
    template_name = 'emailhub/emailmessage_list.html'
    paginate_by = emailhub_settings.PAGINATE_BY

    def get_user(self):
        """ Returns request user """
        return self.request.user

    def get_queryset(self):
        """ Returns view's queryset """
        user = self.get_user()
        pks = user.emailhub.values_list('message_id', flat=True)
        qs = super(InboxListView, self).get_queryset().filter(pk__in=pks)
        states = ['error', 'sent', 'pending', 'locked']
        if user.is_superuser:
            states.append('draft')
        return qs.filter(state__in=states)


class EmailMessageDetailView(DetailView):
    """ EmailMessage detail view """
    model = EmailMessage
    template_name = 'emailhub/emailmessage_detail.html'


class EmailMessageUpdateView(DetailView):
    """ EmailMessage update view """
    model = EmailMessage
    template_name = 'emailhub/emailmessage_update.html'


@staff_member_required
@require_http_methods(['POST'])
def process_message(request, pk=None, action=None):  # noqa pylint: disable=inconsistent-return-statements
    """ EmailMessage process ajax view """
    if not request.is_ajax():
        return HttpResponseBadRequest()
    else:
        try:
            msg = EmailMessage.objects.get(pk=pk)
        except EmailMessage.DoesNotExist:
            raise Http404

    if action == 'send':
        # To send the message, we just remove the is_draft flag so it will
        # be sent with the next batch
        if settings.DEV:
            msg.send(force=True)  # Print to console right away and mark as sent.
        else:
            msg.send()
        return JsonResponse({
            'success': True,
            'redirect_to': msg.get_absolute_url(),
            'message': _('Sending message')})

    elif action == 'delete':
        msg.delete()
        return JsonResponse({
            'success': True,
            'redirect_to': '',
            'message': _('Message deleted')})
    elif action == 'save':
        msg.body_text = request.POST.get('text_content') or ''
        msg.body_html = request.POST.get('html_content') or ''
        msg.save()
        return JsonResponse({'success': True, 'message': _('Message saved')})
