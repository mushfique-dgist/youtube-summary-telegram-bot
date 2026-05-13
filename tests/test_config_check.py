from __future__ import annotations

import unittest

from scripts.config_check import check_config


class ConfigCheckTests(unittest.TestCase):
    def test_allows_missing_token_for_offline_review(self) -> None:
        report = check_config({}, allow_missing_token=True)

        self.assertTrue(report.ok)
        self.assertIn("OK TELEGRAM_BOT_TOKEN: missing, allowed for offline review", report.lines)

    def test_requires_token_for_live_deployment(self) -> None:
        report = check_config({}, allow_missing_token=False)

        self.assertFalse(report.ok)
        self.assertIn("FAIL TELEGRAM_BOT_TOKEN: required for live Telegram deployment", report.lines)

    def test_masks_present_secrets(self) -> None:
        report = check_config(
            {
                "TELEGRAM_BOT_TOKEN": "1234567890:secret-token",
                "OPENAI_API_KEY": "sk-test-secret-value",
            },
            allow_missing_token=False,
        )

        text = "\n".join(report.lines)
        self.assertTrue(report.ok)
        self.assertIn("1234...oken", text)
        self.assertIn("sk-t...alue", text)
        self.assertNotIn("1234567890:secret-token", text)
        self.assertNotIn("sk-test-secret-value", text)

    def test_rejects_invalid_numeric_config(self) -> None:
        report = check_config({"TELEGRAM_BOT_TOKEN": "123456:token", "MAX_VIDEO_SECONDS": "zero"})

        self.assertFalse(report.ok)
        self.assertIn("FAIL MAX_VIDEO_SECONDS: expected a positive integer, got 'zero'", report.lines)


if __name__ == "__main__":
    unittest.main()
