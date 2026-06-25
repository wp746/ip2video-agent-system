"""Pipeline 3B: Create an asset ledger and reference-duty split."""

from __future__ import annotations

from typing import Any, Dict, List


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    brief = state["INPUT_COMPILER"]["compiled_brief"]
    visual = state["VISUAL_DESIGN"]
    ip_bible = state["IP_BIBLE_BUILDER"]["ip_bible"]
    prompts = visual["image_prompts"]

    assets = [
        _asset("CHAR-001", "identity_reference", "character_asset_board", prompts["character_asset_board_cn"], 1),
        _asset("SCENE-001", "world_reference", "scene_9_grid", prompts["scene_9_grid_cn"], 2),
        _asset("PROP-001", "product_prop_reference", "prop_board", prompts["prop_board_cn"], 2),
        _asset("BOARD-001", "execution_reference", "storyboard_board", prompts["storyboard_board_cn"], 1),
    ]

    return {
        "pipeline": "ASSET_LEDGER",
        "asset_ledger": assets,
        "reference_duty": {
            "identity_lock": ["CHAR-001"],
            "world_lock": ["SCENE-001"],
            "product_lock": ["PROP-001"] if brief.get("product") else [],
            "execution_state": ["BOARD-001"],
        },
        "source_board_exclusion": [
            "Identity boards define who the IP is; do not copy their white background into video scenes.",
            "Execution storyboard defines action and layout; do not use it to mutate character identity.",
        ],
        "asset_signoff": {
            "required_before_video": ["CHAR-001", "BOARD-001"],
            "coverage": "PASS",
            "identity_anchors": ip_bible["visual_lock"]["must_keep"],
        },
        "prompt_usage": "Use asset ids in storyboard and final prompts to separate identity references from execution references.",
    }


def _asset(asset_id: str, duty: str, name: str, prompt: str, priority: int) -> Dict[str, Any]:
    return {
        "asset_id": asset_id,
        "duty": duty,
        "name": name,
        "prompt": prompt,
        "priority": priority,
        "status": "TO_GENERATE",
    }
