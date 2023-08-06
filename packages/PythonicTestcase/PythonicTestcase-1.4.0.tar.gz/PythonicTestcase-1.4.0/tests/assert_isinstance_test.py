# -*- coding: UTF-8 -*-
#
# SPDX-License-Identifier: MIT
# Copyright (c) 2011, 2015 Felix Schwarz <felix.schwarz@oss.schwarz.eu>

from __future__ import absolute_import, unicode_literals, print_function

from unittest import TestCase

from pythonic_testcase import assert_equals, assert_isinstance, assert_raises
from .util import basestring, exception_message


class AssertIsInstanceTest(TestCase):
    def test_passes_if_object_is_instance_of_class(self):
        assert_isinstance({}, dict)
        assert_isinstance('', basestring)

    def assert_fail(self, value, klass, message=None):
        return assert_raises(AssertionError, lambda: assert_isinstance(value, klass, message=message))

    def test_fails_if_object_is_no_instance_of_class(self):
        self.assert_fail(None, list)

    def test_fails_with_sensible_default_error_message(self):
        e = self.assert_fail('bar', list)
        actual_str = "%r (%s)" % ('bar', ''.__class__.__name__)
        assert_equals(actual_str + " is not an instance of list", exception_message(e))

    def test_can_specify_additional_custom_message(self):
        e = self.assert_fail('bar', list, message='Bar')
        actual_str = "%r (%s)" % ('bar', ''.__class__.__name__)
        assert_equals(actual_str + " is not an instance of list: Bar", exception_message(e))

