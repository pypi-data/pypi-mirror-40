# -*- coding: UTF-8 -*-
#
# SPDX-License-Identifier: MIT
# Copyright (c) 2016 Felix Schwarz <felix.schwarz@oss.schwarz.eu>

from __future__ import absolute_import, unicode_literals, print_function

from pythonic_testcase import PythonicTestCase, SkipTest


class SkippingTestsTest(PythonicTestCase):
    def test_can_skip_tests(self):
        # This test should be marked as "skipped"
        raise SkipTest('just because')

    def test_can_skip_via_instance_method(self):
        # This test should be marked as "skipped"
        self.skipTest('can do it also without raise')

