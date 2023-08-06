# -*- coding: utf-8 -*-

"""Split an iterable into multiple using arbitrary predicates."""

from typing import Callable, Iterable, TypeVar, Union

__all__ = [
    'VERSION',
    'multi_split_by',
]

VERSION = '0.0.1'


class _Sentinel:
    pass


F = TypeVar('F')
MaybeF = Union[F, _Sentinel]


def multi_split_by(values: Iterable[F], predicates: Iterable[Callable[[F], bool]]) -> Iterable[Iterable[F]]:
    """Split the iterator after the predicate becomes true, then repeat for every remaining iterable.

    For all lists ``values`` and ``predicates``, the following conditions are always true:

    1. ``1 + len(predicates) = len(list(multi_split_by(values, predicates)))``
    2. ``values == itertools.chain.from_iterable(multi_split_by(values, predicates))``

    Normal usage with one predicate:
    >>> values = range(4)
    >>> predicates = [lambda x: 2 < x]
    >>> list(map(list, multi_split_by(values, predicates)))
    [[0, 1, 2], [3]]

    Normal usage with several predicates:
    >>> values = range(9)
    >>> predicates = [lambda x: 2 < x, lambda x: 4 < x, lambda x: 7 < x]
    >>> list(map(list, multi_split_by(values, predicates)))
    [[0, 1, 2], [3, 4], [5, 6, 7], [8]]

    If no values are given, will result in |predicates| + 1 generators, all yielding empty lists.
    >>> values = []
    >>> predicates = [lambda x: 2 < x, lambda x: 4 < x, lambda x: 7 < x]
    >>> list(map(list, multi_split_by(values, predicates)))
    [[], [], [], []]

    If no predicates are given, will result in a single generator that yields the original list:
    >>> values = range(4)
    >>> predicates = []
    >>> list(map(list, multi_split_by(values, predicates)))
    [[0, 1, 2, 3]]
    """
    last_value = _Sentinel()  # type: MaybeF
    values = iter(values)

    def generator(p: Callable[[F], bool]) -> Iterable[F]:
        """Yield values until the given predicate is met, keeping the last value saved each time."""
        nonlocal last_value

        if not isinstance(last_value, _Sentinel):
            yield last_value

        for value in values:
            if p(value):
                last_value = value
                return

            yield value

    yield from map(generator, predicates)

    def generator_last() -> Iterable[F]:
        """Yield the remaining value on which the last predicate stopped, then the remainder of the iterable."""
        if not isinstance(last_value, _Sentinel):
            yield last_value

        yield from values

    yield generator_last()
