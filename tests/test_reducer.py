import itertools
import random
import unittest

from reducer import reduce_word, replay, word_length, word_permutation


class ReducerTests(unittest.TestCase):
    def assert_reduction(self, rank, word, expected=None):
        reduction = reduce_word(rank, word)
        if expected is not None:
            self.assertEqual(reduction.reduced, tuple(expected))
        self.assertEqual(reduction.replay(), reduction.reduced)
        self.assertEqual(
            word_permutation(rank, reduction.original),
            word_permutation(rank, reduction.reduced),
        )
        self.assertEqual(len(reduction.reduced), word_length(rank, reduction.original))
        return reduction

    def test_a2_relations(self):
        self.assert_reduction(2, [1, 1], [])
        self.assert_reduction(2, [2, 2], [])
        self.assert_reduction(2, [2, 1, 2], [1, 2, 1])
        self.assert_reduction(2, [1, 2, 1, 2, 1, 2], [])

    def test_a3_commutation_exposes_cancellation(self):
        reduction = self.assert_reduction(3, [1, 3, 1], [3])
        self.assertEqual(
            [step.rule for step in reduction.steps],
            ["commute-order-two", "cancel-involution"],
        )

    def test_evidence_replays_from_whole_original_word(self):
        reduction = self.assert_reduction(3, [1, 3, 1, 2, 2], [3])
        current = reduction.original
        for step in reduction.steps:
            self.assertEqual(step.before, current)
            current = step.after
        self.assertEqual(current, reduction.reduced)

    def test_invalid_generator_is_rejected(self):
        with self.assertRaises(ValueError):
            reduce_word(2, [3])
        with self.assertRaises(ValueError):
            reduce_word(3, [0])

    def test_replay_rejects_tampered_evidence(self):
        reduction = reduce_word(3, [1, 3, 1])
        first = reduction.steps[0]
        tampered = type(first)(
            before=first.before,
            after=first.after,
            rule=first.rule,
            start=first.start,
            generators=first.generators,
            coxeter_order=3,
        )
        with self.assertRaises(ValueError):
            replay(3, reduction.original, [tampered, *reduction.steps[1:]])

    def test_exhaustive_small_words_have_exact_minimal_length_and_replay(self):
        for rank, maximum_input_length in ((2, 8), (3, 7)):
            alphabet = range(1, rank + 1)
            for length in range(maximum_input_length + 1):
                for word in itertools.product(alphabet, repeat=length):
                    with self.subTest(rank=rank, word=word):
                        self.assert_reduction(rank, word)

    def test_returned_reduced_word_is_lexicographically_canonical(self):
        for rank in (2, 3):
            alphabet = range(1, rank + 1)
            longest = rank * (rank + 1) // 2
            canonical = {}
            for length in range(longest + 1):
                for word in itertools.product(alphabet, repeat=length):
                    permutation = word_permutation(rank, word)
                    if word_length(rank, word) != length:
                        continue
                    canonical.setdefault(permutation, word)
                    canonical[permutation] = min(canonical[permutation], word)

            for permutation, expected in canonical.items():
                reduction = reduce_word(rank, expected)
                self.assertEqual(word_permutation(rank, reduction.reduced), permutation)
                self.assertEqual(reduction.reduced, expected)

    def test_long_inputs_do_not_expand_the_search_boundary(self):
        rng = random.Random(0)
        for rank in (2, 3):
            word = [rng.randint(1, rank) for _ in range(1000)]
            self.assert_reduction(rank, word)


if __name__ == "__main__":
    unittest.main()
