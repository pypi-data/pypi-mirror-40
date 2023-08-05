# -*- coding: utf-8 -*-
"""
EmailHub console email backend
"""
from django.core.mail.backends.console import EmailBackend as ConsoleEmailBackend  # noqa

from emailhub.utils.email import process_outgoing_email


class EmailBackend(ConsoleEmailBackend):
    """ Console email backend """
    def write_message(self, message):
        """ Writes the message and archive it """
        process_outgoing_email(message)
        super(EmailBackend, self).write_message(message)
