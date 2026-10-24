import unittest
from pathlib import Path

from deck.build_deck import _structural_qa


class DeckTests(unittest.TestCase):
    def test_current_draft_has_structural_qa_invariants(self):
        deck = Path(__file__).resolve().parents[1] / "deck/out/Vishwakarma_Stage2_VaaniCore.pptx"
        result = _structural_qa(deck, 18)
        self.assertEqual(result["zip_integrity"], "PASS")
        self.assertEqual(result["slide_count"], 18)
        self.assertEqual(result["forbidden_template_text"], "PASS")


if __name__ == "__main__":
    unittest.main()
