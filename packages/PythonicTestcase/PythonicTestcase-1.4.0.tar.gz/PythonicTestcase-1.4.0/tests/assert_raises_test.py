# -*- coding: UTF-8 -*-
#
# SPDX-License-Identifier: MIT
# Copyright (c) 2011, 2015 Felix Schwarz <felix.schwarz@oss.schwarz.eu>

from __future__ import absolute_import, unicode_literals, print_function

from unittest import TestCase

from pythonic_testcase import assert_raises
from .util import exception_message


class AssertRaisesTest(TestCase):
    # assert_raises is the basis of all testing. Therefore this test case must
    # not use any other helper method.
    def _good_callable(self):
        return lambda: None

    def test_fails_if_no_exception_was_raised(self):
        try:
            assert_raises(Exception, self._good_callable())
        except AssertionError:
            pass
        else:
            self.fail('No assertion raised')

    def _fail_with(self, exception):
        def failing_callable():
            raise exception
        return failing_callable

    def test_passes_if_callable_raised_exception(self):
        assert_raises(ValueError, self._fail_with(ValueError()))
        # also test for Python 2.6 specific "behavior"/bug where
        # Python 2.6 sometimes only passes a string (instead of
        # the exception instance) to the context manager
        # https://bugs.python.org/issue7853
        def raises_valueerror():
            from datetime import date
            # not sure how to reproduce the issue generically but
            # this date call triggers it at least.
            date(2000, 12, 50)
        assert_raises(ValueError, raises_valueerror)

    def test_returns_caught_exception_instance(self):
        expected_exception = ValueError('foobar')
        e = assert_raises(ValueError, self._fail_with(expected_exception))
        assert expected_exception == e
        assert id(expected_exception) == id(e)

    def test_callable_can_also_raise_assertion_error(self):
        expected_exception = AssertionError('foobar')
        e = assert_raises(AssertionError, self._fail_with(expected_exception))
        assert expected_exception == e
        assert id(expected_exception) == id(e)

    def test_passes_unexpected_exceptions(self):
        try:
            assert_raises(ValueError, self._fail_with(AssertionError()))
        except AssertionError:
            pass
        else:
            self.fail('Did not raise ValueError')

    def test_fails_with_sensible_default_error_message(self):
        try:
            assert_raises(ValueError, self._good_callable())
        except AssertionError as e:
            assert 'ValueError not raised!' == exception_message(e), repr(exception_message(e))
        else:
            self.fail('AssertionError not raised!')

    def test_can_specify_additional_custom_message(self):
        try:
            assert_raises(ValueError, self._good_callable(), message='Foo')
        except AssertionError as e:
            assert 'ValueError not raised! Foo' == exception_message(e), repr(exception_message(e))
        else:
            self.fail('AssertionError not raised!')

    def test_can_return_contextmanager(self):
        with assert_raises(ValueError):
            raise ValueError()

        try:
            with assert_raises(ValueError):
                raise AssertionError()
        except AssertionError:
            pass
        else:
            self.fail('Did not raise ValueError')

        try:
            with assert_raises(ValueError):
                pass
        except AssertionError:
            pass
        else:
            self.fail('No assertion raised')

