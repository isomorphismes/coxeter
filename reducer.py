"""Tiny exact proof-producing reducer for Coxeter types A2 and A3.

Generators are numbered 1..rank. Type A_rank is identified exactly with the
symmetric group S_(rank+1), where generator i is the adjacent transposition
(i, i+1).

The permutation model is used only to answer the exact descent question
"did appending this generator increase or decrease Coxeter length?". Every
change to the word itself is justified by an explicit Coxeter relation and is
recorded as replayable RewriteEvidence.

This is intentionally not a general Coxeter reducer and not equality
saturation. For A3 a reduced prefix has length at most 6, so the only search
performed is a tiny breadth-first search through braid-equivalent words of
length at most 7, either to expose one cancellable pair or to choose a
lexicographically canonical reduced expression.
"""

from __future__ import annotations

import argparse
import json
from collections import deque
from dataclasses import dataclass
from typing import Iterable, Sequence

Word = tuple[int, ...]


@dataclass(frozen=True)
class RewriteEvidence:
    before: Word
    after: Word
    rule: str
    start: int
    generators: tuple[int, ...]
    coxeter_order: int

    def as_dict(self) -> dict[str, object]:
        return {
            "before": list(self.before),
            "after": list(self.after),
            "rule": self.rule,
            "start": self.start,
            "generators": list(self.generators),
            "coxeter_order": self.coxeter_order,
        }


@dataclass(frozen=True)
class Reduction:
    rank: int
    original: Word
    reduced: Word
    steps: tuple[RewriteEvidence, ...]

    @property
    def coxeter_type(self) -> str:
        return f"A{self.rank}"

    def replay(self) -> Word:
        return replay(self.rank, self.original, self.steps)

    def as_dict(self) -> dict[str, object]:
        return {
            "coxeter_type": self.coxeter_type,
            "original": list(self.original),
            "reduced": list(self.reduced),
            "steps": [step.as_dict() for step in self.steps],
        }


def _check_rank(rank: int) -> None:
    if rank not in (2, 3):
        raise ValueError(f"only A2 and A3 are supported, not A{rank}")


def _word(rank: int, generators: Iterable[int]) -> Word:
    _check_rank(rank)
    word = tuple(int(generator) for generator in generators)
    for generator in word:
        if not 1 <= generator <= rank:
            raise ValueError(
                f"generator {generator} is outside 1..{rank} for A{rank}"
            )
    return word


def coxeter_order(rank: int, left: int, right: int) -> int:
    """Return m(left,right) for type A2/A3."""
    _check_rank(rank)
    if not 1 <= left <= rank or not 1 <= right <= rank:
        raise ValueError("generator outside the Coxeter system")
    if left == right:
        return 1
    if abs(left - right) == 1:
        return 3
    return 2


def word_permutation(rank: int, generators: Iterable[int]) -> tuple[int, ...]:
    """Interpret an A_rank word as an exact permutation of 1..rank+1."""
    word = _word(rank, generators)
    permutation = list(range(1, rank + 2))
    for generator in word:
        i = generator - 1
        permutation[i], permutation[i + 1] = permutation[i + 1], permutation[i]
    return tuple(permutation)


def _inversion_count(permutation: Sequence[int]) -> int:
    return sum(
        left > right
        for i, left in enumerate(permutation)
        for right in permutation[i + 1 :]
    )


def word_length(rank: int, generators: Iterable[int]) -> int:
    """Exact Coxeter length in type A, computed as permutation inversions."""
    return _inversion_count(word_permutation(rank, generators))


def _cancel_index(word: Word) -> int | None:
    for i in range(len(word) - 1):
        if word[i] == word[i + 1]:
            return i
    return None


def _braid_neighbors(rank: int, word: Word) -> list[RewriteEvidence]:
    """All one-step braid/commutation rewrites, in deterministic order."""
    neighbors: list[RewriteEvidence] = []

    for i in range(len(word) - 1):
        left, right = word[i], word[i + 1]
        if coxeter_order(rank, left, right) == 2:
            after = word[:i] + (right, left) + word[i + 2 :]
            neighbors.append(
                RewriteEvidence(
                    before=word,
                    after=after,
                    rule="commute-order-two",
                    start=i,
                    generators=(left, right),
                    coxeter_order=2,
                )
            )

    for i in range(len(word) - 2):
        left, middle, right = word[i : i + 3]
        if left == right and coxeter_order(rank, left, middle) == 3:
            after = word[:i] + (middle, left, middle) + word[i + 3 :]
            neighbors.append(
                RewriteEvidence(
                    before=word,
                    after=after,
                    rule="braid",
                    start=i,
                    generators=(left, middle),
                    coxeter_order=3,
                )
            )

    neighbors.sort(key=lambda step: (step.after, step.start, step.rule))
    return neighbors


def _reconstruct_path(
    start: Word,
    predecessor: dict[Word, Word | None],
    edge: dict[Word, RewriteEvidence],
    target: Word,
) -> list[RewriteEvidence]:
    path: list[RewriteEvidence] = []
    current = target
    while current != start:
        path.append(edge[current])
        previous = predecessor[current]
        assert previous is not None
        current = previous
    path.reverse()
    return path


def _expose_cancellation(rank: int, word: Word) -> tuple[Word, list[RewriteEvidence]]:
    """Use braid moves only until an adjacent involution pair is visible."""
    if _cancel_index(word) is not None:
        return word, []

    queue: deque[Word] = deque([word])
    predecessor: dict[Word, Word | None] = {word: None}
    edge: dict[Word, RewriteEvidence] = {}

    while queue:
        current = queue.popleft()
        for step in _braid_neighbors(rank, current):
            candidate = step.after
            if candidate in predecessor:
                continue
            predecessor[candidate] = current
            edge[candidate] = step
            if _cancel_index(candidate) is not None:
                return candidate, _reconstruct_path(
                    word, predecessor, edge, candidate
                )
            queue.append(candidate)

    raise AssertionError(
        "non-reduced A2/A3 word had no braid path to an involution cancellation"
    )


def _canonicalize(rank: int, word: Word) -> tuple[Word, list[RewriteEvidence]]:
    """Choose the lexicographically least reduced word in its braid class."""
    queue: deque[Word] = deque([word])
    predecessor: dict[Word, Word | None] = {word: None}
    edge: dict[Word, RewriteEvidence] = {}
    best = word

    while queue:
        current = queue.popleft()
        if current < best:
            best = current
        for step in _braid_neighbors(rank, current):
            candidate = step.after
            if candidate in predecessor:
                continue
            predecessor[candidate] = current
            edge[candidate] = step
            queue.append(candidate)

    return best, _reconstruct_path(word, predecessor, edge, best)


def _lift(step: RewriteEvidence, suffix: Word) -> RewriteEvidence:
    """Lift a prefix rewrite so the evidence applies to the entire word."""
    return RewriteEvidence(
        before=step.before + suffix,
        after=step.after + suffix,
        rule=step.rule,
        start=step.start,
        generators=step.generators,
        coxeter_order=step.coxeter_order,
    )


def validate_step(rank: int, step: RewriteEvidence) -> bool:
    """Validate one evidence record from its stated exact Coxeter relation."""
    try:
        before = _word(rank, step.before)
        after = _word(rank, step.after)
    except (TypeError, ValueError):
        return False

    i = step.start
    if step.rule == "cancel-involution":
        if not 0 <= i < len(before) - 1:
            return False
        generator = before[i]
        return (
            before[i + 1] == generator
            and step.generators == (generator,)
            and step.coxeter_order == coxeter_order(rank, generator, generator) == 1
            and after == before[:i] + before[i + 2 :]
        )

    if step.rule == "commute-order-two":
        if not 0 <= i < len(before) - 1:
            return False
        left, right = before[i], before[i + 1]
        return (
            step.generators == (left, right)
            and step.coxeter_order == coxeter_order(rank, left, right) == 2
            and after == before[:i] + (right, left) + before[i + 2 :]
        )

    if step.rule == "braid":
        if not 0 <= i < len(before) - 2:
            return False
        left, middle, right = before[i : i + 3]
        return (
            left == right
            and step.generators == (left, middle)
            and step.coxeter_order == coxeter_order(rank, left, middle) == 3
            and after == before[:i] + (middle, left, middle) + before[i + 3 :]
        )

    return False


def replay(
    rank: int,
    original: Iterable[int],
    steps: Iterable[RewriteEvidence],
) -> Word:
    """Replay and independently validate a rewrite ledger."""
    current = _word(rank, original)
    for number, step in enumerate(steps):
        if step.before != current:
            raise ValueError(
                f"rewrite step {number} starts at {step.before}, expected {current}"
            )
        if not validate_step(rank, step):
            raise ValueError(f"rewrite step {number} is not a valid A{rank} relation")
        current = step.after
    return current


def reduce_word(rank: int, generators: Iterable[int]) -> Reduction:
    """Reduce an A2/A3 generator word and return replayable exact evidence."""
    original = _word(rank, generators)
    current: Word = ()
    steps: list[RewriteEvidence] = []

    for position, generator in enumerate(original):
        suffix = original[position + 1 :]
        candidate = current + (generator,)
        exact_length = word_length(rank, candidate)

        if exact_length == len(candidate):
            current = candidate
            continue

        # current is reduced. Multiplication by a simple reflection changes
        # length by exactly one, so a descent makes candidate two letters too
        # long. Tits/Matsumoto braid connectivity lets us expose ss and cancel.
        if exact_length != len(candidate) - 2:
            raise AssertionError("type-A simple-reflection length invariant failed")

        exposed, braid_steps = _expose_cancellation(rank, candidate)
        steps.extend(_lift(step, suffix) for step in braid_steps)

        cancel_at = _cancel_index(exposed)
        assert cancel_at is not None
        cancelled_generator = exposed[cancel_at]
        after = exposed[:cancel_at] + exposed[cancel_at + 2 :]
        cancellation = RewriteEvidence(
            before=exposed,
            after=after,
            rule="cancel-involution",
            start=cancel_at,
            generators=(cancelled_generator,),
            coxeter_order=1,
        )
        steps.append(_lift(cancellation, suffix))
        current = after

        if word_length(rank, current) != len(current):
            raise AssertionError("cancellation did not restore a reduced prefix")

    canonical, canonical_steps = _canonicalize(rank, current)
    steps.extend(canonical_steps)

    reduction = Reduction(rank, original, canonical, tuple(steps))
    if reduction.replay() != reduction.reduced:
        raise AssertionError("internal evidence replay failed")
    return reduction


def _parse_type(value: str) -> int:
    normalized = value.strip().upper()
    if normalized not in {"A2", "A3"}:
        raise argparse.ArgumentTypeError("type must be A2 or A3")
    return int(normalized[1])


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Reduce an A2/A3 Coxeter generator word with replayable evidence."
    )
    parser.add_argument("type", type=_parse_type, metavar="A2|A3")
    parser.add_argument("generators", nargs="*", type=int)
    args = parser.parse_args(argv)

    reduction = reduce_word(args.type, args.generators)
    print(json.dumps(reduction.as_dict(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
