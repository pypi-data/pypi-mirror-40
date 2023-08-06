# -*- coding: UTF-8 -*-
#
# SPDX-License-Identifier: MIT
# Copyright (c) 2011, 2015 Felix Schwarz <felix.schwarz@oss.schwarz.eu>

from __future__ import absolute_import, unicode_literals, print_function

from unittest import TestCase

from pythonic_testcase import assert_contains, assert_equals, \
    assert_not_contains, assert_raises
from .util import exception_message


class AssertContainsTest(TestCase):
    def test_passes_if_iterable_contains_value(self):
        assert_contains(True, ['foo', True])
        assert_contains(True, ('foo', True))

    def assert_fail(self, value, actual_iterable, message=None):
        return assert_raises(AssertionError, lambda: assert_contains(value, actual_iterable, message=message))

    def test_fails_if_iterable_does_not_contain_value(self):
        self.assert_fail(None, ('foo', True))
        self.assert_fail(None, [])

    def test_fails_with_sensible_default_error_message(self):
        # using a string here on purpose so we can check that repr is used in
        # exception message
        e = self.assert_fail('foo', [])
        assert_equals("%r not in []" % 'foo', exception_message(e))

    def test_can_specify_additional_custom_message(self):
        e = self.assert_fail('foo', [], message='Bar')
        expected_error = "%r not in []: Bar" % ('foo', )
        assert_equals(expected_error, exception_message(e))


class AssertNotContainsTest(TestCase):
    def test_passes_if_iterable_does_not_contain_value(self):
        assert_not_contains(None, ['foo', True])
        assert_not_contains('bar', ('foo', True))

    def assert_fail(self, value, actual_iterable, message=None):
        return assert_raises(AssertionError, lambda: assert_not_contains(value, actual_iterable, message=message))

    def test_if_iterable_contains_value(self):
        self.assert_fail('foo', ('foo', True))

    def test_fails_with_sensible_default_error_message(self):
        # using a string here on purpose so we can check that repr is used in
        # exception message
        e = self.assert_fail('foo', ['foo'])
        expected_error = "%r in [%r]" % ('foo', 'foo')
        assert_equals(expected_error, exception_message(e))

    def test_can_specify_additional_custom_message(self):
        e = self.assert_fail('foo', ['foo'], message='Bar')
        expected_error = "%r in [%r]: Bar" % ('foo', 'foo')
        assert_equals(expected_error, exception_message(e))

