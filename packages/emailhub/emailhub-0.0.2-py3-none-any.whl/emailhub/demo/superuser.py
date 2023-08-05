#!/usr/bin/env python
from wsgi import *  # noqa
from django.contrib.auth import get_user_model
try:
    user = get_user_model().objects.get(username='demouser')
except get_user_model().DoesNotExist:
    pass
else:
    user.is_staff = True
    user.is_superuser = True
    user.save()
