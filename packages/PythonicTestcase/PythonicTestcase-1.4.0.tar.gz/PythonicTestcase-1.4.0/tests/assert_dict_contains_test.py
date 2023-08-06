# -*- coding: UTF-8 -*-
#
# SPDX-License-Identifier: MIT
# Copyright (c) 2012, 2015 Felix Schwarz <felix.schwarz@oss.schwarz.eu>

from __future__ import absolute_import, unicode_literals, print_function

from unittest import TestCase

from pythonic_testcase import assert_dict_contains, assert_equals, assert_raises
from .util import exception_message


class AssertDictContainsTest(TestCase):
    def test_passes_if_dict_contains_subdict(self):
        assert_dict_contains({'foo': 42}, {'foo': 42})
        assert_dict_contains({'foo': 42, 'bar': 21}, {'foo': 42, 'bar': 21})
        assert_dict_contains({'foo': 42}, {'foo': 42, 'bar': 21})

    def assert_fail(self, expected_sub_dict, actual_super_dict, message=None):
        return assert_raises(AssertionError, lambda: assert_dict_contains(expected_sub_dict, actual_super_dict, message=message))

    def test_fails_if_dict_does_not_contain_subdict(self):
        # no keys at all in super dict
        self.assert_fail({'foo': 42}, {})

        # key not present
        self.assert_fail({'bar': 21}, {'foo': 42})

        # different value
        self.assert_fail({'foo': 21}, {'foo': 42})

    def test_fails_with_sensible_default_error_message(self):
        e = self.assert_fail({'foo': '42'}, {})
        assert_equals("%r not in {}" % 'foo', exception_message(e))

        e = self.assert_fail({'foo': 21}, {'foo': 42})
        expected_error = "%r=21 != %r=42" % ('foo', 'foo')
        assert_equals(expected_error, exception_message(e))

    def test_can_specify_additional_custom_message(self):
        e = self.assert_fail({'foo': '42'}, {}, message='Bar')
        assert_equals("%r not in {}: Bar" % 'foo', exception_message(e))

        e = self.assert_fail({'foo': 21}, {'foo': 42}, message='Bar')
        expected_error = "%r=21 != %r=42: Bar" % ('foo', 'foo')
        assert_equals(expected_error, exception_message(e))

