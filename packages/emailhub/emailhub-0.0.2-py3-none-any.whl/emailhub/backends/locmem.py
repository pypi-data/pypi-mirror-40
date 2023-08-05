# -*- coding: utf-8 -*-
"""
EmailHub locmem email backend
"""
from django.core import mail
from django.core.mail.backends.locmem import EmailBackend as LocmemEmailBackend

from emailhub.utils.email import process_outgoing_email


class EmailBackend(LocmemEmailBackend):
    """ LocMem email backend """
    def send_messages(self, messages):
        """Redirect messages to the dummy outbox"""
        msg_count = 0
        for message in messages:  # .message() triggers header validation
            message.message()
            mail.outbox.append(message)
            process_outgoing_email(message)
            msg_count += 1
        return msg_count
