# -*- coding: utf-8 -*-
"""
EmailHub AnyMail console backend
"""
from anymail.backends.console import EmailBackend as BaseEmailBackend # noqa pylint: disable=import-error
from emailhub.utils.email import process_outgoing_email


class EmailBackend(BaseEmailBackend):
    """ EmailHub AnyMail console backend """
    def send_messages(self, email_messages):  # noqa pylint: disable=missing-docstring
        for message in email_messages:
            process_outgoing_email(message)
        super(EmailBackend, self).send_messages(email_messages)
