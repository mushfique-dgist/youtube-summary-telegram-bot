from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - dependency is installed in normal setup
    load_dotenv = None


@dataclass(frozen=True)
class ConfigReport:
    ok: bool
    lines: list[str]


def _mask_secret(value: str) -> str:
    if len(value) <= 8:
        return "***"
    return f"{value[:4]}...{value[-4:]}"


def _positive_int(name: str, env: Mapping[str, str], default: str, lines: list[str]) -> bool:
    raw_value = env.get(name, default).strip()
    try:
        value = int(raw_value)
    except ValueError:
        lines.append(f"FAIL {name}: expected a positive integer, got {raw_value!r}")
        return False

    if value <= 0:
        lines.append(f"FAIL {name}: expected a positive integer, got {value}")
        return False

    lines.append(f"OK {name}: {value}")
    return True


def check_config(env: Mapping[str, str] | None = None, *, allow_missing_token: bool = False) -> ConfigReport:
    if env is None:
        if load_dotenv is not None:
            load_dotenv()
        env = os.environ

    lines: list[str] = []
    ok = True

    token = env.get("TELEGRAM_BOT_TOKEN", "").strip()
    if token:
        lines.append(f"OK TELEGRAM_BOT_TOKEN: present ({_mask_secret(token)})")
    elif allow_missing_token:
        lines.append("OK TELEGRAM_BOT_TOKEN: missing, allowed for offline review")
    else:
        lines.append("FAIL TELEGRAM_BOT_TOKEN: required for live Telegram deployment")
        ok = False

    whisper_model = env.get("WHISPER_MODEL", "base").strip() or "base"
    lines.append(f"OK WHISPER_MODEL: {whisper_model}")

    ok = _positive_int("MAX_VIDEO_SECONDS", env, "1800", lines) and ok

    openai_key = env.get("OPENAI_API_KEY", "").strip()
    if openai_key:
        lines.append(f"OK OPENAI_API_KEY: present ({_mask_secret(openai_key)})")
    else:
        lines.append("OK OPENAI_API_KEY: missing, extractive fallback will be used")

    openai_model = env.get("OPENAI_MODEL", "gpt-4o-mini").strip() or "gpt-4o-mini"
    lines.append(f"OK OPENAI_MODEL: {openai_model}")

    work_dir = env.get("WORK_DIR", "/tmp/youtube-summary-bot").strip()
    if not work_dir:
        lines.append("FAIL WORK_DIR: must not be empty")
        ok = False
    else:
        lines.append(f"OK WORK_DIR: {Path(work_dir)}")

    return ConfigReport(ok=ok, lines=lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate deployment config without printing secrets.")
    parser.add_argument(
        "--allow-missing-token",
        action="store_true",
        help="Permit TELEGRAM_BOT_TOKEN to be absent for offline repository review.",
    )
    args = parser.parse_args()

    report = check_config(allow_missing_token=args.allow_missing_token)
    for line in report.lines:
        print(line)

    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
