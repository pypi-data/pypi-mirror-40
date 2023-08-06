# -*- coding: UTF-8 -*-
#
# SPDX-License-Identifier: MIT
# Copyright (c) 2011, 2015, 2017 Felix Schwarz <felix.schwarz@oss.schwarz.eu>

from __future__ import absolute_import, unicode_literals, print_function

from unittest import TestCase

from pythonic_testcase import assert_length, assert_raises
from .util import exception_message


class AssertLengthTest(TestCase):
    def test_passes_if_length_matches_actual(self):
        assert_length(0, [])
        assert_length(1, ['foo'])

    def test_can_consume_generator_if_necessary(self):
        def generator():
            for i in (1, 2, 3):
                yield i
        assert_length(3, generator())
        generator_ = generator()
        assert_length(3, generator_)
        assert_length(0, generator_)

    def assert_fail(self, expected, actual, message=None):
        return assert_raises(AssertionError, lambda: assert_length(expected, actual, message=message))

    def test_fails_if_length_does_not_match_equal(self):
        self.assert_fail(2, ['foo'])

    def test_fails_with_sensible_default_error_message(self):
        e = self.assert_fail(2, ['foo'])
        assert "2 != 1" == exception_message(e), repr(exception_message(e))

    def test_can_specify_additional_custom_message(self):
        e = self.assert_fail(2, ['foo'], message='Bar')
        assert "2 != 1: Bar" == exception_message(e), repr(exception_message(e))

