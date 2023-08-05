# -*- coding: utf-8 -*-
"""
EmailHub filebased email backend
"""
from django.core.mail.backends.filebased import EmailBackend as FileBasedEmailBackend  # noqa

from emailhub.utils.email import process_outgoing_email


class EmailBackend(FileBasedEmailBackend):
    """ Filebased email backend """
    def write_message(self, message):
        """ Writes the message and archive it """
        process_outgoing_email(message)
        super(EmailBackend, self).write_message(message)
