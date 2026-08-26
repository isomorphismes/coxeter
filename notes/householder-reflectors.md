# Householder reflectors

Householder transformations are the numerical-linear-algebra version of a reflection and are an obvious bridge between this repository and compiler optimization of matrix code.

## Real case

Given a nonzero vector `v`, define

`H(v) = I - 2 vvᵀ / (vᵀv)`.

Then algebraically:

- `H(v)ᵀ = H(v)`;
- `H(v)ᵀ H(v) = I`;
- `H(v)^2 = I`;
- `H(v) v = -v`;
- every vector orthogonal to `v` is fixed.

So `H(v)` is the reflection across the hyperplane perpendicular to `v`.

A compiler does not need to materialize the dense matrix to apply it:

`H(v)x = x - 2 v (vᵀx)/(vᵀv)`.

That representation retains the *reason* the operation is orthogonal and involutive.

## Numerical library representation

LAPACK routines `xLARFG` generate elementary Householder reflectors and represent them compactly as a vector plus a scalar `tau`, rather than as a dense matrix. The real form is

`H = I - tau * u uᵀ`.

Reference implementation/documentation:

- https://www.netlib.org/lapack/explore-html/d8/d0d/group__larfg.html
- https://github.com/Reference-LAPACK/lapack

LAPACK is distributed under a modified BSD license.

Eigen likewise has an explicit `HouseholderSequence` abstraction rather than forcing a product of reflectors to become a matrix immediately:

- https://libeigen.gitlab.io/eigen/docs-nightly/HouseholderSequence_8h_source.html

That source file is MPL-2.0.

## Standard numerical-linear-algebra reading

Householder reflectors are central to QR factorization and to reductions such as Hessenberg and tridiagonal form. Standard references include:

- Trefethen & Bau, *Numerical Linear Algebra*;
- Golub & Van Loan, *Matrix Computations*.

The conceptual point for this repo is more important than a particular implementation: numerical linear algebra already learned long ago not to throw away a reflector's compact structure too early.

## Compiler representation sketch

Instead of lowering immediately to `Matrix n n Float`, retain something like:

```text
Reflector n scalar =
  Householder {
    normal : Vector n scalar,
    scale  : scalar,
    certificate : ReflectionCertificate
  }
```

Then an orthogonal transform can remain:

```text
OrthogonalProgram n scalar = List (Reflector n scalar)
```

with optional stronger metadata:

```text
CoxeterGenerator {
  diagram : DiagramId,
  node    : NodeId,
  reflector : Reflector n scalar
}
```

## Safe simplifications

### Always safe from certified reflection structure

- identical exact reflector twice: `H H → I`;
- applying a reflector through its vector form rather than materializing `H`;
- retain products of Householders in compact form when the consumer can apply them directly.

### Safe only with additional certified group structure

- commuting distinct reflectors;
- braid relations;
- replacing `(H_i H_j)^m` by identity;
- claiming a finite Coxeter type.

Those require information about the relative roots/normals, not merely the fact that each factor happens to be a reflection.

## Floating-point boundary

Do **not** decide that an arbitrary floating-point matrix “is a Householder reflection” merely because numerically `HᵀH ≈ I` and `H² ≈ I`.

Prefer provenance:

- `householder(v)` creates a reflection certificate by construction;
- a proven algebraic rewrite preserves that certificate;
- a generic matrix imported from outside may receive only an *observed approximately orthogonal* annotation unless a stronger proof is available.

This is the same separation needed by RHS verification: exact semantic evidence and numerical discrepancy are different things.

## Relation to Coxeter groups

A sequence of arbitrary Householder reflectors is an orthogonal transformation, but it is **not automatically a word in a useful finite Coxeter system**.

The stronger Coxeter optimization becomes available when the reflector normals are known to be roots/simple roots with certified pairwise Coxeter orders. At that point the compiler can replace expensive matrix reasoning with word/relation reasoning.

This gives a clean ladder:

`generic matrix → certified orthogonal operator → certified reflection → certified Coxeter generator`.

Never move upward on that ladder from a floating-point resemblance alone.
