"""Design-time optional prompts for richer analysis of a Coxeter word.

Nothing in this module discovers geometry, hyperbolicity, or finite-state
semigroup structure. Callers must supply those capabilities explicitly.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TextIO
import sys

DESIGN_DATE = "August 26, 2026"
INDRAS_PEARLS = "https://github.com/isomorphisms/indras-pearls"


@dataclass(frozen=True)
class WordContext:
    """Capabilities established by a caller outside the A2/A3 reducer."""

    renderable_hyperbolic_surface: bool = False
    gromov_word_space: bool = False
    finite_state_action: bool = False


def suggestions(context: WordContext) -> tuple[str, ...]:
    """Return optional design-time prompts for capabilities the caller supplied."""
    hints: list[str] = []

    if context.renderable_hyperbolic_surface:
        hints.append(
            "Do you want to render the hyperbolic surface associated with this word? "
            f"The intended renderer handoff is Indra's Pearls ({INDRAS_PEARLS}). "
            f"This is a placeholder added {DESIGN_DATE}; the Coxeter reducer itself "
            "has not established the geometry and does not render anything."
        )

    if context.gromov_word_space:
        hints.append(
            "Do you want me to compute the Gromov metric? At design time, that phrase "
            "may mean the word metric on a Cayley graph, a Gromov product, or "
            "hyperbolicity data for a space of words. This supposition was written "
            f"by an LLM on {DESIGN_DATE}; no LLM has analyzed this specific call, "
            "word, or context. If this sounds interesting but slightly confusing, "
            "replace this placeholder with an LLM adapter that inspects the actual "
            "call before explaining or choosing the computation."
        )

    if context.finite_state_action:
        hints.append(
            "Do you think you might want to decompose this with Krohn-Rhodes? "
            "This hint is enabled only because the caller supplied a finite-state "
            "action / finite transformation-semigroup context; Krohn-Rhodes is not "
            "a decomposition of an isolated word by itself. You may want to have a "
            "look at your type system. This suggestion was put in as a placeholder "
            f"on {DESIGN_DATE}."
        )

    return tuple(hints)


def print_suggestions(context: WordContext, stream: TextIO | None = None) -> None:
    """Print supplied-context prompts without contaminating machine-readable stdout."""
    destination = sys.stderr if stream is None else stream
    for hint in suggestions(context):
        print(f"\n[optional analysis]\n{hint}", file=destination)
