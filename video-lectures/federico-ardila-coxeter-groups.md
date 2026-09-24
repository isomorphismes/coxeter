# Federico Ardila: Coxeter Groups (2008)

Official course material for Federico Ardila's 2008 Coxeter groups course, taught jointly at San Francisco State University and Universidad de los Andes.

## Links

- YouTube playlist: https://www.youtube.com/playlist?list=PL-XzhVrXIVeSVcV9iRJ4S9WAH1ryq4hTQ
- Course / lecture notes: https://fardila.com/Clase/Coxeter/lectures.html
- Two-page lecture index: https://fardila.com/Clase/coxeterindex.pdf
- Texts and references: https://fardila.com/Clase/Coxeter/texts.html
- Ardila teaching page: https://fardila.com/teaching.html

Ardila's teaching page says these course videos, notes, homework, and related resources were posted for anyone to use freely. I did not find an explicit content license that clearly authorizes republishing the files themselves, so this repository links to the originals rather than mirroring them.

## Especially relevant lectures for this repository

The full course is 42 lectures. The following clusters are particularly close to the compiler/reflection questions here.

- Lectures 1–8: symmetric groups, Coxeter systems, generators/relations, length, exchange/deletion, and the geometric reflection representation.
- **Lecture 8 has a serious mistake that Ardila says is fixed in Lecture 19.** Keep that warning attached to any derived notes.
- Lectures 19–24: geometric representation, roots, reflections, fundamental domain, Coxeter complex.
- Lectures 25–29: root depth, small roots, automaticity, finite automata recognizing reduced words, transfer-matrix counting.
- Lectures 30–35: root systems, Coxeter systems from roots, crystallographic roots, Cartan matrices, crystallographic Coxeter groups.
- Lectures 36–41: bilinear forms, positive-definiteness criterion, classification of finite Coxeter groups.
- Lecture 42: regular polytopes.

## Compiler questions to keep in mind while watching

1. Which algorithms decide whether a word in simple reflections is reduced?
2. Which relations can be applied locally and deterministically?
3. Can the finite automaton for reduced words become a small compiler-side recognizer?
4. Can root/reflection metadata be retained after lowering to vectors or matrices?
5. Which algorithms work for arbitrary Coxeter systems and which silently assume finite or crystallographic type?
