# Coxeter

A working repository for reflections, Coxeter groups, Dynkin diagrams, root systems, and compiler-facing uses of their algebraic structure.

The immediate engineering question is: when code constructs a sequence of reflections, rotations, or matrix products with certified group structure, can we preserve that meaning long enough to simplify the sequence algebraically instead of blindly multiplying matrices?

Research notes and experiments should keep exact algebraic claims separate from floating-point observations, and should retain provenance for each rewrite used.

## Geometry and response-map notes

- [Gromov: Sign and Geometric Meaning of Curvature](references/gromov/sign-and-geometric-meaning-of-curvature.md) — existing reading guide, not a mirrored PDF.
- [Suspension response maps: retain the structure before the matrix](notes/suspension-response-structure.md) — spaces, metrics, units, orientations, chain rules, and coordinate invariants in the eccentric-cam example. Cross-linked with ASE, Econometrician in a Box, and Fulton. This is a design note, not an implemented reducer, a calibrated truck model, or validation of speculative CP^n/SO(n) machinery.
