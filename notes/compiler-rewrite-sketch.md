# Compiler sketch: preserve the group before multiplying the matrices

## Goal

If source code says, in effect,

```text
M4 * M3 * M2 * M1 * x
```

and the compiler knows that `M1...M4` are reflections/rotations belonging to a known generated group, it should not be forced to treat this as four opaque dense matrix multiplications.

The optimizer should retain a symbolic transformation program, use certified group relations to simplify it, and lower to matrices only when necessary.

## Three distinct levels of knowledge

### 1. Matrix facts

Examples:

- dimensions agree;
- matrix is orthogonal/unitary;
- determinant is ±1;
- numerical error bounds.

### 2. Geometric operator facts

Examples:

- this operation was constructed as a reflection across `v⊥`;
- this operation was constructed as a rotation in a specified plane;
- this Householder vector/tau pair is a compact representation of the operator.

### 3. Group-presentation facts

Examples:

- reflector `r` is simple generator 2 of Coxeter system `A3`;
- `r² = e`;
- `(rs)^3 = e`;
- `r` and `t` commute;
- a word has this certified reduced form.

The optimization pass should never manufacture level 3 merely from approximate level-1 measurements.

## IR idea

```text
Transform n scalar
  = DenseMatrix (Matrix n n scalar)
  | Householder (Reflector n scalar)
  | Rotation (PlaneRotation n scalar)
  | CoxeterWord DiagramId (List NodeId)
  | Compose (Transform n scalar) (Transform n scalar)
  | Identity
```

A later implementation can use a more typed representation. The important design decision is that `CoxeterWord` and `Householder` survive long enough to be optimized.

## Coxeter relation table

For a Coxeter system with generators `S = {s_i}` and Coxeter matrix `m`:

- `m[i,i] = 1`;
- `m[i,j] = m[j,i]`;
- `s_i² = e`;
- for finite `m[i,j]`, `(s_i s_j)^m[i,j] = e`;
- equivalently the alternating braid words of length `m[i,j]` are equal;
- `m[i,j] = 2` means the generators commute.

This is tiny data compared with repeatedly comparing matrices.

## First deterministic rewrite rules

These should emit proof records.

```text
cancel-involution:
  ... s s ...  →  ... ...
  evidence: generator s is certified involutive

commute-unconnected:
  ... s t ...  ↔  ... t s ...
  precondition: m[s,t] = 2

braid:
  alternate(s,t,m) ↔ alternate(t,s,m)
  precondition: m[s,t] = m < ∞
```

Braid rewrites alone need an orientation/canonicalization strategy to avoid loops. Do not implement them as unrestricted bidirectional term rewriting and hope for convergence.

## Reduced words

The compiler ultimately wants a deterministic function such as

```text
reduce : CoxeterSystem → Word → (ReducedWord, Proof input ≡ output)
```

rather than a bag of ad-hoc substitutions.

Candidates to study:

- exchange/deletion algorithms;
- root/sign tests for whether right multiplication increases or decreases length;
- normal-form algorithms from coxeter3;
- finite automata for reduced words / small roots, as in Ardila's later lectures;
- equality saturation with a cost model, provided the extracted result is accompanied by trustworthy rewrite evidence.

## Example: A2

Generators `s,t` satisfy

```text
s² = e
t² = e
sts = tst
```

Suppose source produces:

```text
s * t * s * t * s * t
```

Since `(st)^3 = e`, the whole transformation is identity. A matrix-first compiler would likely perform several multiplications before discovering this, if it discovered it at all. A group-aware pass can return `Identity` with a short proof.

## Example: commuting reflections in a larger diagram

If two nodes are not connected in a Coxeter diagram, `m_ij = 2`, so their simple reflections commute. The compiler may reorder them to expose adjacent equal generators and cancel them.

For example, if `s` commutes with `u`:

```text
s u s
→ u s s
→ u
```

The first step is justified by `m[s,u] = 2`; the second by involution.

## Pair of reflections as rotation

Two Euclidean reflections compose to a rotation in the relevant 2-plane by twice the angle between their reflecting hyperplanes/normals, with the orthogonal complement fixed.

That gives two useful representations of the same program:

```text
Reflection(a) ∘ Reflection(b)
```

and

```text
PlaneRotation(plane(a,b), angle)
```

Do not necessarily replace one by the other. Keep both as equivalent views if useful. The Coxeter relation becomes finite precisely when the angle data gives a finite order.

## Householder lowering

A sequence of Householders should normally stay as compact vectors/scalars until a consumer demands a dense matrix. Applying k reflectors to a vector can be cheaper and structurally clearer than first forming their dense product.

If the sequence is also a certified Coxeter word, simplify the word *before* applying any reflectors.

## Equality saturation is relevant, but proof matters

`egg`/`egglog` are relevant because they maintain many equivalent expressions and extract a low-cost representative. Coxeter braid relations naturally create many equivalent words.

A possible flow:

```text
certified Coxeter word
→ insert into equality structure
→ saturate only with relations justified by this diagram
→ extract minimum-cost word
→ replay exact rule sequence
→ emit proof/evidence ledger
```

The replay step matters for RHS verification. “The e-graph says they are equal” is not a sufficient external explanation unless the equality can be traced to explicit rules and preconditions.

## Cost model

Start stupid and visible:

```text
cost Identity                 = 0
cost CoxeterGenerator         = 1
cost HouseholderApply         = O(n)
cost DenseMatrixVector        = O(n²)
cost DenseMatrixMatrix        = O(n³)
```

Then add architecture/backend-specific costs later. The algebraic reducer should not need to know ARM instruction timing to prove `(st)^3 = e`.

## Proof/evidence record

Every simplification should be replayable:

```text
RewriteEvidence = {
  before,
  after,
  rule,
  diagram_or_certificate,
  exact_preconditions,
  numeric_observations_optional
}
```

This can feed RHS verification directly. A function named `rotateQuarterCircle`, for example, could be checked against both its produced vector action and its symbolic group/angle meaning when available.

## Important limitation

The orthogonal group is much larger than any one finite Coxeter group. The theorem that orthogonal transformations can be expressed as products of reflections does **not** imply that arbitrary program rotations can be reduced using a fixed finite Coxeter presentation.

The compiler may use Coxeter relations only when it knows which generators/system the operations inhabit. Otherwise retain the weaker facts: reflection, orthogonal transformation, rotation, etc.

## Suggested implementation order

1. Introduce `Identity`, `Householder`, `Compose`, and exact reflection certificates.
2. Cancel identical certified involutions.
3. Add `CoxeterSystem`/`CoxeterWord` with a matrix of pairwise orders.
4. Implement and test A2, A3, B2/I2(m) fixtures exhaustively.
5. Add reduced-word/length machinery and proof replay.
6. Compare against Sage and coxeter3 as conformance oracles, without making either a runtime dependency.
7. Experiment with equality saturation only after the simple deterministic reducer is trustworthy.
8. Feed rewrite evidence to ai-ci and RHS verification.
