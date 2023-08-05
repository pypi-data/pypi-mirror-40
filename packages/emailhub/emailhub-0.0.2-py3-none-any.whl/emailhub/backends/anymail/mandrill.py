# -*- coding: utf-8 -*-
"""
EmailHub AnyMail Mandrill backend
"""
from anymail.backends.mandrill import EmailBackend as BaseEmailBackend  # noqa pylint: disable=import-error
from emailhub.utils.email import process_outgoing_email


class EmailBackend(BaseEmailBackend):
    """ EmailHub AnyMail Mandrill backend """
    def _send(self, message):  # noqa pylint: disable=missing-docstring
        process_outgoing_email(message)
        super(EmailBackend, self)._send(message)
