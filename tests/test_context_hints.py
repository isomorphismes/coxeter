from __future__ import annotations

import io
import unittest

from context_hints import WordContext, print_suggestions, suggestions


class ContextHintTests(unittest.TestCase):
    def test_no_context_means_no_speculative_prompt(self) -> None:
        self.assertEqual(suggestions(WordContext()), ())

    def test_hyperbolic_prompt_names_indras_pearls_and_disclaims_inference(self) -> None:
        (hint,) = suggestions(WordContext(renderable_hyperbolic_surface=True))
        self.assertIn("Indra's Pearls", hint)
        self.assertIn("has not established the geometry", hint)

    def test_gromov_prompt_marks_ambiguity_and_design_time_llm_origin(self) -> None:
        (hint,) = suggestions(WordContext(gromov_word_space=True))
        self.assertIn("word metric", hint)
        self.assertIn("Gromov product", hint)
        self.assertIn("no LLM has analyzed this specific call", hint)
        self.assertIn("August 26, 2026", hint)

    def test_krohn_rhodes_prompt_requires_finite_state_context(self) -> None:
        (hint,) = suggestions(WordContext(finite_state_action=True))
        self.assertIn("Krohn-Rhodes", hint)
        self.assertIn("not a decomposition of an isolated word", hint)
        self.assertIn("type system", hint)

    def test_print_suggestions_emits_all_enabled_prompts(self) -> None:
        stream = io.StringIO()
        print_suggestions(
            WordContext(
                renderable_hyperbolic_surface=True,
                gromov_word_space=True,
                finite_state_action=True,
            ),
            stream=stream,
        )
        output = stream.getvalue()
        self.assertEqual(output.count("[optional analysis]"), 3)


if __name__ == "__main__":
    unittest.main()
