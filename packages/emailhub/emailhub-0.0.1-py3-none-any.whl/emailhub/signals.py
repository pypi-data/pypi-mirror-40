"""
EmailHub signals dispatchers
"""

from django.dispatch import Signal

on_email_process = Signal(providing_args=["email"])  # pylint: disable=C0103
on_email_out = Signal(providing_args=["email"])  # pylint: disable=C0103
