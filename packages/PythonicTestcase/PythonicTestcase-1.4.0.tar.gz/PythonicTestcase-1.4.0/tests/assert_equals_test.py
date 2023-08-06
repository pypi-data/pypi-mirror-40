# -*- coding: UTF-8 -*-
#
# SPDX-License-Identifier: MIT
# Copyright (c) 2011, 2015 Felix Schwarz <felix.schwarz@oss.schwarz.eu>

from __future__ import absolute_import, unicode_literals, print_function

from unittest import TestCase

from pythonic_testcase import assert_equals, assert_raises
from .util import exception_message


class AssertEqualsTest(TestCase):
    # assert_equals testing relies on assert_raises being correct, however it
    # should not rely on any other helper method so assert_raises and
    # assert_equals can provide the foundation for all other test methods

    def test_passes_if_values_are_equal(self):
        assert_equals(1, 1)

    def test_fails_if_values_are_not_equal(self):
        assert_raises(AssertionError, lambda: assert_equals(1, 2))

    def test_fails_with_sensible_default_error_message(self):
        # using a string here on purpose so we can check that repr is used in
        # exception message
        e = assert_raises(AssertionError, lambda: assert_equals('foo', 'bar'))
        expected_str = '%r != %r' % ('foo', 'bar')
        assert expected_str == exception_message(e), repr(exception_message(e))

    def test_can_specify_additional_custom_message(self):
        e = assert_raises(AssertionError, lambda: assert_equals(1, 2, message='foo'))
        assert "1 != 2: foo" == exception_message(e), repr(exception_message(e))

