# -*- coding: utf-8 -*-
"""
EmailHub AnyMail MailJet backend
"""
from anymail.backends.mailjet import EmailBackend as BaseEmailBackend  # noqa pylint: disable=import-error
from emailhub.utils.email import process_outgoing_email


class EmailBackend(BaseEmailBackend):
    """ AnyMail MailJet backend """
    def _send(self, message):  # noqa pylint: disable=missing-docstring
        process_outgoing_email(message)
        super(EmailBackend, self)._send(message)
