# Books and longer references

The initial bibliography follows Federico Ardila's Coxeter-groups course bibliography, then adds notes about what is most useful for compiler work.

## Main books

- Anders Björner and Francesco Brenti, *Combinatorics of Coxeter Groups*. Strong candidate for reduced words, Bruhat order, exchange/deletion, and combinatorial algorithms.
- James E. Humphreys, *Reflection Groups and Coxeter Groups*. Best first bridge from literal Euclidean reflections to abstract Coxeter systems. See `humphreys-reflection-groups-and-coxeter-groups.md`.
- Richard Kane, *Reflection Groups and Invariant Theory*. Useful when the compiler-facing question expands from transformations to polynomial invariants.

## Other references named by Ardila

- Marcelo Aguiar and Swapneel Mahajan, *Coxeter Groups and Hopf Algebras*.
- N. Bourbaki, *Lie Groups and Lie Algebras, Chapters 4–6*.
- Michael W. Davis, *The Geometry and Topology of Coxeter Groups*.
- Meinolf Geck and Götz Pfeiffer, *Characters of Finite Coxeter Groups and Iwahori–Hecke Algebras*.
- Larry C. Grove and C. T. Benson, *Finite Reflection Groups*.
- Brian C. Hall, *Lie Groups, Lie Algebras, and Representations*.
- James E. Humphreys, *Introduction to Lie Algebras and Representation Theory*.

Ardila bibliography: https://fardila.com/Clase/Coxeter/texts.html

## Online notes worth retaining as links

- Bill Casselman, CRM Winter School notes on Coxeter groups: https://personal.math.ubc.ca/~cass/coxeter/crm.html
  - Part I: geometry and combinatorics.
  - Part II: word processing — directly interesting for normal forms and compiler rewriting.
- Federico Ardila's notes and lecture index: https://fardila.com/Clase/Coxeter/lectures.html

## Numerical linear algebra references for the Householder side

The standard numerical-linear-algebra path into reflections is Householder QR and related reductions. Useful references include:

- Lloyd N. Trefethen and David Bau III, *Numerical Linear Algebra*.
- Gene H. Golub and Charles F. Van Loan, *Matrix Computations*.

See `../notes/householder-reflectors.md` for the compiler-facing connection.

## Repository policy for books

Do not infer redistribution permission from the existence of a PDF or an Internet Archive/Open Library scan. A book file belongs here only when a license or public-domain status actually permits repository redistribution. Otherwise store bibliographic metadata, lawful source/borrow/preview links, and original notes.
