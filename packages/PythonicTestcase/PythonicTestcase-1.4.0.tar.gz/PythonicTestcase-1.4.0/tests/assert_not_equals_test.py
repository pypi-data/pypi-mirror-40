# -*- coding: UTF-8 -*-
#
# SPDX-License-Identifier: MIT
# Copyright (c) 2011, 2015 Felix Schwarz <felix.schwarz@oss.schwarz.eu>

from __future__ import absolute_import, unicode_literals, print_function

from unittest import TestCase

from pythonic_testcase import assert_equals, assert_not_equals, assert_raises
from .util import exception_message


class AssertNotEqualsTest(TestCase):
    def test_passes_if_values_are_not_equal(self):
        assert_not_equals(True,  False)

    def assert_fail(self, expected, actual, message=None):
        return assert_raises(AssertionError, lambda: assert_not_equals(expected, actual, message=message))

    def test_fails_if_values_are_equal(self):
        self.assert_fail(False, False)
        self.assert_fail(1, 1)

    def test_fails_with_sensible_default_error_message(self):
        # using a string here on purpose so we can check that repr is used in
        # exception message
        e = self.assert_fail('foo', 'foo')
        assert_equals("%r == %r" % ('foo', 'foo'), exception_message(e))

    def test_can_specify_additional_custom_message(self):
        e = self.assert_fail('foo', 'foo', message='Bar')
        assert_equals("%r == %r: Bar" % ('foo', 'foo'), exception_message(e))

