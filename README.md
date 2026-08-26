# Coxeter

A working repository for reflections, Coxeter groups, Dynkin diagrams, root systems, and compiler-facing uses of their algebraic structure.

The immediate engineering question is: when code constructs a sequence of reflections, rotations, or matrix products with certified group structure, can we preserve that meaning long enough to simplify the sequence algebraically instead of blindly multiplying matrices?

Research notes and experiments should keep exact algebraic claims separate from floating-point observations, and should retain provenance for each rewrite used.

## Start here

- [Compiler rewrite sketch](notes/compiler-rewrite-sketch.md) — proposed IR, Coxeter relations, reduced words, proof-carrying rewrites, and lowering order.
- [Idriç-shaped Dynkin/Coxeter pseudocode](pseudocode/Dynkin.idric) — data boundaries for Coxeter systems, Dynkin/Cartan data, words, reflectors, and rewrite evidence.
- [Householder reflectors](notes/householder-reflectors.md) — numerical-linear-algebra bridge and compact reflection representation.
- [John Baez: ADE and Dynkin diagrams](notes/baez-ade-dynkin.md) — summaries of the main Baez sequences with compiler takeaways.
- [Open-source survey](notes/open-source-survey.md) — Sage, coxeter3, CHEVIE, GAP, LAPACK, Eigen, egglog, TensorRight, and related references.
- [Humphreys: *Reflection Groups and Coxeter Groups*](books/humphreys-reflection-groups-and-coxeter-groups.md) — sourcing/licensing notes and chapter-level orientation.
- [Other books and long references](books/README.md).
- [Federico Ardila's Coxeter-groups lectures](video-lectures/federico-ardila-coxeter-groups.md) — official YouTube/course/index links and high-value lecture clusters.
- [Pending RHS-verification integration issue](issues/rhs-verification-import-coxeter.md) — preserved here because GitHub Issues are currently disabled in the target repository.

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
