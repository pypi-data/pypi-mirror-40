# -*- coding: utf-8 -*-

"""
Core routines and optimization logic.
"""

import collections as _collections
import itertools as _itertools
import json as _json
import logging as _logging

import multiset as _multiset

from . import check as _check


logger = _logging.getLogger(__name__)  # pylint: disable=invalid-name


def convert_order_position(vector):
    """Convert an order vector into a position vector, and vice-versa."""
    # order vectors and position vectors are dual objects, see the definition
    # of final_position for a more detailed description
    dual = [None] * len(vector)
    for i, item in enumerate(vector):
        dual[item] = i
    return dual


def final_position(matrix):
    """Compute the final position of strands according to the linking matrix."""
    assert _check.is_symmetric(matrix)
    size = len(matrix)
    # compute the final order of strands using Melvin's algorithm
    # given a strand `s` and an index `i`, we have `final_order[i] == s`
    final_order = list(range(size))
    for i, row in enumerate(matrix):
        for j in range(i):  # decreasing index in final order
            if row[j] % 2 == 1:
                final_order[i] -= 1
        for j in range(i + 1, size):  # increasing index in final order
            if row[j] % 2 == 1:
                final_order[i] += 1
    # transform final_order to get the final position
    # given a strand `s` and an index `i`, we have `final_position_[s] == i`
    return convert_order_position(final_order)


def _pairwise(iterable):
    # see https://docs.python.org/3/library/itertools.html#itertools-recipes
    a, b = _itertools.tee(iterable)  # pylint: disable=invalid-name
    next(b, None)
    return zip(a, b)


class _OptimizerState:
    """Internal state of the optimization logic to compute crosslevels."""

    __slots__ = ('position', 'crossings', )

    def __init__(self, position, crossings):
        self.position = position  # current position of strands
        self.crossings = crossings  # remaining crossings

    @staticmethod
    def _adjacent_pairs(position):
        """Generate the pairs of adjacent strands, in increasing order."""
        for left, right in _pairwise(position):
            if left < right:
                yield left, right
            else:
                yield right, left

    @staticmethod
    def _is_valid_transition(transition):
        """Return True iff every strand is used in at most one crossing."""
        already_encountered = set()
        for crossing in transition:
            for strand in crossing:
                if strand in already_encountered:
                    return False  # strand is used more than once
                else:
                    already_encountered.add(strand)
        return True

    def _valid_transitions(self):
        """Generate the valid transitions from self."""
        # keep one occurence of each remaining crossings
        crossings_set = set(self.crossings.distinct_elements())
        # only consider crossings of adjacent strands
        crossings_set.intersection_update(self._adjacent_pairs(self.position))

        # yield valid transitions with decreasing number of crossings
        for size in reversed(range(1, len(crossings_set) + 1)):
            yield from filter(
                self._is_valid_transition,
                _itertools.combinations(crossings_set, size)
            )

    @staticmethod
    def _apply_transition(position, transition):
        """Compute the position reached by applying transition to position."""
        order = convert_order_position(position)
        new_position = list(position)  # do not alter original position
        for left, right in transition:
            new_position[order[left]], new_position[order[right]] = \
                    new_position[order[right]], new_position[order[left]]
            order[left], order[right] = order[right], order[left]

        return tuple(new_position)

    def next_states(self):
        """
        Generate the tuples (state, transition) for reachable states from self.
        """
        for transition in self._valid_transitions():
            new_position = self._apply_transition(self.position, transition)
            new_crossings = self.crossings.difference(transition)
            new_state = type(self)(new_position, new_crossings)
            yield new_state, transition

    def __eq__(self, other):
        return self.position == other.position and \
                self.crossings == other.crossings

    def __hash__(self):
        return hash((self.position, self.crossings))


class Template:
    def __init__(self, matrix):
        if not _check.is_linking(matrix):
            raise ValueError('Invalid linking matrix')
        self.matrix = matrix
        self.__crosslevels = None

    @classmethod
    def from_json(cls, fp):  # pylint: disable=invalid-name
        """
        Create a template by loading a linking matrix from a JSON file.

        Deserialize `fp` (a `.read()`-supporting text file containing a JSON
        document) to a Python object compatible with the structure of a linking
        matrix.

        A linking matrix serialized as a JSON document must be structured as a
        JSON array made of arrays of integers.  The validity of the matrix is
        not checked by this function.

        If the data being deserialized has not a structure compatible with the
        structure of a linking matrix, a TypeError will be raised.
        """

        # interpret the input as a JSON file
        try:
            matrix = _json.load(fp)
        except _json.JSONDecodeError as err:
            raise TypeError('Malformed JSON') from err

        # check the loaded input JSON structure is compatible with a linking
        # matrix object: i.e., a List[List[int]]
        if not isinstance(matrix, list):
            raise TypeError('Invalid input structure')
        if not matrix:  # empty linking matrix
            raise TypeError('Invalid input structure')
        for row in matrix:
            if not isinstance(row, list):
                raise TypeError('Invalid input structure')
            for coeff in row:
                if not isinstance(coeff, int):
                    raise TypeError('Invalid input structure')

        return cls(matrix)

    @property
    def size(self):
        """Number of strands of the template."""
        return len(self.matrix)

    @property
    def torsions(self):
        """Number of (oriented) torsions for each strand of the template."""
        return [self.matrix[i][i] for i in range(len(self.matrix))]

    @property
    def crossings(self):
        """
        Mapping of {crossing: arity} for each (oriented) crossing of the template.
        """
        return {
            (j, i): self.matrix[i][j]
            for i in range(len(self.matrix))
            for j in range(i)
            if self.matrix[i][j]  # keep only crossings with non-zero arity
        }

    def _optimize_crosslevels(self):
        """Compute a sequence of crossing levels of minimum depth."""
        initial_state = _OptimizerState(
            tuple(range(self.size)),
            _multiset.FrozenMultiset(
                {
                    # the optimization loop needs the arity of each crossing
                    # without their orientation: drop orientation
                    crossing: abs(arity)
                    for crossing, arity in self.crossings.items()
                }
            )
        )
        final_state = _OptimizerState(
            tuple(final_position(self.matrix)),
            _multiset.FrozenMultiset()
        )

        # depth tracks the number of crosslevels
        # path tracks the previous state
        # how tracks the transition used from the previous state
        depth, path, how = {initial_state: 0}, {}, {}

        lifo = _collections.deque()
        lifo.append(initial_state)
        while lifo:
            current_state = lifo.popleft()
            for new_state, transition in current_state.next_states():
                if new_state not in depth:
                    depth[new_state], path[new_state], how[new_state] = \
                            depth[current_state] + 1, current_state, transition
                    lifo.append(new_state)

        crosslevels = [None] * depth[final_state]
        current_state = final_state
        for depth in reversed(range(depth[final_state])):
            crosslevels[depth] = how[current_state]
            current_state = path[current_state]

        return crosslevels

    @property
    def crosslevels(self):
        """Level-by-level list of concurrent crossings of the template."""
        if self.__crosslevels is None:
            logger.info('Starting optimization of template depth')
            self.__crosslevels = self._optimize_crosslevels()
            logger.info('Finished optimization of template depth')
        return self.__crosslevels
