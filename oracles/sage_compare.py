"""Behavioral oracle for reducer.py using Sage and optional coxeter3.

Run with Sage, not ordinary Python:

    sage -python oracles/sage_compare.py

The oracle intentionally does not require our canonical reduced word to match
Sage's chosen reduced expression. Reduced expressions are not unique. It
checks the invariant behavior that matters:

* original and returned words represent the same group element;
* returned word has Sage's exact Coxeter length;
* the proof ledger replays locally before the external comparison.

If Sage's optional coxeter3 package is installed, the same fixtures are also
checked with implementation="coxeter3".
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from reducer import reduce_word
from sage.all import CoxeterGroup


FIXTURES = {
    2: [
        (),
        (1, 1),
        (1, 2, 1),
        (2, 1, 2),
        (1, 2, 1, 2, 1, 2),
        (2, 1, 1, 2, 1, 2, 2, 1),
    ],
    3: [
        (),
        (1, 3, 1),
        (1, 2, 1, 2),
        (1, 2, 3, 1, 2, 1),
        (3, 2, 1, 3, 2, 3),
        (1, 3, 2, 1, 3, 2, 2, 1, 3),
    ],
}


def product(group, word):
    simple = group.simple_reflections()
    value = group.one()
    for generator in word:
        value *= simple[generator]
    return value


def check_backend(rank, backend):
    group = CoxeterGroup(["A", rank], implementation=backend)
    for word in FIXTURES[rank]:
        reduction = reduce_word(rank, word)
        assert reduction.replay() == reduction.reduced

        original = product(group, reduction.original)
        reduced = product(group, reduction.reduced)
        assert original == reduced, (backend, rank, word, reduction.reduced)
        assert len(reduction.reduced) == original.length(), (
            backend,
            rank,
            word,
            reduction.reduced,
            original.reduced_word(),
        )

        print(
            f"{backend:10} A{rank} {list(word)!s:28} -> "
            f"{list(reduction.reduced)!s:18} "
            f"sage={list(original.reduced_word())}"
        )


def main():
    for rank in (2, 3):
        check_backend(rank, "reflection")

    try:
        for rank in (2, 3):
            check_backend(rank, "coxeter3")
    except (ImportError, RuntimeError, TypeError, ValueError) as error:
        print(f"coxeter3 oracle skipped: {error}")


if __name__ == "__main__":
    main()
