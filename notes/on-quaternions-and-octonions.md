# John H. Conway and Derek A. Smith — *On Quaternions and Octonions*

## Bibliographic note

- John H. Conway and Derek A. Smith, *On Quaternions and Octonions: Their Geometry, Arithmetic, and Symmetry*, A K Peters, 2003.
- The book develops complex numbers, quaternions, and octonions through geometry, finite symmetry groups, arithmetic, and exceptional structures.
- The publisher's contents include Coxeter notation for polyhedral groups, Hurwitz integral quaternions, composition algebras, Moufang loops, Spin(8) and triality, the E8 lattice, octonion automorphisms, and the octonion projective plane.

Primary sources used for this note:
- https://www.routledge.com/On-Quaternions-and-Octonions/Conway-Smith/p/book/9781568811345
- https://books.google.com/books/about/On_Quaternions_and_Octonions.html?id=1UBZDwAAQBAJ

This file is a research note for Coxeter, not a transcription or substitute for the book.

## Why it belongs in Coxeter

This book is unusually close to the intended scope of the repository. It connects explicit multiplication laws to geometric transformations and then to finite groups, Coxeter notation, lattices, Spin groups, Dynkin-type phenomena, and exceptional symmetry.

It also supplies a valuable negative lesson for algebraic rewriting: octonion multiplication is nonassociative. A compiler or simplifier that treats every multiplication-like operation as associative will silently destroy meaning.

The octonion work should therefore preserve:

1. operand order;
2. parenthesization;
3. the exact identity used for any reassociation;
4. the subalgebra in which a simplification is valid;
5. whether a claim is exact algebra or numerical evidence.

## Part I — Complex numbers

The opening material treats complex numbers geometrically and connects them with two-dimensional rotations, reflections, finite subgroups, and integer lattices.

Coxeter-facing point: this gives a low-dimensional test bed in which every operation can be checked visually, algebraically, and as a matrix.

Potential fixtures:
- reflection in a line;
- composition of two reflections as a rotation;
- cyclic and dihedral symmetry groups;
- Gaussian-integer lattice symmetries.

These should become the easy cases against which later quaternionic and octonionic machinery is tested.

## Part II — Quaternions

### Quaternions and 3-dimensional groups

Unit quaternions encode 3D rotations and expose the double-cover relationship with SO(3). The book also uses them to enumerate finite rotation groups.

Repository relevance:
- represent a rotation independently of its quaternion or matrix encoding;
- keep the 2-to-1 cover visible rather than pretending a quaternion and a rotation are literally the same object;
- compare polyhedral symmetry groups with their binary lifts.

### Quaternions and 4-dimensional groups

The table of contents explicitly includes Coxeter's notation for polyhedral groups. This should be harvested as a notation/interoperability note rather than immediately copied into an API.

Potential task:
- make a small concordance among Coxeter notation, conventional group names, and concrete quaternionic actions;
- test whether a generated action has the group order and relations claimed by its name.

### Hurwitz integral quaternions

The Hurwitz integers add arithmetic and factorization to quaternionic geometry.

This is useful because it provides exact discrete data inside a continuous-looking algebra. Exact arithmetic here can serve as a reference implementation against which floating-point quaternion code is checked.

## Part III — Octonions

### Composition algebras

The progression R, C, H, O makes the dimensions 1, 2, 4, 8 structurally meaningful rather than accidental. Norm composition is central.

Potential invariant:

`norm(x * y) = norm(x) * norm(y)`

For exact test fixtures this is stronger than checking coordinates one by one, although coordinate equality should still be available as evidence.

### Nonassociativity, alternativity, and diassociativity

Octonion multiplication is nonassociative, but two generated elements lie in an associative subalgebra. Conway and Smith exploit this through diassociativity and then Moufang identities.

This matters directly for a compiler-facing algebra package:

- `(a*b)*c` and `a*(b*c)` must remain distinct syntax trees;
- reassociation must never be a generic multiplication optimization;
- an identity such as a Moufang law must be represented as the reason a particular rewrite is valid;
- simplification inside a certified quaternion subalgebra may use stronger laws than simplification in the full octonions.

This is a good stress test for the broader “say what you mean, mean what you say” philosophy: the operator name `*` alone does not imply associativity.

### Moufang loops

The unit octonions do not form a group under multiplication because associativity fails, but they do form a Moufang loop.

Repository design consequence: do not force every symmetry-like algebraic object into a `Group` interface. A hierarchy should distinguish at least magma/loop/group-like law sets or, better, attach individually certified laws rather than assuming a large bundle of them.

### Octonions and 8-dimensional geometry

This is one of the most important sections for Coxeter. The book develops isotopies, SO(8), the Spin group, and triality.

Triality is the striking symmetry associated with Spin(8) and Dynkin diagram D4. That gives a direct bridge among:
- octonion multiplication;
- 8-dimensional geometry;
- Spin(8);
- D4;
- automorphisms/permutations of the three 8-dimensional representations.

This deserves a later dedicated experiment rather than only prose notes.

### Octavian integers and E8

The integral octonions are tied to the E8 lattice. The book's table of contents explicitly identifies the E8 lattice in the construction of the Octavian integers.

This is probably the strongest direct bridge from octonions into a Coxeter/root-system repository.

Possible future work:
- encode E8 roots exactly;
- compare an E8 root-system implementation with the norm-one/integral-octonion descriptions used in the literature;
- generate reflections in E8 roots and verify Coxeter relations exactly;
- compare alternative coordinate systems without treating one set of coordinates as canonical meaning.

### Automorphisms of the octonions

The automorphism group of the octonions is the exceptional Lie group G2. That creates another bridge from a concrete algebra to an exceptional Lie group/root system.

Potential project:
- begin with automorphisms preserving the octonion product;
- separately characterize the G2 root system;
- test the relationship rather than identifying the two merely by naming convention.

### Octonion projective plane and exceptional Lie groups

The final material connects the octonion projective plane with exceptional Lie groups and Freudenthal's magic square.

This should be treated as a roadmap toward the exceptional groups, not as an immediate implementation requirement.

## Concrete repository ideas

- Implement an octonion value type whose multiplication syntax preserves parentheses.
- Add exact multiplication-table fixtures before adding floating-point implementations.
- Add tests for conjugation, norm composition, inverses where defined, alternativity, and selected Moufang identities.
- Add explicit negative tests showing generic associativity is false.
- Add quaternion-subalgebra detection or certification so associative rewrites can be scoped safely.
- Build a small Spin(8)/D4/triality research note and executable fixture.
- Add an E8 root-system fixture and compare it with an integral-octonion construction.
- Add a G2 bridge: octonion automorphisms versus the G2 root system.
- Record Coxeter's notation for finite quaternionic/polyhedral groups alongside modern names.

## Suggested reading order for this project

For immediate Coxeter work:

1. Quaternions and 3-dimensional groups
2. Quaternions and 4-dimensional groups
3. Composition algebras
4. Moufang loops
5. Octonions and 8-dimensional geometry
6. Octavian integers / E8
7. Automorphisms and subrings of the octonions
8. Octonion projective plane

The arithmetic chapters on Hurwitz and Octavian integers should move earlier if exact discrete test fixtures become a priority.
