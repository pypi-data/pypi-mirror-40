# Copyright (C) 2019 Max Steinberg

import collections


class complexrange(collections.abc.Sequence):
    """A complex range."""
    def __init__(self, rng_i, rng_j):
        """Takes two tuples: (start_i, stop_i[, step_i]), (start_j, stop_j[, step_j])."""
        if len(rng_i) < 2:
            raise ValueError(f"{rng_i} does not have enough parameters (expected 2-3, got {len(rng_i)}).")

        if len(rng_j) < 2:
            raise ValueError(f"{rng_j} does not have enough parameters (expected 2-3, got {len(rng_j)}).")

        self._start_i = rng_i[0]
        self._end_i = rng_i[1]
        self._step_i = rng_i[2] if len(rng_i) > 2 else 1
        self._start_j = rng_j[0]
        self._end_j = rng_j[1]
        self._step_j = rng_j[2] if len(rng_j) > 2 else 1

        if (self._end_i - self._start_i) // self._step_i != (self._end_j - self._start_j) // self._step_j:
            raise ValueError("Ranges are of different length!")

        self.length = abs((self._end_i - self._start_i) // self._step_i) + 1

    def __contains__(self, item: complex) -> bool:
        """Is this complex value in the range?"""
        if self._step_i < 0:
            if not (self._end_i < item.real <= self._start_i):
                return False
        else:
            if not (self._start_i <= item.real < self._end_i):
                return False
        if self._step_j < 0:
            if not (self._end_j < item.imag <= self._start_j):
                return False
        else:
            if not (self._start_j <= item.imag < self._end_j):
                return False
        return (item.real - self._start_i) % self._step_i == 0 and (item.imag - self._start_j) % self._step_j == 0

    def __len__(self) -> int:
        """Length of range."""
        return self.length

    def __getitem__(self, item) -> complex:
        """Get an item from the range."""
        while item < 0:
            item += self.length
        if 0 <= item < self.length:
            return self._start_i + item * self._step_i + (self._start_j + item * self._step_j) * 1j
        raise IndexError('Index out of range: {}'.format(item))

    def __reversed__(self):
        """Reverse the range."""
        return complexrange((self._end_i, self._start_i, -self._step_i), (self._end_j, self._start_j, -self._step_j))
