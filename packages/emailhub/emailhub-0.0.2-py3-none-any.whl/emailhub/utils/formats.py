# -*- coding: utf-8 -*-
"""
EmailHub formats utils
"""

from __future__ import unicode_literals

from django.utils.functional import lazy
from django.utils import six


def _format_lazy(format_string, *args, **kwargs):
    """
    Taken from Django 1.11 source code

    Apply str.format() on 'format_string' where format_string, args,
    and/or kwargs might be lazy.
    """
    return format_string.format(*args, **kwargs)
format_lazy = lazy(_format_lazy, six.text_type)


def as_list(v):
    """ Will return a string or a list as list """
    if v is None:
        return []
    if isinstance(v, six.string_types):
        return [v]
    try:
        iter(v)
    except TypeError:
        return [v]
    else:
        return list(v)
