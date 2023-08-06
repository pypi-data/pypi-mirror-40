# -*- coding: utf-8 -*-

"""Tests for multigroupby."""

import unittest
from typing import Iterable

from multisplitby import multi_split_by


def _consume(iterable: Iterable):
    def yield_all():
        yield from iterable

    return list(yield_all())


def predicate_1(x: int) -> bool:
    """Return true if the integer is 3."""
    return x == 3


def predicate_2(x: int) -> bool:
    """Return true if the integer is 6."""
    return x == 6


def predicate_3(x: int) -> bool:
    """Return true if the integer is 8."""
    return x == 8


class TestIter(unittest.TestCase):
    """Test :mod:`multisplitby`."""

    def test_split_by_iterable_is_empty(self):
        """Test when an empty iterable is given."""
        integers = []
        predicates = [predicate_1, predicate_2]

        r = list(multi_split_by(integers, predicates))
        self.assertEqual(1 + len(predicates), len(r))

        a, b, c = r
        self.assertIsNotNone(a)
        self.assertIsNotNone(b)
        self.assertIsNotNone(c)

        a = _consume(a)
        b = _consume(b)
        c = _consume(c)

        self.assertEqual([], a)
        self.assertEqual([], b)
        self.assertEqual([], c)

    def test_split_by_predicates_is_empty(self):
        """Test when empty predicates are given."""
        integers = [1, 2, 3, 4]
        predicates = []

        r = tuple(multi_split_by(integers, predicates))
        self.assertEqual(1 + len(predicates), len(r))

        a, = r
        self.assertIsNotNone(a)
        a = _consume(a)
        self.assertEqual([1, 2, 3, 4], a)

    def test_split_by_two(self):
        """Test the :func:`multisplitby.multi_split_by` function with two predicates."""
        integers = [1, 2, 3, 4, 5, 6, 7]
        predicates = [predicate_1, predicate_2]
        # expected = [[1, 2], [3, 4, 5], [6, 7]]

        r = tuple(multi_split_by(integers, predicates))
        self.assertEqual(1 + len(predicates), len(r))

        a, b, c = r
        self.assertIsNotNone(a)
        self.assertIsNotNone(b)
        self.assertIsNotNone(c)

        a = _consume(a)
        b = _consume(b)
        c = _consume(c)

        self.assertEqual([1, 2], a)
        self.assertEqual([3, 4, 5], b)
        self.assertEqual([6, 7], c)

    def test_split_by_three(self):
        """Test the :func:`multisplitby.multi_split_by` function with three predicates."""
        integers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        predicates = [predicate_1, predicate_2, predicate_3]
        # expected = [[1, 2], [3, 4, 5], [6, 7], [8, 9, 10]]

        r = tuple(multi_split_by(integers, predicates))
        self.assertEqual(1 + len(predicates), len(r))

        a, b, c, d = r
        self.assertIsNotNone(a)
        self.assertIsNotNone(b)
        self.assertIsNotNone(c)
        self.assertIsNotNone(d)

        a = _consume(a)
        b = _consume(b)
        c = _consume(c)
        d = _consume(d)

        self.assertEqual([1, 2], a)
        self.assertEqual([3, 4, 5], b)
        self.assertEqual([6, 7], c)
        self.assertEqual([8, 9, 10], d)
