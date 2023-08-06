# -*- coding: UTF-8 -*-
#
# SPDX-License-Identifier: MIT
# Copyright (c) 2016 Felix Schwarz <felix.schwarz@oss.schwarz.eu>

from __future__ import absolute_import, unicode_literals, print_function

from pythonic_testcase import assert_raises, expect_failure, PythonicTestCase, _ExpectedFailure


class ExpectedFailureTest(PythonicTestCase):
    @expect_failure
    def test_failing_tests_marked_as_expected_failure_are_not_treated_as_errors(self):
        raise AssertionError('not yet fixed')

    def test_passing_tests_marked_as_expected_failure_are_treated_as_errors(self):
        @expect_failure
        def passing():
            pass

        with assert_raises(AssertionError, message='should treat passing tests as error'):
            passing()

    def test_tests_with_errors_marked_as_expected_failure_are_treated_as_errors(self):
        # This is actually a really important part of the "expected failure"
        # concept: The test code should not bit-rot due to API changes but
        # always exercise the exact problem.
        @expect_failure
        def error_test():
            raise ValueError('foobar')

        try:
            with assert_raises(ValueError, message='should treat errors (anything besides AssertionError) as error'):
                error_test()
        except _ExpectedFailure:
            # need to handle this exception explicitly as test runners (e.g.
            # nosetests on Python 2.7) can't tell which part of the code
            # (test code or the PythonicTestcase decorator) threw the exception.
            # This ensures our decorator really just catches AssertionError.
            self.fail('ValueError should cause errors')


if __name__ == '__main__':
    import unittest
    unittest.main()
