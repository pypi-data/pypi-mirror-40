# -*- coding: UTF-8 -*-
#
# SPDX-License-Identifier: MIT
# Copyright (c) 2012, 2015 Felix Schwarz <felix.schwarz@oss.schwarz.eu>

from __future__ import absolute_import, unicode_literals, print_function

from unittest import TestCase

from pythonic_testcase import assert_equals, assert_greater, assert_raises
from .util import exception_message


class AssertGreaterTest(TestCase):
    def test_passes_if_value_is_greater(self):
        assert_greater(4, 1)
        assert_greater(0, -1)

    def assert_fail(self, first, second, message=None):
        return assert_raises(AssertionError, lambda: assert_greater(first, second, message=message))

    def test_fails_if_value_is_smaller_or_equal(self):
        self.assert_fail(1, 4)
        self.assert_fail(1, 1)

    def test_fails_with_sensible_default_error_message(self):
        e = self.assert_fail(1, 2)
        assert_equals("1 <= 2", exception_message(e))

    def test_can_specify_additional_custom_message(self):
        e = self.assert_fail(1, 2, message='Bar')
        assert_equals("1 <= 2: Bar", exception_message(e))

