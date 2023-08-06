# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: MIT
# Copyright (c) 2012, 2015 Felix Schwarz <felix.schwarz@oss.schwarz.eu>

from __future__ import absolute_import, unicode_literals, print_function

from unittest import TestCase

from pythonic_testcase import assert_equals, assert_smaller, assert_raises
from .util import exception_message


class AssertSmallerTest(TestCase):
    def test_passes_if_value_is_smaller(self):
        assert_smaller(1, 4)
        assert_smaller(-1, 0)

    def assert_fail(self, first, second, message=None):
        return assert_raises(AssertionError, lambda: assert_smaller(first, second, message=message))

    def test_fails_if_value_is_greater_or_equal(self):
        self.assert_fail(4, 1)
        self.assert_fail(1, 1)

    def test_fails_with_sensible_default_error_message(self):
        e = self.assert_fail(2, 1)
        assert_equals("2 >= 1", exception_message(e))

    def test_can_specify_additional_custom_message(self):
        e = self.assert_fail(2, 1, message='Bar')
        assert_equals("2 >= 1: Bar", exception_message(e))

