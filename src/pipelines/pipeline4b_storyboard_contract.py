"""Pipeline 4B: Convert shots into a strict storyboard execution contract."""

from __future__ import annotations

from typing import Any, Dict


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    shots = state["CINEMATOGRAPHY"]["shots"]
    ledger = state["ASSET_LEDGER"]
    compliance = state["COMPLIANCE_REVIEW"]
    ip_bible = state["IP_BIBLE_BUILDER"]["ip_bible"]
    visual = state["VISUAL_DESIGN"]
    identity_refs = ledger["reference_duty"].get("identity_lock", [])
    execution_refs = ledger["reference_duty"].get("execution_state", [])
    product_refs = ledger["reference_duty"].get("product_lock", [])

    contract_shots = []
    for shot in shots:
        contract = {
            "shot_id": shot["shot"],
            "time": shot["time"],
            "duration_seconds": _duration_seconds(shot["time"]),
            "beat": shot["beat"],
            "purpose": shot.get("purpose", ""),
            "subject": _subject(shot),
            "action": shot["action_cn"],
            "action_en": shot["action_en"],
            "camera": shot["camera"],
            "transition": shot["transition"],
            "first_frame_state": _first_frame(shot),
            "last_frame_state": _last_frame(shot),
            "reference_assets": {
                "identity": identity_refs,
                "execution": execution_refs,
                "product": product_refs,
            },
            "visible_identity_anchors": ip_bible["visual_lock"]["must_keep"],
            "negative_constraints": compliance["hard_rules"],
            "continuity_check": [
                "IP identity anchors visible",
                "Product/action relationship clear",
                "No forbidden medical, fear, or unsafe detail",
                "First and last frame states are visually different",
            ],
        }
        contract["single_shot_prompt_en"] = _single_shot_prompt(contract, visual)
        contract_shots.append(contract)

    return {
        "pipeline": "STORYBOARD_CONTRACT",
        "shot_contract": contract_shots,
        "shot_prompt_pack": {shot["shot_id"]: shot["single_shot_prompt_en"] for shot in contract_shots},
        "storyboard_signoff": {
            "status": "READY_FOR_VIDEO_PROMPT",
            "required_assets": ledger["asset_signoff"]["required_before_video"],
            "reference_split": ledger["reference_duty"],
            "shot_count": len(contract_shots),
            "total_duration_seconds": sum(shot["duration_seconds"] for shot in contract_shots),
        },
        "prompt_usage": "Video prompts must preserve this shot contract and include negative constraints.",
    }


def _duration_seconds(time_value: str) -> int:
    try:
        start, end = time_value.replace("s", "").split("-")
        return max(0, int(float(end) - float(start)))
    except (ValueError, AttributeError):
        return 0


def _subject(shot: Dict[str, str]) -> str:
    if shot["shot"] == "S01":
        return "target user, key object, environment tension"
    if shot["shot"] == "S05":
        return "IP protagonist, target user, product or memory object"
    return "IP protagonist, target user, product or action object according to beat"


def _first_frame(shot: Dict[str, str]) -> str:
    return f"{shot['shot']} begins with the emotional state of '{shot['beat']}' clearly readable."


def _last_frame(shot: Dict[str, str]) -> str:
    return f"{shot['shot']} ends with a changed emotional or action state that motivates the next cut."


def _single_shot_prompt(contract: Dict[str, Any], visual: Dict[str, Any]) -> str:
    style = visual["style_lock"]
    anchors = ", ".join(contract["visible_identity_anchors"])
    negative = " ".join(contract["negative_constraints"])
    refs = contract["reference_assets"]
    return (
        f"{contract['shot_id']} single-shot video prompt. Duration: {contract['duration_seconds']} seconds. "
        f"Subject: {contract['subject']}. Action: {contract['action_en']}. "
        f"First frame: {contract['first_frame_state']} Last frame: {contract['last_frame_state']} "
        f"Camera: {contract['camera']} Transition: {contract['transition']}. "
        f"Visual style: {style['style']}; palette: {style['palette']}; lighting: {style['lighting']}; material: {style['material']}. "
        f"Identity anchors visible: {anchors}. Reference assets: identity={refs['identity']}, execution={refs['execution']}, product={refs['product']}. "
        f"Negative constraints: {negative}. Keep motion smooth, readable, and consistent with the storyboard contract."
    )
