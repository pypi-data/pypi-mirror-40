# -*- coding: UTF-8 -*-
#
# SPDX-License-Identifier: MIT
# Copyright (c) 2012 Felix Schwarz <felix.schwarz@oss.schwarz.eu>

from __future__ import absolute_import, unicode_literals, print_function

from unittest import TestCase

import pythonic_testcase
from pythonic_testcase import assert_true


class ExportedSymbolsTest(TestCase):
    def test_exports_all_assert_methods_for_star_imports(self):
        exported_methods = pythonic_testcase.__all__
        for symbol_name in dir(pythonic_testcase):
            if symbol_name.startswith('assert_'):
                msg = '%r not exported in __all__' % symbol_name
                assert_true(symbol_name in exported_methods, message=msg)

