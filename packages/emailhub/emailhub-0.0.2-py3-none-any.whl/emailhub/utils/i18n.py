# -*- coding: utf-8 -*-
"""
EmailHub models
"""

from __future__ import unicode_literals

from django.conf import settings


def guess_user_language(user):
    """
    EmailHub's default language resolver
    """
    if hasattr(user, 'profile') and hasattr(user.profile, 'language'):
        return user.profile.language
    elif hasattr(user, 'profile') and hasattr(user.profile, 'lang'):
        return user.profile.lang
    elif hasattr(user, 'language'):
        return user.profile.language
    elif hasattr(user, 'lang'):
        return user.lang
    elif hasattr(settings, 'LANGUAGE_CODE'):
        return settings.LANGUAGE_CODE.split('-')[0]
    return 'en'
