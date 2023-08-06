# -*- coding: UTF-8 -*-
#
# SPDX-License-Identifier: MIT
# Copyright (c) 2011, 2015 Felix Schwarz <felix.schwarz@oss.schwarz.eu>

from __future__ import absolute_import, unicode_literals, print_function

from unittest import TestCase

from pythonic_testcase import assert_equals, assert_falseish, assert_trueish, assert_raises
from .util import exception_message, UPREFIX


class AssertTrueish(TestCase):
    def test_passes_if_value_is_trueish(self):
        assert_trueish(True)
        assert_trueish(1)
        assert_trueish('foo')
        assert_trueish([42])
        assert_trueish(42)

    def assert_fail(self, value, message=None):
        return assert_raises(AssertionError, lambda: assert_trueish(value, message=message))

    def test_fails_if_value_is_not_trueish(self):
        self.assert_fail(False)
        self.assert_fail(0)
        self.assert_fail('')
        self.assert_fail([])

    def test_fails_with_sensible_default_error_message(self):
        # using a string here on purpose so we can check that repr is used in
        # exception message
        e = self.assert_fail(u'')
        assert_equals(UPREFIX+"'' is not trueish", exception_message(e))

    def test_can_specify_additional_custom_message(self):
        e = self.assert_fail(u'', message='Bar')
        assert_equals(UPREFIX+"'' is not trueish: Bar", exception_message(e))



class AssertFalseish(TestCase):
    def test_passes_if_value_is_falseish(self):
        assert_falseish(False)
        assert_falseish(0)
        assert_falseish('')
        assert_falseish([])
        assert_falseish({})

    def assert_fail(self, value, message=None):
        return assert_raises(AssertionError, lambda: assert_falseish(value, message=message))

    def test_fails_if_value_is_not_falseish(self):
        self.assert_fail(True)
        self.assert_fail(1)
        self.assert_fail('foo')
        self.assert_fail([42])
        self.assert_fail(42)

    def test_fails_with_sensible_default_error_message(self):
        # using a string here on purpose so we can check that repr is used in
        # exception message
        e = self.assert_fail(u'foo')
        assert_equals(UPREFIX+"'foo' is not falseish", exception_message(e))

    def test_can_specify_additional_custom_message(self):
        e = self.assert_fail(u'foo', message='Bar')
        assert_equals(UPREFIX+"'foo' is not falseish: Bar", exception_message(e))

