# -*- coding: UTF-8 -*-
#
# SPDX-License-Identifier: MIT
# Copyright (c) 2012 Robert Buchholz <rbu@goodpoint.de>

from __future__ import absolute_import, unicode_literals, print_function

from unittest import TestCase

from pythonic_testcase import create_spy, assert_raises, assert_equals


class CreateSpyTest(TestCase):
    def test_spy_knows_if_it_was_called(self):
        spy = create_spy()
        spy.assert_was_not_called()
        assert_raises(AssertionError, spy.assert_was_called)
        spy()
        assert_raises(AssertionError, spy.assert_was_not_called)
        spy.assert_was_called()

    def test_should_know_keyword_call_parameters(self):
        spy = create_spy()
        assert_raises(AssertionError, lambda: spy.assert_was_called_with())
        spy()
        spy.assert_was_called_with()
        spy(foo='bar')
        spy.assert_was_called_with(foo='bar')
        assert_raises(AssertionError, lambda: spy.assert_was_called_with())
        assert_raises(AssertionError, lambda: spy.assert_was_called_with('bar'))
        assert_raises(AssertionError, lambda: spy.assert_was_called_with(foo='bar', fnord='baz'))

    def test_should_know_positional_call_parameters(self):
        spy = create_spy()
        spy(23)
        spy.assert_was_called_with(23)
        assert_raises(AssertionError, lambda: spy.assert_was_called_with())
        assert_raises(AssertionError, lambda: spy.assert_was_called_with(23, 24))
        assert_raises(AssertionError, lambda: spy.assert_was_called_with(foo=23))
        assert_raises(AssertionError, lambda: spy.assert_was_called_with(23, fnord='baz'))

    def test_should_allow_mocking_return_value(self):
        spy = create_spy().and_return(23)
        assert_equals(23, spy())

    def test_should_reset(self):
        spy = create_spy().and_return(23)
        spy()
        spy.reset()
        spy.assert_was_not_called()
        assert_equals(None, spy())
