# -*- coding: UTF-8 -*-
#
# SPDX-License-Identifier: MIT
# Copyright (c) 2015 Felix Schwarz <felix.schwarz@oss.schwarz.eu>

from __future__ import absolute_import, unicode_literals, print_function

from unittest import TestCase

from pythonic_testcase import assert_equals, assert_not_raises
from .util import exception_message


class AssertNotRaisesTest(TestCase):
    def test_passes_if_callable_did_not_raise_exception(self):
        assert_not_raises(Exception, self._good_callable())
        assert_not_raises(callable=self._good_callable(),
            message='exception class should be optional')

    def test_fails_if_callable_raised_exception(self):
        try:
            assert_not_raises(ValueError, self._fail_with(ValueError))
            self.fail('assert_not_raises() did not notice raised ValueError')
        except AssertionError:
            pass
        except ValueError:
            self.fail('assert_not_raises() should wrap caught exceptions')

    def test_pass_unexpected_exceptions_unmodified(self):
        try:
            assert_not_raises(ValueError, self._fail_with(Exception))
        except AssertionError:
            self.fail('raised Exception is unexpected, should be passed up without modification')
        except Exception:
            pass

    def test_fails_with_sensible_default_error_message(self):
        try:
            assert_not_raises(Exception, self._fail_with(ValueError))
        except AssertionError as e:
            assert_equals('unexpected exception ValueError()', exception_message(e))
        else:
            self.fail('test did not catch exception!')

    def test_can_specify_additional_custom_message(self):
        try:
            assert_not_raises(Exception, self._fail_with(ValueError), message='Foo')
        except AssertionError as e:
            assert_equals('unexpected exception ValueError(): Foo', exception_message(e))
        else:
            self.fail('test did not catch exception!')

    def test_can_return_contextmanager(self):
        with assert_not_raises(ValueError):
            pass

        try:
            with assert_not_raises(ValueError):
                raise ValueError()
        except AssertionError:
            pass
        else:
            self.fail('Did not catch ValueError which was mentioned explicitely.')

        try:
            with assert_not_raises(ValueError):
                raise TypeError()
        except AssertionError:
            self.fail('raised Exception is unexpected, should be passed up without modification')
        except TypeError:
            # exception was passed up without modification which is ok as the
            # exception is really unexpected and the developer should get as
            # much information about it as possible.
            pass

    # --- internal helpers ----------------------------------------------------

    def _good_callable(self):
        return lambda: None

    def _fail_with(self, exception):
        def failing_callable():
            raise exception
        return failing_callable

