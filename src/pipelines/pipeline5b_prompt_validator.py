"""Pipeline 5B: Validate prompt completeness and production constraints."""

from __future__ import annotations

from typing import Any, Dict, List


REQUIRED_PROMPT_TERMS = ("character", "Story", "Visual style", "Shot plan", "Keep", "Do not")


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    prompts = state["PROMPT_GENERATION"]
    compliance = state["COMPLIANCE_REVIEW"]
    storyboard = state["STORYBOARD_CONTRACT"]
    visual = state["VISUAL_DESIGN"]
    ip_bible = state["IP_BIBLE_BUILDER"]["ip_bible"]
    asset_ledger = state["ASSET_LEDGER"]

    validations = {
        "seedance_20_15s": _validate_prompt(prompts["seedance_20_15s"]),
        "seedance_25_30s": _validate_prompt(prompts["seedance_25_30s"]),
    }
    missing_rules = _missing_compliance_rules(prompts, compliance["hard_rules"])
    anchor_coverage = _anchor_coverage(ip_bible["visual_lock"]["must_keep"], prompts, visual)
    reference_validation = _reference_validation(asset_ledger, storyboard)
    shot_coverage = len(storyboard["shot_contract"])
    shot_prompt_coverage = len(storyboard.get("shot_prompt_pack", {}))

    status = (
        "PASS"
        if not missing_rules
        and all(not value["missing_terms"] for value in validations.values())
        and not anchor_coverage["missing_from_video_prompts"]
        and reference_validation["ready"]
        and shot_coverage == shot_prompt_coverage
        else "REVIEW"
    )
    return {
        "pipeline": "PROMPT_VALIDATOR",
        "status": status,
        "validations": validations,
        "missing_compliance_rules": missing_rules,
        "anchor_coverage": anchor_coverage,
        "reference_validation": reference_validation,
        "shot_coverage": shot_coverage,
        "shot_prompt_coverage": shot_prompt_coverage,
        "repair_instructions": _repair_instructions(status, missing_rules, anchor_coverage, reference_validation),
        "negative_prompt": _negative_prompt(compliance),
        "prompt_usage": "Run before exporting final production package.",
    }


def _validate_prompt(prompt: str) -> Dict[str, Any]:
    missing = [term for term in REQUIRED_PROMPT_TERMS if term not in prompt]
    return {
        "missing_terms": missing,
        "length": len(prompt),
        "ready": not missing,
    }


def _missing_compliance_rules(prompts: Dict[str, Any], hard_rules: List[str]) -> List[str]:
    prompt_text = f"{prompts.get('seedance_20_15s', '')} {prompts.get('seedance_25_30s', '')}"
    missing = []
    for rule in hard_rules:
        key_terms = [part for part in rule.replace("，", " ").replace("。", " ").split() if len(part) >= 2]
        if key_terms and not any(term in prompt_text for term in key_terms):
            missing.append(rule)
    return missing


def _anchor_coverage(anchors: List[str], prompts: Dict[str, Any], visual: Dict[str, Any]) -> Dict[str, Any]:
    image_text = str(visual.get("image_prompts", ""))
    video_text = f"{prompts.get('seedance_20_15s', '')} {prompts.get('seedance_25_30s', '')}"
    return {
        "anchors": anchors,
        "missing_from_image_prompts": [anchor for anchor in anchors if anchor not in image_text],
        "missing_from_video_prompts": [anchor for anchor in anchors if anchor not in video_text],
    }


def _reference_validation(asset_ledger: Dict[str, Any], storyboard: Dict[str, Any]) -> Dict[str, Any]:
    reference_duty = asset_ledger.get("reference_duty", {})
    has_identity = bool(reference_duty.get("identity_lock"))
    has_execution = bool(reference_duty.get("execution_state"))
    shot_contract = storyboard.get("shot_contract", [])
    shots_with_refs = [
        shot.get("shot_id")
        for shot in shot_contract
        if shot.get("reference_assets", {}).get("identity") and shot.get("reference_assets", {}).get("execution")
    ]
    return {
        "ready": has_identity and has_execution and len(shots_with_refs) == len(shot_contract),
        "has_identity_reference": has_identity,
        "has_execution_reference": has_execution,
        "shots_with_required_refs": shots_with_refs,
    }


def _repair_instructions(
    status: str,
    missing_rules: List[str],
    anchor_coverage: Dict[str, Any],
    reference_validation: Dict[str, Any],
) -> List[str]:
    if status == "PASS":
        return []
    instructions = [
        "Append missing compliance rules to both Seedance prompt variants.",
        "Check every shot includes subject, action, camera, continuity, and negative constraints.",
    ]
    instructions.extend(f"Add rule: {rule}" for rule in missing_rules)
    instructions.extend(f"Add identity anchor to video prompts: {anchor}" for anchor in anchor_coverage["missing_from_video_prompts"])
    if not reference_validation["ready"]:
        instructions.append("Repair reference duty: every shot needs identity and execution references.")
    return instructions


def _negative_prompt(compliance: Dict[str, Any]) -> str:
    rules = compliance.get("hard_rules", []) + compliance.get("blocked_claims", [])
    return "Negative prompt / 禁止项: " + "；".join(rules)
