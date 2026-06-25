#!/usr/bin/env python3
"""Command line entry for the IP2Video agent system."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict

import yaml

from src.core.orchestrator import Orchestrator
from src.utils.validator import validate_input


def load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an IP2Video AIGC prompt package.")
    parser.add_argument("--input", required=True, help="Path to an input YAML brief.")
    parser.add_argument("--config", default="config/default_config.yaml", help="Path to runtime config YAML.")
    parser.add_argument("--output", default=None, help="Optional output Markdown path.")
    parser.add_argument("--template-id", default=None, help="Override style template id, such as MED-A.")
    parser.add_argument("--duration", default=None, choices=["15s", "30s"], help="Override target duration.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path.cwd()
    config = load_yaml(root / args.config)
    request = load_yaml(root / args.input)

    if args.template_id:
        request.setdefault("request", {})["style_template_id"] = args.template_id
    if args.duration:
        request.setdefault("ip_input", {})["duration"] = args.duration

    validate_input(request)
    orchestrator = Orchestrator(root=root, config=config)
    output_path = orchestrator.run(request, output_path=args.output)
    print(f"Generated: {output_path}")


if __name__ == "__main__":
    main()
