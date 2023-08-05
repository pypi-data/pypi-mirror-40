#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
EmailHub rest runner
"""
import os
import sys

# fix sys path so we don't need to setup PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
os.environ['DJANGO_SETTINGS_MODULE'] = 'emailhub.runtests.settings'

import django # pylint: disable=wrong-import-position

if django.VERSION >= (1, 7, 0):
    # starting from 1.7.0 we need to run setup() in order to populate
    # app config
    django.setup()

from django.conf import settings # pylint: disable=wrong-import-position
from django.test.utils import get_runner # pylint: disable=wrong-import-position


def usage():  # pylint: disable=missing-docstring
    return """
    Usage: python runtests.py [app] [-p <pattern>]
    """


def main():  # pylint: disable=missing-docstring
    TestRunner = get_runner(settings)

    # Ugly parameter parsing. We probably want to improve that in future
    # or just use default django test command. This may be problematic,
    # knowing how testing in Django changes from version to version.
    if '-p' in sys.argv:
        try:
            pos = sys.argv.index('-p')
            pattern = sys.argv.pop(pos) and sys.argv.pop(pos)
        except IndexError:
            print(usage())
            sys.exit(1)
    else:
        pattern = None

    test_modules = sys.argv[1:]

    test_runner = TestRunner(verbosity=2, failfast=False, pattern=pattern)

    if len(sys.argv) > 1:
        test_modules = sys.argv[1:]
    elif len(sys.argv) == 1:
        test_modules = []
    else:
        print(usage())
        sys.exit(1)

    if  (1, 6, 0) <= django.VERSION < (1, 9, 0):
        # this is a compat hack because in django>=1.6.0 you must provide
        # module like "emailhub.contrib.plugin" not "plugin"
        from django.db.models import get_app  # pylint: disable=no-name-in-module
        test_modules = [
            # be more strict by adding .tests to not run tests twice
            get_app(module_name).__name__[:-7] + ".tests"
            for module_name
            in test_modules
        ]
    elif django.VERSION >= (1, 9, 0):
        from django.apps import apps  # pylint: disable=no-name-in-module
        test_modules = [
            # be more strict by adding .tests to not run tests twice
            apps.get_app_config(module_name).name + ".tests"
            for module_name
            in test_modules
        ]

    if django.VERSION < (1, 7, 0):
        # starting from 1.7.0 built in django migrations are run
        # for older releases this patch is required to enable testing with
        # migrations
        from south.management.commands import patch_for_test_db_setup  # pylint: disable=import-error
        patch_for_test_db_setup()

    failures = test_runner.run_tests(test_modules or ['emailhub'])
    sys.exit(failures)


if __name__ == '__main__':
    main()
