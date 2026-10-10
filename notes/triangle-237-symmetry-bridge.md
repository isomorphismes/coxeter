# The infinite Coxeter group `[2,3,7]`, an exact finite quotient, and the Klein quartic

The runnable [Conway `*237` experiment](https://github.com/isomorphismes/Conway/tree/main/hyperbolic237)
provides two different representations of the same triangle-group generators:

1. Geometric reflections of a Poincaré-disk Schwarz triangle of angles
   π/2, π/3, π/7. Floating-point coordinates are for geometric display.
2. **Exact matrices** in PGL(2,F7), a finite quotient of the **infinite**
   hyperbolic Coxeter reflection group. The quotient identifies 336 projective
   group elements and its orientation-preserving PSL(2,7) subgroup has 168.

Let r0 reflect AB, r1 reflect AC, and r2 reflect BC, where
A=π/2, B=π/3, C=π/7. Then

```text
r0² = r1² = r2² = 1
(r0 r1)² = (r0 r2)³ = (r1 r2)⁷ = 1

Coxeter matrix = [[1,2,3],[2,1,7],[3,7,1]]
```

An exact representation, computed in `Conway/hyperbolic237/finite-quotient.mjs`,
uses

```text
U = [1 1; 0 1]        order 7 in PSL(2,7)
V = [0 -1; 1 0]       order 2 in PSL(2,7)
D = [-1 0; 0 1]       determinant nonsquare modulo 7

r0 -> V D
r1 -> D
r2 -> D U
```

Thus r0r1 goes to V, r0r2 to VU, and r1r2 to U, of orders 2,3,7.
The exact group order and quotient map combinatorics are checked in the
Conway test suite; no floating-point comparison establishes these relations.

## Exact equality in the infinite group: Tits matrices

The next Conway stage implements an independent faithful representation of
the infinite `[2,3,7]` Coxeter group in
[`tits-representation.mjs`](https://github.com/isomorphismes/Conway/blob/experiment/klein-237-finite-quotient-20261009/hyperbolic237/tits-representation.mjs).
Set `t=2cos(pi/7)` with `t^3-t^2-2t+1=0`; integral 3x3 reflection
matrices over `Z[t]` have **exact** BigInt arithmetic. The faithfulness of
Tits' geometric representation makes equality of these matrices a sound
word-equality oracle for this Coxeter group (unlike equality in its finite
quotient). This is **not** a reduction algorithm or an extracted
relation-by-relation replay certificate. In particular, retaining only the
PGL(2,7) label is insufficient to choose adjacent chamber representatives.

The [fundamental polygon](https://github.com/isomorphismes/Conway/blob/experiment/klein-237-finite-quotient-20261009/hyperbolic237/FUNDAMENTAL-POLYGON.md)
uses Tits matrix equality to identify 460 truly shared internal edges among
336 distinct representative triangles, and generates 44 explicit kernel
identifications for the remaining 88 boundary sides. The exact results
recover genus 3 without a floating-point equality test.

## What this means for the reducer

The existing [`reducer.py`](../reducer.py) deliberately reduces finite
**A2/A3** words only. A `[2,3,7]` word is not a type-A word, and pretending
that a 336-element quotient is the infinite group would introduce unsound
reductions: distinct infinite group words can have the same PGL(2,7) image.

What *is* sound: expose the ordered Coxeter matrix and permit only the
presentation's relations as replayable rewrite steps. For every step, keep
`before`, `after`, generator indices, start index, and m_ij. The finite quotient
is then a useful **necessary-condition oracle**: unequal finite images prove
two words are different in the Coxeter group, but equal finite images do not
prove group equality.

The `Conway` integration needs a boundary like:

```text
CoxeterPresentation / GeneratorWord / RewriteEvidence
    -> exact PGL(2,F7) quotient evaluator
    -> optional geometric Poincaré reflection evaluator
```

An Idriç realization should type an action on the *hyperbolic plane* rather
than silently reuse Euclidean `Vector` for arbitrary points. Separate affine
points, tangent vectors, hyperbolic isometries, and Coxeter generator words.
A relation proof belongs to the algebraic layer; drawing error bounds belong
to the numerical layer.

## Relation to the Klein quartic

The kernel of the quotient on the orientation-preserving triangle group is
torsion-free and defines a genus-three surface. Its regular `{7,3}` map has
24 faces, 84 edges, and 56 vertices. A 24-heptagon coloring can be obtained
from right cosets of `<r1,r2>` (dihedral order 14) in PGL(2,7).

See [Klein-quartic](https://github.com/isomorphismes/klein-quartic) for the
surface model and visualization lineage. Thanks to **Chaim Goodman-Strauss**,
**Vladimir Bulatov**, and **Scott Vorthmann** for SymmHub;
**John Horton Conway**, **William Thurston**, and **Adam A. Deaton** for the
orbifold framework; and **Jacques Tits**, **James E. Humphreys**, **Felix Klein**, **Greg Egan**, and **Tim Hutton** for
the curve, explanations, and visual constructions. The new finite-field
implementation is independent of their source code.
