# James E. Humphreys — *Reflection Groups and Coxeter Groups*

Cambridge Studies in Advanced Mathematics 29. First published 1990; first paperback edition with corrections 1992.

## Legal/source status

Publisher: Cambridge University Press.

- Publisher page: https://www.cambridge.org/core/books/reflection-groups-and-coxeter-groups/2910C1E00877D33A04A512791B6EDD72
- Google Books preview / contents: https://books.google.com/books?id=ODfjmOeNLMUC
- Open Library record: https://openlibrary.org/books/OL1455066M/Reflection_groups_and_coxeter_groups
- Publisher frontmatter: https://assets.cambridge.org/97805214/36137/frontmatter/9780521436137_frontmatter.pdf

Cambridge's frontmatter states © Cambridge University Press 1990 and says reproduction requires permission except for statutory/licensing exceptions. Therefore the book itself is **not mirrored in this repository**. Open Library availability is useful for lawful access but is not evidence of a redistribution license.

## Why this is the book we want

The book starts with concrete finite and affine reflection groups and then abstracts the same structure into Coxeter systems. That is almost exactly the route a compiler experiment should take:

`actual reflection operator → roots/simple reflections → relations → symbolic Coxeter word → reduced/canonical representation → matrix only when needed`

## Chapter-level summaries and compiler relevance

These are original orientation notes, not replacements for the text.

### 1. Finite reflection groups

Builds the concrete vocabulary: roots, positive and simple systems, length, deletion/exchange, longest elements, generators and relations, parabolic subgroups, fundamental domains, and the Coxeter complex.

**Compiler relevance:** this is the core chapter for attaching symbolic meaning to a sequence of reflection calls. Length is a natural optimization cost; deletion/exchange tell us when a generator word is redundant; parabolic subgroups describe computations restricted to a subset of generators.

### 2. Classification of finite reflection groups

Moves from reflection geometry to Coxeter graphs and their bilinear forms, then classifies finite types. It separates crystallographic cases and develops root systems/Weyl groups, including exceptional and noncrystallographic types.

**Compiler relevance:** a finite labeled graph can be treated as a compact relation table. Positive-definiteness/classification tells us when that table describes a finite reflection group and therefore when aggressive finite-group reasoning is justified.

### 3. Polynomial invariants of finite reflection groups

Studies invariant polynomial rings, degrees, Jacobians, Coxeter elements, Coxeter numbers, eigenvalues and exponents.

**Compiler relevance:** not the first implementation slice, but potentially valuable for recognizing quantities that are unchanged by a reflection group. An optimizer could preserve or exploit certified invariants instead of repeatedly recomputing transformed values.

### 4. Affine reflection groups

Introduces affine Weyl groups, alcoves, affine hyperplane arrangements, exchange, Coxeter graphs/extended Dynkin diagrams, and fundamental domains.

**Compiler relevance:** ordinary Householder/Coxeter reflections are linear and fix the origin; affine reflections add translation. This chapter marks the boundary for extending a linear transformation pass to rigid/affine transformations without confusing the two.

### 5. Coxeter groups

Develops the abstract Coxeter-system theory: length, geometric representation, positive/negative roots, parabolics, roots and reflections, strong exchange, Bruhat order, subexpressions, intervals, Poincaré series, and a fundamental domain.

**Compiler relevance:** probably the most important abstract chapter. The group element should be represented by its symbolic word/equivalence class rather than by the matrix product already evaluated. Strong exchange and reduced expressions are exactly the kind of deterministic proof-producing simplification we want.

### 6. Special cases

Studies the bilinear form and its radical and organizes finite, affine, crystallographic, rank-three and hyperbolic Coxeter groups.

**Compiler relevance:** prevents an optimizer from applying a rule outside the class where its assumptions hold. The type/classification should be explicit metadata, not an LLM guess from a matrix.

### 7. Hecke algebras and Kazhdan–Lusztig polynomials

Moves beyond group multiplication into Hecke algebras, R-polynomials, Kazhdan–Lusztig polynomials, cells and representations.

**Compiler relevance:** later work. It is evidence that reduced-word/Bruhat structure carries much richer computable information, but there is no reason to put this in the first transformation optimizer.

### 8. Complements

Surveys additional internal structure, representations, Bruhat-order topics, and further directions.

**Compiler relevance:** bibliography and future-work map rather than a first implementation target.

## First implementation reading order

For the stated compiler goal, read in this order rather than cover-to-cover:

1. Chapter 1: length, deletion/exchange, generators/relations.
2. Chapter 5: abstract geometric representation, roots/reflections, strong exchange, Bruhat order.
3. Chapter 2: Coxeter graphs, bilinear forms, finite/crystallographic classification.
4. Chapter 4 if affine transformations become relevant.
5. Chapters 3, 7, 8 only as later applications demand them.
