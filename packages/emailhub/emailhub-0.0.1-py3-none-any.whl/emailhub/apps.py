# -*- coding: utf-8 -*-
"""
EmailHub Django app definition
"""
from django.apps import AppConfig


class EmailhubConfig(AppConfig):
    """ Emailhub Django app config """
    name = 'emailhub'
    label = 'emailhub'
    verbose_name = 'EmailHub'
    icon = '<i class="material-icons">markunread_mailbox</i>'
