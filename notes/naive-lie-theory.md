# John Stillwell — *Naive Lie Theory*

## Bibliographic note

- John Stillwell, *Naive Lie Theory*, Undergraduate Texts in Mathematics, Springer, 2008.
- Springer describes the book as an undergraduate introduction to Lie theory through the classical matrix groups acting on real, complex, and quaternionic spaces.
- The book deliberately uses elementary calculus and linear algebra before moving into tangent spaces, Lie algebras, topology, and simply connected Lie groups.

Primary source used for this note:
- https://link.springer.com/book/10.1007/978-0-387-78214-0

This file is a research note for Coxeter, not a transcription or substitute for the book.

## Why it belongs in Coxeter

Coxeter groups are discrete reflection groups; Lie groups are continuous symmetry groups. The useful overlap is not merely historical. Reflections and products of reflections give concrete matrix representatives of symmetries, while Lie theory gives a language for the continuous groups in which those symmetries live.

For this repository, Stillwell suggests keeping several levels of structure distinct:

1. the exact geometric operation — reflection, rotation, conjugation;
2. the exact group-theoretic identity or factorization;
3. a matrix representation of that operation;
4. a floating-point realization of the matrix;
5. infinitesimal/tangent information when a continuous family is involved.

That separation matches the repository rule that exact algebraic claims should not be confused with floating-point observations.

## Chapter map and Coxeter-facing notes

### 1. Geometry of complex numbers and quaternions

Complex numbers and unit quaternions give compact representations of low-dimensional rotations. This is a useful place to compare a named geometric operation with its matrix representation.

Potential experiment:
- retain a rotation as an exact operation or a product of reflections;
- separately emit its complex/quaternion representative and its matrix representative;
- verify that all representations agree without throwing away the original construction history.

### 2. Groups

Use this as the elementary group-language baseline: products, inverses, subgroups, homomorphisms, kernels, quotients, and matrix groups.

Compiler-facing point: a rewrite should cite the group law or relation that justified it. A matrix equality discovered numerically is weaker evidence than a rewrite derived from a presentation or certified group identity.

### 3. Generalized rotation groups

This is probably the most immediately relevant chapter for Coxeter. Classical matrix groups turn geometric symmetry into explicit algebra.

Things to track:
- orthogonal groups and orientation-preserving subgroups;
- unitary and symplectic analogues;
- reflections as generators or building blocks for rotations;
- double-cover phenomena in low dimensions.

A useful representation design would let the same transformation carry both a structural tag such as `reflection`/`rotation` and a concrete matrix.

### 4. The exponential map

The exponential map connects infinitesimal generators to continuous group elements.

For Coxeter this should be treated as a different construction path from a finite product of reflections. If two paths produce the same matrix, retain both provenances rather than silently collapsing them.

Numerical matrix exponentials should be observations unless an exact symbolic calculation is available.

### 5. The tangent space

Tangent vectors at the identity provide the linearized form of a Lie group. This is directly suggestive for the repository's vector-verification work: vectors can describe infinitesimal transformations without pretending that they are themselves finite group elements.

Possible use:
- a reflection/rotation object emits a finite transformation representation;
- a smooth path emits a tangent vector or Lie-algebra element;
- verification checks that the declared interpretation matches which sort of object was actually produced.

### 6. Structure of Lie algebras

The Lie bracket records noncommutativity infinitesimally. This gives a second algebraic surface to compare with group multiplication.

Important distinction:
- group product: finite transformations;
- Lie bracket: infinitesimal commutator structure.

Do not let an implementation flatten these into the same generic binary operation merely because both can be encoded with matrices.

### 7. The matrix logarithm

The logarithm is a partial inverse to the exponential map and is potentially useful for recovering a local infinitesimal description from a matrix.

Engineering caution: matrix logarithms have branch issues and numerical instability. Any recovered generator should carry the method and assumptions used to obtain it.

### 8. Topology

Topology explains distinctions invisible to local matrix algebra alone: connected components, loops, coverings, and obstructions.

For a symmetry library, this warns against equating “same local Lie algebra” with “same global group.”

### 9. Simply connected Lie groups

This chapter is relevant to covering groups such as Spin groups. Those are especially important once Coxeter/Dynkin material reaches type D and triality.

A later bridge to the `octonions` branch should explicitly compare the Lie-theoretic Spin(8)/D4 story with Conway–Smith's octonionic triality story.

## Concrete repository ideas

- Add exact constructors for reflections and rotations that retain provenance.
- Add conversion routines to matrices without making the matrix the canonical meaning.
- Add tests that a product of two reflections has the expected rotation action in simple 2D/3D fixtures.
- Add Lie-algebra/tangent-vector representations separately from finite transformations.
- Add checks that distinguish exact symbolic equality from approximate numerical agreement.
- Record exponential/logarithm operations with branch and precision metadata.
- Later compare Coxeter/Dynkin types with the corresponding compact Lie groups and Lie algebras.

## Reading order for this project

If the immediate goal is implementation rather than a linear read, start with:

1. Geometry of complex numbers and quaternions
2. Generalized rotation groups
3. The tangent space
4. Structure of Lie algebras
5. Simply connected Lie groups

Then return to exponential/logarithm and topology as the implementation starts crossing from finite reflection products into continuous-group structure.
