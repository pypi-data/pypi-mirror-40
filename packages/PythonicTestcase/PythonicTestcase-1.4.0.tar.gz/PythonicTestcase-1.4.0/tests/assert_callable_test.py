# -*- coding: UTF-8 -*-
#
# SPDX-License-Identifier: MIT
# Copyright (c) 2011, 2015-2016 Felix Schwarz <felix.schwarz@oss.schwarz.eu>

from __future__ import absolute_import, unicode_literals, print_function

from unittest import TestCase

from pythonic_testcase import assert_equals, assert_callable, assert_raises
from .util import exception_message


class AssertCallableTest(TestCase):
    def test_passes_if_object_is_callable(self):
        assert_callable(lambda: None)
        assert_callable(self.assert_fail)
        assert_callable(list)

    def assert_fail(self, kallable, message=None):
        return assert_raises(AssertionError, lambda: assert_callable(kallable, message=message))

    def test_fails_if_object_is_not_callable(self):
        self.assert_fail(None)
        self.assert_fail('')

    def test_fails_with_sensible_default_error_message(self):
        e = self.assert_fail(None)
        assert_equals("None is not callable", exception_message(e))

    def test_can_specify_additional_custom_message(self):
        e = self.assert_fail('bar', message='Bar')
        expected_error = "%r is not callable: Bar" % ('bar', )
        assert_equals(expected_error, exception_message(e))

