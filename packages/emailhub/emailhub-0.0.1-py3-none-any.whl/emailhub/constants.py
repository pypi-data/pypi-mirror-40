# -*- coding: utf-8 -*-
"""
EmailHub constants
"""
import os

TO = 'to'
CC = 'cc'
BCC = 'bcc'
REPLY_TO = 'reply-to'

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACKAGE_NAME = 'emailhub'
PACKAGE_PATH = os.path.join(ROOT_PATH, PACKAGE_NAME)
