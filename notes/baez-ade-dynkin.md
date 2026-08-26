# John Baez on ADE, Coxeter diagrams, and Dynkin diagrams

Baez himself gives a useful map of this material in *This Week's Finds* Week 230. He points back to Weeks 62–65 for the original Dynkin/ADE discussion, Weeks 178–182 for geometry, and Weeks 186–187 for q-deformation/combinatorics. Week 230 then adds quivers, singularities, Hall algebras, and quantum groups.

This note follows that map rather than searching for the word “Dynkin” in unrelated Baez writing.

## Core sequence: Weeks 62–65

### Week 62 — finite reflection groups and Coxeter diagrams

https://math.ucr.edu/home/baez/week62.html

This is the most directly useful post for the compiler project.

- A reflection is attached to a vector/hyperplane.
- Two reflections compose to a rotation through twice the angle between their normals.
- If the angle is π/n, the product has finite order n.
- A Coxeter diagram records generators and these pairwise orders compactly.
- Each generator is an involution: `s² = 1`.
- An edge labeled `m` means `(s t)^m = 1`; no edge means `m = 2`, hence the generators commute.
- The finite irreducible families are classified by the familiar A, B, D, E, F, G, H, I diagrams.

**Compiler takeaway:** a diagram can be a tiny static relation table for a large family of matrix identities. If a matrix operation carries a certificate saying it is generator `s_i`, the compiler can reason about the word before evaluating the matrices.

### Week 63 — crystallographic condition and the road to Dynkin diagrams

https://math.ucr.edu/home/baez/week63.html

Baez restricts finite reflection groups to those preserving a lattice. This removes H and most I types and leads toward Weyl groups. Root *lengths*, not just angles, now matter. The B-type Coxeter diagram admits two root-length choices, which become the B and C Dynkin diagrams.

**Compiler takeaway:** a Coxeter matrix/graph and a Dynkin/Cartan description are related but not identical data. Do not erase root-length/orientation information when it matters, and do not invent it when only Coxeter relations are known.

### Week 64 — Dynkin diagrams and simple Lie algebras

https://math.ucr.edu/home/baez/week64.html

The Dynkin diagram refines the crystallographic Coxeter information enough to classify simple Lie algebras. A, B, C, D are classical families; E, F, G are exceptional. The same diagram controls roots, Weyl reflections, and Lie-theoretic structure.

**Compiler takeaway:** separate layers:

1. unlabeled transformation graph / generic group facts;
2. Coxeter matrix and reflection relations;
3. Cartan/Dynkin data when crystallographic root data is certified;
4. Lie-algebra data only when the program actually needs it.

### Week 65 — ADE lattices and McKay correspondence

https://math.ucr.edu/home/baez/week65.html

Baez concentrates on simply-laced A, D, E. He gives concrete lattice models for A_n, D_n and E_8, then explains the McKay correspondence: finite subgroups of SU(2), their irreducible representations, and tensoring by the defining 2-dimensional representation produce extended ADE diagrams.

**Compiler takeaway:** the diagram is not merely a picture of a group presentation. It can be a shared index connecting several representations of the same structure: roots, reflection generators, lattices, representations, and graphs. That suggests keeping a stable diagram/node identity and attaching multiple certified views rather than converting destructively from one representation to another.

## Geometry sequence: Weeks 178–182

### Week 178 — nodes as geometric figure types

https://math.ucr.edu/home/baez/week178.html

For a complex simple Lie group G, dots in the Dynkin diagram correspond to distinguished types of geometric figures. Their spaces are homogeneous spaces `G/P`, with `P` a maximal parabolic subgroup. Edges encode basic incidence relationships.

**Compiler takeaway:** selecting nodes/subgraphs has mathematical meaning. A subset of generators is not arbitrary bookkeeping; it naturally points toward a parabolic subsystem/subgroup.

### Week 179 — transitional geometry material

https://math.ucr.edu/home/baez/week179.html

Baez lists Week 179 as part of his geometry sequence in Week 230, but this post does not materially develop Dynkin diagrams themselves. Keep it in the reading chain, but it is not a first implementation source.

### Week 180 — Dynkin nodes and fundamental representations

https://math.ucr.edu/home/baez/week180.html

Baez walks through Spin(n), low-dimensional coincidences such as Spin(3) ≅ SU(2), and the fundamental representations attached to Dynkin nodes. D4 triality is visible as symmetry of the diagram.

**Compiler takeaway:** diagram automorphisms can represent genuine equivalences/symmetries. If the compiler ever canonicalizes named nodes, it must not accidentally destroy a meaningful outer automorphism.

### Week 181 — subsets of nodes, flags, parabolics

https://math.ucr.edu/home/baez/week181.html

A subset of Dynkin nodes corresponds to a flag type and a parabolic subgroup. A single selected node gives a Grassmannian/fundamental representation. Baez notes that some dimensions depend only on the underlying reflection group, so B_n and C_n can agree after forgetting arrow direction.

**Compiler takeaway:** explicitly record which layer a rewrite uses. A Coxeter-level rewrite may legally forget Dynkin arrow direction; a root-length-sensitive rewrite may not.

### Week 182 — ADE from a positivity / Egyptian-fraction boundary

https://math.ucr.edu/home/baez/week182.html

Baez relates the classification of certain simply-laced diagrams to the same inequality that separates spherical, Euclidean and hyperbolic triangle/tiling behavior. For a Y-shaped simply-laced diagram, positivity reduces to an inequality of the form `1/k + 1/n + 1/m > 1`; equality gives the affine boundary and the opposite inequality leads toward hyperbolic Kac–Moody behavior.

**Compiler takeaway:** classification can often be reduced to small exact arithmetic on graph metadata. Prefer exact integer/rational predicates like these to floating-point eigenvalue guesses when a symbolic graph is available.

## q/combinatorics: Weeks 186–187

### Week 186

https://math.ucr.edu/home/baez/week186.html

A Dynkin diagram gives a Coxeter group; the Coxeter group acts through reflections, has a Coxeter complex, and supports a q-polynomial story. This is another example of one finite graph driving several derived structures.

### Week 187

https://math.ucr.edu/home/baez/week187.html

Baez draws the pipeline explicitly:

`Dynkin diagram → Coxeter group → Coxeter complex`

and, after choosing a field,

`Dynkin diagram → simple algebraic group → flag variety`.

The two routes meet in q-polynomials; the Coxeter result behaves like the `q = 1` specialization of finite-field formulas.

**Compiler takeaway:** build transformations as derived views from a common symbolic source. Do not make matrices the one representation that everything else has to rediscover.

## Week 230 — ADE reappears in quivers, singularities, Hall algebras

https://math.ucr.edu/home/baez/week230.html

Baez reviews ADE as a classification of:

- suitable integral root lattices;
- simply-laced semisimple Lie groups;
- finite subgroups associated with 3d rotations / SU(2) via McKay;
- simple singularities;
- quivers of finite representation type.

He then explains Ringel's result connecting Hall algebras of ADE quivers to quantum groups.

**Compiler takeaway:** a Dynkin diagram is useful precisely because it is a compact invariant that survives changes of representation. That is the design principle worth stealing: recognize structure once, retain its identity, and let multiple lowering/analysis passes consume it.

## Later revisit

Week 267 revisits the spherical/affine/hyperbolic and McKay/Egyptian-fraction picture:
https://math.ucr.edu/home/baez/week267.html

## Minimal facts worth making executable

For Coxeter generators `s_i`:

- `s_i s_i = e`.
- `m_ii = 1`.
- `m_ij = m_ji`.
- `(s_i s_j)^(m_ij) = e` when `m_ij` is finite.
- `m_ij = 2` means `s_i` and `s_j` commute.
- the braid relation has `m_ij` alternating factors on each side.

For Dynkin data, add a Cartan matrix/root-length layer instead of overloading the Coxeter matrix.

These facts are small enough to encode directly, test exhaustively for small diagrams, and attach proof records to each compiler rewrite.
