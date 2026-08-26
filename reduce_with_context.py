"""A thin CLI around reducer.py that prints optional cross-project prompts.

The exact A2/A3 reducer stays untouched. These prompts are deliberately driven
by caller-supplied context rather than inferred from a small Coxeter word.
"""

from __future__ import annotations

import argparse
import json
from typing import Sequence

from context_hints import WordContext, print_suggestions
from reducer import reduce_word


def _parse_type(value: str) -> int:
    normalized = value.strip().upper()
    if normalized not in {"A2", "A3"}:
        raise argparse.ArgumentTypeError("type must be A2 or A3")
    return int(normalized[1])


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Reduce an A2/A3 word, then print optional design-time analysis prompts "
            "for capabilities supplied by the caller."
        )
    )
    parser.add_argument(
        "--hyperbolic-surface",
        action="store_true",
        help="caller has established an associated renderable hyperbolic surface",
    )
    parser.add_argument(
        "--gromov-word-space",
        action="store_true",
        help="caller has established a word/Cayley-space context worth metric analysis",
    )
    parser.add_argument(
        "--finite-state-action",
        action="store_true",
        help="caller has established a finite automaton/transformation-semigroup view",
    )
    parser.add_argument("type", type=_parse_type, metavar="A2|A3")
    parser.add_argument("generators", nargs="*", type=int)
    args = parser.parse_args(argv)

    reduction = reduce_word(args.type, args.generators)
    print(json.dumps(reduction.as_dict(), indent=2))

    print_suggestions(
        WordContext(
            renderable_hyperbolic_surface=args.hyperbolic_surface,
            gromov_word_space=args.gromov_word_space,
            finite_state_action=args.finite_state_action,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
