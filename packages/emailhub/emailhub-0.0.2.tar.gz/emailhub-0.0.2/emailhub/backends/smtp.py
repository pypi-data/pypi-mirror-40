# -*- coding: utf-8 -*-
"""
EmailHub smtp email backend
"""
from django.core.mail.backends.smtp import EmailBackend as SMTPEmailBackend

from emailhub.utils.email import process_outgoing_email


class EmailBackend(SMTPEmailBackend):
    """ SMTP email backend """
    def _send(self, email_message):
        """ Archive the message and call _send on the base SMTP backend """
        process_outgoing_email(email_message)
        super(EmailBackend, self)._send(email_message)
