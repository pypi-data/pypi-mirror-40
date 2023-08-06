# -*- coding: UTF-8 -*-
#
# SPDX-License-Identifier: MIT
# Copyright (c) 2015 Felix Schwarz <felix.schwarz@oss.schwarz.eu>

from __future__ import absolute_import, unicode_literals, print_function

import sys


__all__ = ['basestring', 'exception_message', 'UPREFIX']

UPREFIX = 'u' if (sys.version_info < (3, 0)) else ''

try:
    basestring = basestring
except NameError:
    basestring = str

def exception_message(exception):
    if (exception is None) or (len(exception.args) == 0):
        return None
    return exception.args[0]

