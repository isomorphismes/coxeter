# Open-source survey: reflections, Coxeter groups, and verified rewriting

The point of this survey is not to import everything. It is to identify mature implementations that can serve as design references, conformance oracles, or selectively reusable code when licensing and architecture fit.

## 1. SageMath — Coxeter groups and root systems

- Coxeter group docs: https://doc.sagemath.org/html/en/reference/combinat/sage/combinat/root_system/coxeter_group.html
- Matrix/reflection implementation: https://github.com/sagemath/sage/blob/develop/src/sage/groups/matrix_gps/coxeter_group.py
- Root-system package: https://github.com/sagemath/sage/tree/develop/src/sage/combinat/root_system
- License: GPL.

Why it matters:

- constructs a Coxeter group from a Cartan type, Coxeter matrix, or graph;
- has reflection, matrix, permutation, and coxeter3-backed representations;
- exposes roots and reflections;
- already separates abstract Coxeter structure from concrete matrix actions.

**Best use here:** conformance oracle for small exact fixtures and a design reference. Avoid making a compiler runtime depend on Sage.

## 2. coxeter3 / Fokko du Cloux — reduced words and normal forms

- Upstream mirror: https://github.com/tscrim/coxeter
- Sage package description: https://doc.sagemath.org/html/en/reference/spkg/coxeter3.html
- License: GPL.

Capabilities called out by Sage include:

- general Coxeter groups represented through reduced-word combinatorics;
- reduced expressions and normal forms;
- Bruhat order;
- Kazhdan–Lusztig calculations.

This may be the single most directly relevant implementation for the immediate compiler question because it treats **words and their reductions as primary objects**, instead of beginning from dense matrices.

**Study first:** representation of a word, multiplication by a generator, length/descent tests, and normal-form/reduction code.

## 3. CHEVIE / Chevie.jl — reflection groups and representation data

- Current Julia port: https://github.com/jmichel7/Chevie.jl
- License: MIT.

Chevie.jl is a current port of GAP3 CHEVIE and includes infrastructure for permutation groups, signed permutations, integer matrices/lattices, and groups by generators and relations. It retains substantial Coxeter/reflection-group functionality.

**Best use here:** compare reflection/root/group APIs and test exceptional/crystallographic cases after the tiny Coxeter core works.

Because it is MIT licensed, it is a more permissive source for adaptation than GPL code, but any copied implementation should still retain required notices and provenance.

## 4. GAP — general computational group theory

- https://github.com/gap-system/gap
- License: GPL-2.0-or-later.

GAP is much broader than this project, but it is an obvious oracle for finite-group calculations, presentations, subgroup computations, and representations.

**Best use here:** external truth source in tests, not a dependency in the small compiler path.

## 5. CoxIter / CoxIterGAP — hyperbolic Coxeter graphs

- GAP interface: https://github.com/gap-packages/CoxIterGAP

This is useful later if the project moves beyond finite/crystallographic examples. It accepts Coxeter-graph descriptions, including hyperbolic geometry conventions.

**Best use here:** boundary tests showing which assumptions break once the bilinear form is no longer positive definite.

## 6. LAPACK — compact Householder reflectors

- Repository: https://github.com/Reference-LAPACK/lapack
- Householder generator docs: https://www.netlib.org/lapack/explore-html/d8/d0d/group__larfg.html
- License: modified BSD.

`xLARFG` produces an elementary reflector as compact vector/scalar data. This is the production numerical-linear-algebra example of **not materializing a reflection matrix unnecessarily**.

**Best use here:** representation/lowering model and numerical test oracle.

## 7. Eigen — `HouseholderSequence`

- Source: https://libeigen.gitlab.io/eigen/docs-nightly/HouseholderSequence_8h_source.html
- License for this source: MPL-2.0.

Eigen gives a first-class lazy/product representation for sequences of Householder transformations.

**Best use here:** API design reference for keeping an orthogonal transform as a sequence of reflectors until a dense matrix is actually required.

## 8. egg / egglog — equality saturation

- egg: https://github.com/egraphs-good/egg
- egglog: https://github.com/egraphs-good/egglog
- linear-algebra compiler tutorial case study: https://github.com/egraphs-good/egglog-tutorial/tree/main/case-study-linear-algebra-compiler
- License: MIT.

Why it matters:

Coxeter braid relations create many equivalent words, and choosing a shortest/cheapest representative is naturally an equality-saturation problem. egglog rules match modulo equality and support explicit rewrite rules and cost-based extraction.

**Caution:** do not start here. First make a small deterministic reducer with explicit proof records. Then compare an e-graph optimizer against it and require extracted equalities to be replayable as trusted rules.

## 9. TensorRight — verified tensor graph rewrites

- https://github.com/ADAPT-uiuc/TensorRight
- License: Apache-2.0.

TensorRight represents tensor compiler rewrites with preconditions and automatically verifies them, reducing unbounded-rank obligations to finitely many SMT obligations where possible.

This is not group theory, but it is directly relevant to the *verification boundary*: optimizer rewrites should be statements with explicit preconditions and machine-checkable semantics, not folklore transformations.

**Best use here:** design reference for how ai-ci/RHS verification can treat group-theoretic transformations as independently checkable rewrite rules.

## 10. Smaller reflection-group code worth looking at later

- CHAMP complex reflection-group database: https://github.com/ulthiel/Champ
- PyCox (parts of GAP-CHEVIE in Python): https://github.com/geckmf/PyCox

These may be useful for test data or examples, but are not first choices for the core compiler representation.

## What to borrow conceptually

From **LAPACK/Eigen**:
- keep reflector structure compact and lazy.

From **Sage/coxeter3/CHEVIE**:
- make generator words, roots, lengths, descents, and Coxeter matrices explicit objects;
- treat matrix representation as one view of a group element, not its definition.

From **egglog**:
- explore many equivalent words and extract by a transparent cost model.

From **TensorRight**:
- state rewrite preconditions formally and verify the rewrite independently.

From **GAP/Sage**:
- use mature systems as conformance oracles for tiny exact fixtures.

## A practical anti-goal

Do not vendor millions of lines of computer algebra into Idriç merely to simplify a handful of reflection words. Start with the tiny algebraic interface:

```text
Coxeter matrix
+ generator word
+ length/reduction
+ proof of each rewrite
```

Then use the large systems to tell us when our tiny implementation is wrong.
