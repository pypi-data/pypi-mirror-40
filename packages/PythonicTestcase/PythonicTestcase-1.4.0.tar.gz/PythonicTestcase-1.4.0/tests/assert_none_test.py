# -*- coding: UTF-8 -*-
#
# SPDX-License-Identifier: MIT
# Copyright (c) 2011, 2015 Felix Schwarz <felix.schwarz@oss.schwarz.eu>

from __future__ import absolute_import, unicode_literals, print_function

from unittest import TestCase

from pythonic_testcase import assert_equals, assert_none, assert_raises
from .util import exception_message


class AssertNoneTest(TestCase):
    def test_passes_if_value_is_none(self):
        assert_none(None)

    def assert_fail(self, value, message=None):
        return assert_raises(AssertionError, lambda: assert_none(value, message=message))

    def test_fails_if_value_is_not_none(self):
        self.assert_fail(1)
        self.assert_fail('')
        self.assert_fail([])
        self.assert_fail(dict())

    def test_fails_with_sensible_default_error_message(self):
        # using a string here on purpose so we can check that repr is used in
        # exception message
        e = self.assert_fail('bar')
        assert_equals("None != %r" % 'bar', exception_message(e))

    def test_can_specify_additional_custom_message(self):
        e = self.assert_fail('bar', message='Foo')
        assert_equals("None != %r: Foo" % 'bar', exception_message(e))

