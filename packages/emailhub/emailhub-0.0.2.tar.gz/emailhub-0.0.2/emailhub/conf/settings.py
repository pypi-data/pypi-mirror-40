# -*- coding: utf-8 -*-
"""
EmailHub default settings
"""
from django.conf import settings

# # General

# Send also the HTML version (multi-parts)
DRAFT_MODE = getattr(settings, 'EMAILHUB_DRAFT_MODE', True)

# Default pagination count
PAGINATE_BY = getattr(settings, 'EMAILHUB_PAGINATE_BY', 5)

# If set to True, templates rendering will be rendered with the user's language
# if it can be resoved. See `EMAILHUB_USER_LANGUAGE_RESOLVER` to see how
# language is resolved or customize it.
USER_LANGUAGE_DETECTION = getattr(
    settings, 'EMAILHUB_USER_LANGUAGE_DETECTION', True)

# This function is used to guess a user's preferred language according to
# common models patterns, you should provide your own function to resolve
# the language.
USER_LANGUAGE_RESOLVER = getattr(
    settings, 'EMAILHUB_USER_LANGUAGE_RESOLVER',
    'emailhub.utils.i18n.guess_user_language')

# # Sending

# Default email from
DEFAULT_FROM = getattr(settings, 'EMAILHUB_DEFAULT_FROM', 'no-reply@domain.com')

# Sleep N seconds between sending each batches
SEND_BATCH_SLEEP = getattr(settings, 'EMAILHUB_SEND_BATCH_SLEEP', 2)

# Limit the number of Email objects will be sent
SEND_BATCH_SIZE = getattr(settings, 'EMAILHUB_SEND_BATCH_SIZE', 20)

# Maximum send retries
SEND_MAX_RETRIES = getattr(settings, 'EMAILHUB_SEND_MAX_RETRIES', 3)

# Send also the HTML version (multi-parts)
SEND_HTML = getattr(settings, 'EMAILHUB_SEND_HTML', True)

# # Templates

# Template tags specified here will be loaded for all text and html templates
PRELOADED_TEMPLATE_TAGS = getattr(
    settings, 'EMAILHUB_PRELOADED_TEMPLATE_TAGS', ['i18n'])

# Template string used to render text email
TEXT_TEMPLATE = getattr(
    settings, 'EMAILHUB_TEXT_TEMPLATE',
    """{{% load {template_tags} %}}{content}""")

# Template string used to render HTML email
HTML_TEMPLATE = getattr(
    settings, 'EMAILHUB_HTML_TEMPLATE',
    """
{{% load {template_tags} %}}
{{% language lang|default:"en" %}}
<!DOCTYPE html>
<html lang="{{{{ lang }}}}">
  <head><meta charset="utf-8"></head>
  <body>{content}</body>
</html>
{{% endlanguage %}}
""")

# List of key value pairs of regex patterns and replace values
# to use this in template use body_text_censored and body_html_censored
# properties of EmailMessage
CENSOR_PATTERNS = getattr(settings, 'EMAILHUB_CENSOR_PATTERNS', [])
