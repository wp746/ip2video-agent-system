#!/usr/bin/env python3
"""Validate an exported IP2Video production package."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

import yaml


REQUIRED_FILES = (
    "final_prompt_pack.md",
    "production_manifest.json",
    "channel_plan.yaml",
    "campaign_calendar.yaml",
    "wechat_content.yaml",
    "wechat_content.md",
    "poster_prompts.yaml",
    "poster_prompts.md",
    "asset_ledger.yaml",
    "shot_contract.yaml",
    "shot_prompts.yaml",
    "shot_prompts.md",
    "negative_prompts.md",
    "qa_report.md",
    "seedance_2_0_15s.txt",
    "seedance_2_5_30s.txt",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate an IP2Video production package.")
    parser.add_argument("package_dir", help="Path to output/<ip>_<duration>_prompt_pack")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    package_dir = Path(args.package_dir)
    if not package_dir.exists():
        raise SystemExit(f"Package directory does not exist: {package_dir}")

    missing = [name for name in REQUIRED_FILES if not (package_dir / name).exists()]
    if missing:
        raise SystemExit(f"Missing required files: {', '.join(missing)}")

    manifest = _load_json(package_dir / "production_manifest.json")
    asset_ledger = _load_yaml(package_dir / "asset_ledger.yaml")
    shot_contract = _load_yaml(package_dir / "shot_contract.yaml")
    shot_prompts = _load_yaml(package_dir / "shot_prompts.yaml")
    wechat_content = _load_yaml(package_dir / "wechat_content.yaml")
    poster_prompts = _load_yaml(package_dir / "poster_prompts.yaml")

    errors = []
    errors.extend(_require_keys(manifest, ["ip", "research", "channels", "ip_bible", "compliance", "reference_duty", "storyboard_signoff", "qa_summary"]))
    if not isinstance(asset_ledger, list) or not asset_ledger:
        errors.append("asset_ledger.yaml must be a non-empty list")
    if not isinstance(shot_contract, list) or not shot_contract:
        errors.append("shot_contract.yaml must be a non-empty list")
    if not isinstance(shot_prompts, dict) or not shot_prompts:
        errors.append("shot_prompts.yaml must be a non-empty mapping")
    elif isinstance(shot_contract, list) and len(shot_prompts) != len(shot_contract):
        errors.append("shot_prompts.yaml count must match shot_contract.yaml count")
    if manifest.get("qa_summary", {}).get("prompt_validation") != "PASS":
        errors.append("prompt_validation must be PASS")
    if not isinstance(wechat_content, dict) or not wechat_content.get("article_draft"):
        errors.append("wechat_content.yaml must include article_draft")
    if not isinstance(poster_prompts, dict) or not poster_prompts:
        errors.append("poster_prompts.yaml must be a non-empty mapping")
    else:
        invalid_ratios = [key for key, item in poster_prompts.items() if ":" not in str(item.get("ratio", ""))]
        if invalid_ratios:
            errors.append(f"poster prompt ratios must preserve colon format: {', '.join(invalid_ratios)}")
    if "story" not in manifest:
        errors.append("production_manifest.json missing key: story")
    if "visual" not in manifest:
        errors.append("production_manifest.json missing key: visual")

    if errors:
        raise SystemExit("Validation failed:\n- " + "\n- ".join(errors))

    print(f"Validated production package: {package_dir}")


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _require_keys(data: dict, keys: Iterable[str]) -> list[str]:
    return [f"production_manifest.json missing key: {key}" for key in keys if key not in data]


if __name__ == "__main__":
    main()
