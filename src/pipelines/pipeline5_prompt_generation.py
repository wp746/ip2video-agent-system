"""Pipeline 5: Prompt aggregation for final Markdown generation."""

from __future__ import annotations

from typing import Any, Dict


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    ip = state["IP_UNDERSTANDING"]["ip_profile"]
    story = state["STORY_CREATION"]
    visual = state["VISUAL_DESIGN"]
    cine = state["CINEMATOGRAPHY"]
    compliance = state["COMPLIANCE_REVIEW"]
    storyboard = state["STORYBOARD_CONTRACT"]
    ip_bible = state["IP_BIBLE_BUILDER"]["ip_bible"]
    name = ip["name"]

    seedance_20_15s = _seedance_prompt(name, story, visual, cine, compliance, storyboard, ip_bible, "15-second", max_shots=3)
    seedance_25_30s = _seedance_prompt(name, story, visual, cine, compliance, storyboard, ip_bible, "30-second", max_shots=5)
    seedance_25_60s = _seedance_prompt(name, story, visual, cine, compliance, storyboard, ip_bible, "1-minute", max_shots=8)

    return {
        "pipeline": "PROMPT_GENERATION",
        "seedance_20_15s": seedance_20_15s,
        "seedance_25_30s": seedance_25_30s,
        "seedance_25_60s": seedance_25_60s,
        "usage_steps": [
            "Use the character asset board prompt in Image2 or another image generator to lock the IP identity.",
            "Generate the scene 9-grid and storyboard board, then select the clearest references.",
            "Confirm the asset ledger: identity reference and execution storyboard must not be mixed.",
            "Upload the chosen character, scene, prop, and storyboard references to Seedance.",
            "Use the 15s prompt for Seedance 2.0, the 30s prompt for quick tests, or the 60s prompt for full IP story videos.",
            "Apply the negative prompt and compliance rules before generation.",
            "Review whether the character silhouette, product handling, and emotional payoff remain consistent.",
        ],
        "audio_prompt": _audio_prompt(cine),
        "prompt_usage": "Final prompt package is ready for Markdown export.",
    }


def _seedance_prompt(
    name: str,
    story: Dict[str, Any],
    visual: Dict[str, Any],
    cine: Dict[str, Any],
    compliance: Dict[str, Any],
    storyboard: Dict[str, Any],
    ip_bible: Dict[str, Any],
    duration_label: str,
    max_shots: int,
) -> str:
    shots = cine["shots"][:max_shots]
    shot_text = " ".join(
        f"{shot['shot']} {shot['time']}: {shot['action_en']} Camera: {shot['camera']} Transition: {shot['transition']}."
        for shot in shots
    )
    style = visual["style_lock"]
    negative_constraints = " ".join(compliance.get("hard_rules", []) + compliance.get("blocked_claims", []))
    reference_contract = storyboard["storyboard_signoff"]["reference_split"]
    anchors = ", ".join(ip_bible["visual_lock"]["must_keep"])
    return (
        f"Create a {duration_label} cinematic AIGC short film featuring {name}. "
        f"Story: {story['logline_en']} Theme: {story['theme']}. "
        f"Visual style: {style['style']}; palette: {style['palette']}; lighting: {style['lighting']}; material: {style['material']}. "
        f"Fixed identity anchors that must remain visible: {anchors}. "
        f"Reference contract: identity references {reference_contract.get('identity_lock', [])}; execution references {reference_contract.get('execution_state', [])}. "
        f"Shot plan: {shot_text} "
        "Keep the character identity stable across all shots. Keep actions safe, readable, and aligned with the campaign context. "
        f"Negative constraints: {negative_constraints}. "
        "End with a clear emotional payoff and a clean official-account-ready final frame."
    )


def _audio_prompt(cine: Dict[str, Any]) -> str:
    audio = cine["audio_direction"]
    return (
        f"Music prompt: {audio['bgm']}, {audio['bpm']} BPM, instruments: {audio['instruments']}. "
        f"Sound effects: {audio['sfx']}. Mix should support warmth, trust, and clear emotional rhythm."
    )
