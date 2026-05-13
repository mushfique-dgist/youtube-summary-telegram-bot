from __future__ import annotations

import unittest
from pathlib import Path

from scripts.smoke_demo import build_demo_outputs

REPO_ROOT = Path(__file__).resolve().parents[1]


class SmokeDemoTests(unittest.TestCase):
    def test_demo_outputs_cover_english_and_chinese(self) -> None:
        outputs = build_demo_outputs()

        self.assertEqual(set(outputs), {"English demo", "Chinese demo"})
        self.assertIn("Detected language: en", outputs["English demo"])
        self.assertIn("Detected language: zh", outputs["Chinese demo"])
        self.assertIn("Telegram 机器人", outputs["Chinese demo"])

    def test_demo_outputs_include_reviewer_sections(self) -> None:
        for output in build_demo_outputs().values():
            self.assertIn("Summary", output)
            self.assertIn("Timestamped sections", output)
            self.assertIn("Key takeaways", output)

    def test_static_reviewer_demo_matches_renderer_output(self) -> None:
        reviewer_demo = (REPO_ROOT / "reviewer-demo.md").read_text(encoding="utf-8")

        for title, output in build_demo_outputs().items():
            self.assertIn(f"## {title}", reviewer_demo)
            self.assertIn(output, reviewer_demo)


if __name__ == "__main__":
    unittest.main()
