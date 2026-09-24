# Pending issue: import Coxeter into RHS verification

Target repository: https://github.com/isomorphisms/the-equality-sign-means-equality

GitHub Issues were disabled on the target repository when this was attempted on 2026-08-26, so the issue could not be posted. Preserve the intended issue here until Issues are enabled.

## Proposed title

Import Coxeter and use reflection/group structure in RHS verification

## Proposed body

Track integration with https://github.com/isomorphisms/coxeter.

Goal: let RHS verification use explicit reflection/group-theoretic structure rather than treating every transformation as an unrelated matrix operation.

Initial uses to investigate:

- recognize reflections, rotations, Coxeter generators, and known relations;
- canonicalize or reduce sequences of transformations before comparing claimed RHS meaning with computed behavior;
- expose group relations as deterministic evidence alongside vector/matrix evidence;
- distinguish an exact algebraic reduction from a floating-point numerical approximation;
- keep provenance showing which Coxeter/reflection rule justified a reduction.

The Coxeter repository should remain the source of the mathematical notes/implementations; RHS verification should import or depend on a small stable interface instead of duplicating the theory.
