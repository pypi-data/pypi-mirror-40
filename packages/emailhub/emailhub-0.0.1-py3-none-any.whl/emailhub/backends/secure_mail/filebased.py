# -*- coding: utf-8 -*-
"""
EmailHub secure_mail filebased backend
"""
from secure_mail.backends import EncryptingFilebasedEmailBackend  # noqa pylint: disable=import-error
from emailhub.utils.email import process_outgoing_email


class EmailBackend(EncryptingFilebasedEmailBackend):
    """ Encrypting filebased backend """
    def send_messages(self, email_messages):  # noqa pylint: disable=missing-docstring
        for message in email_messages:
            process_outgoing_email(message)
        super(EmailBackend, self).send_messages(email_messages)
