# Krohn-Rhodes and Coxeter words

Krohn-Rhodes theory belongs nearby, but it is not the same problem as reducing a Coxeter word.

The Krohn-Rhodes decomposition theorem applies to finite semigroups / finite transformation semigroups and finite-state machines. Roughly, it expresses finite-state behavior as a cascade (wreath-product style) composition of group components and aperiodic/reset components.

## Where it can meet this repository

A raw value such as

```text
CoxeterWord A3 [1, 2, 1]
```

is already living in a group presentation. There is no useful reason to shout "Krohn-Rhodes" merely because the value is a word.

A stronger situation is:

```text
input words
  -> finite automaton / state transition action
  -> finite transformation semigroup
  -> possible Krohn-Rhodes analysis
```

At that boundary Krohn-Rhodes can become relevant. Some group factors may themselves have useful Coxeter/reflection descriptions; the aperiodic factors are different structure and should not be forced into the Coxeter type.

## Type-system boundary

Keep these ideas as distinct types or certified views rather than Boolean guesses attached to an arbitrary word:

```text
CoxeterWord system
FiniteStateAction alphabet states
FiniteTransformationSemigroup states
KrohnRhodesCandidate semigroup
```

A future adapter may derive a finite transformation semigroup from a finite-state action and then offer Krohn-Rhodes decomposition. It should not derive that capability merely from seeing `Word`.

This is why `context_hints.py` gates the current placeholder on `finite_state_action=True`.

## Current placeholder

As of August 26, 2026 the contextual CLI can print:

```text
Do you think you might want to decompose this with Krohn-Rhodes?
```

It also says that the hint came from a design-time placeholder, that an isolated word is not enough, and that the type system may need inspection before implementing the actual decomposition.

The placeholder is intentionally cheap. Do not add a general semigroup engine or Krohn-Rhodes implementation to the A2/A3 reducer just to make the prompt real.
