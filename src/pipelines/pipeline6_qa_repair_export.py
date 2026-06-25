"""Pipeline 6: Produce QA and export readiness summary."""

from __future__ import annotations

from typing import Any, Dict


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    validator = state["PROMPT_VALIDATOR"]
    compliance = state["COMPLIANCE_REVIEW"]
    ledger = state["ASSET_LEDGER"]

    open_issues = []
    if validator["status"] != "PASS":
        open_issues.extend(validator["repair_instructions"])
    if compliance["signoff"] != "PASS_WITH_RULES":
        open_issues.append("Compliance signoff is not ready.")

    export_files = [
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
    ]

    return {
        "pipeline": "QA_REPAIR_EXPORT",
        "status": "READY_TO_EXPORT" if not open_issues else "REPAIR_NEEDED",
        "open_issues": open_issues,
        "export_files": export_files,
        "asset_signoff": ledger["asset_signoff"],
        "qa_summary": {
            "prompt_validation": validator["status"],
            "compliance": compliance["signoff"],
            "asset_coverage": ledger["asset_signoff"]["coverage"],
        },
        "prompt_usage": "Use this report to decide whether to generate assets/video or repair the prompt package.",
    }
