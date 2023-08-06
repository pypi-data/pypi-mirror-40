# -*- coding: UTF-8 -*-
#
# SPDX-License-Identifier: MIT
# Copyright (c) 2011, 2015 Felix Schwarz <felix.schwarz@oss.schwarz.eu>

from __future__ import absolute_import, unicode_literals, print_function

from unittest import TestCase

from pythonic_testcase import assert_equals, assert_not_none, assert_raises
from .util import exception_message


class AssertNotNoneTest(TestCase):
    def test_passes_if_value_is_not_none(self):
        assert_not_none(True)
        assert_not_none(False)
        assert_not_none('')

    def assert_fail(self, value, message=None):
        return assert_raises(AssertionError, lambda: assert_not_none(value, message=message))

    def test_fails_if_value_is_none(self):
        self.assert_fail(None)

    def test_fails_with_sensible_default_error_message(self):
        # using a string here on purpose so we can check that repr is used in
        # exception message
        e = self.assert_fail(None)
        assert_equals("None == None", exception_message(e))

    def test_can_specify_additional_custom_message(self):
        e = self.assert_fail(None, message='Bar')
        assert_equals("None == None: Bar", exception_message(e))

