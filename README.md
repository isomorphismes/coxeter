# Coxeter

A working repository for reflections, Coxeter groups, Dynkin diagrams, root systems, and compiler-facing uses of their algebraic structure.

The immediate engineering question is: when code constructs a sequence of reflections, rotations, or matrix products with certified group structure, can we preserve that meaning long enough to simplify the sequence algebraically instead of blindly multiplying matrices?

Research notes and experiments should keep exact algebraic claims separate from floating-point observations, and should retain provenance for each rewrite used.
