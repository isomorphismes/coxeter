# Coxeter

A working repository for reflections, Coxeter groups, Dynkin diagrams, root systems, and compiler-facing uses of their algebraic structure.

The immediate engineering question is: when code constructs a sequence of reflections, rotations, or matrix products with certified group structure, can we preserve that meaning long enough to simplify the sequence algebraically instead of blindly multiplying matrices?

Research notes and experiments should keep exact algebraic claims separate from floating-point observations, and should retain provenance for each rewrite used.

## Start here

- [A2/A3 exact reducer](reducer.py) — first executable slice: deterministic reduced generator words plus replayable involution/commute/braid evidence.
- [Reducer tests](tests/test_reducer.py) — exact permutation/length checks, proof replay, exhaustive small words, tamper rejection, and long-input coverage.
- [Sage/coxeter3 behavioral oracle](oracles/sage_compare.py) — compares group element and exact Coxeter length without requiring another implementation to choose the same reduced spelling.
- [Compiler rewrite sketch](notes/compiler-rewrite-sketch.md) — proposed IR, Coxeter relations, reduced words, proof-carrying rewrites, and lowering order.
- [Idriç-shaped Dynkin/Coxeter pseudocode](pseudocode/Dynkin.idric) — data boundaries for Coxeter systems, Dynkin/Cartan data, words, reflectors, and rewrite evidence.
- [Householder reflectors](notes/householder-reflectors.md) — numerical-linear-algebra bridge and compact reflection representation.
- [John Baez: ADE and Dynkin diagrams](notes/baez-ade-dynkin.md) — summaries of the main Baez sequences with compiler takeaways.
- [Open-source survey](notes/open-source-survey.md) — Sage, coxeter3, CHEVIE, GAP, LAPACK, Eigen, egglog, TensorRight, and related references.
- [Humphreys: *Reflection Groups and Coxeter Groups*](books/humphreys-reflection-groups-and-coxeter-groups.md) — sourcing/licensing notes and chapter-level orientation.
- [Other books and long references](books/README.md).
- [Federico Ardila's Coxeter-groups lectures](video-lectures/federico-ardila-coxeter-groups.md) — official YouTube/course/index links and high-value lecture clusters.
- [Pending RHS-verification integration issue](issues/rhs-verification-import-coxeter.md) — preserved here because GitHub Issues are currently disabled in the target repository.

## First executable slice

The reducer intentionally supports only finite types `A2` and `A3`.

```sh
python reducer.py A3 1 3 1
python -m unittest discover -s tests -v
```

The command prints JSON containing the original word, a deterministic lexicographically least reduced word, and a sequence of exact rewrite records. `replay` independently validates every record against the A2/A3 Coxeter matrix before applying it.

Type A is exactly the symmetric group, so the implementation uses the corresponding permutation inversion count only to decide whether appending a simple reflection raises or lowers Coxeter length. The actual word is changed only by recorded Coxeter relations: involution cancellation, order-two commutation, and the order-three braid relation.

For an external behavioral comparison, with Sage installed:

```sh
sage -python oracles/sage_compare.py
```

The script checks the ordinary Sage reflection implementation and, when Sage's optional `coxeter3` package is installed, repeats the same fixtures with `implementation="coxeter3"`. It compares represented group elements and exact lengths rather than insisting that independent implementations choose the same reduced expression.

This slice deliberately does not introduce a general Coxeter matrix engine, minimal-root automata, or equality saturation. In `A3` the longest reduced word has length 6, so the only search is a tiny finite braid-class search of length at most 7 used to expose a cancellation or choose the deterministic reduced spelling.

## Compiler north star

Keep the strongest *certified* representation available:

```text
generic matrix
  → certified orthogonal operator
  → certified reflection / Householder operator
  → certified Coxeter generator
  → symbolic generator word
  → exact reduction with replayable evidence
  → matrix/vector lowering only when needed
```

Do not climb this ladder by guessing from floating-point resemblance. A matrix that numerically looks orthogonal is weaker evidence than an operation constructed as a reflection, and an arbitrary reflection is weaker evidence than a reflection certified as a particular generator of a Coxeter system.
