"""Pipeline 4: Cinematography, editing rhythm, and audio direction."""

from __future__ import annotations

from typing import Any, Dict, List


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    story = state["STORY_CREATION"]["story_beats"]
    ip = state["IP_UNDERSTANDING"]["ip_profile"]
    template = state.get("template", {})
    cine_specs = template.get("cinematography_specs", {})
    audio_specs = template.get("audio_specs", {})
    duration = state.get("duration", "30s")
    profile_id = state["INPUT_COMPILER"]["compiled_brief"].get("research_profile_id", "")

    shots = _build_shots(story, cine_specs)
    return {
        "pipeline": "CINEMATOGRAPHY",
        "shots": shots,
        "audio_direction": {
            "bgm": audio_specs.get("bgm", "warm minimal music"),
            "bpm": audio_specs.get("bpm", "80-100"),
            "instruments": audio_specs.get("instruments", "soft piano, warm pad"),
            "sfx": _sfx(profile_id),
        },
        "seedance_notes": {
            "duration": duration,
            "camera_language": cine_specs.get("camera_moves", "slow push-in, gentle orbit"),
            "logo_position": cine_specs.get("logo_position", "final clean frame"),
            "safety": _safety_note(ip, profile_id),
        },
        "prompt_usage": "Each shot can be copied into image prompts, storyboard prompts, or Seedance video prompts.",
    }


def _build_shots(story_beats: List[Dict[str, str]], cine_specs: Dict[str, Any]) -> List[Dict[str, str]]:
    moves = cine_specs.get("camera_moves", "slow push-in, gentle orbit")
    lenses = cine_specs.get("lenses", "35mm, 50mm, 85mm")
    shots = []
    for index, beat in enumerate(story_beats, start=1):
        shots.append(
            {
                "shot": f"S{index:02d}",
                "time": beat["time"],
                "beat": beat["beat"],
                "purpose": beat.get("purpose", ""),
                "action_cn": beat["cn"],
                "action_en": beat["en"],
                "camera": f"{lenses}; {moves}; keep subject readable and motion smooth.",
                "transition": "soft match cut" if index < len(story_beats) else "clean end-card hold",
            }
        )
    return shots


def _sfx(profile_id: str) -> str:
    if profile_id == "engineering_maritime":
        return "port ambience, distant ship horn, radio click, paper blueprint movement, soft equipment hum, ocean wind"
    return "soft glow, gentle cloth movement, tiny bell, room tone, no frightening sound"


def _safety_note(ip: Dict[str, Any], profile_id: str) -> str:
    product = ip.get("product") or "the product"
    if profile_id == "engineering_maritime":
        return f"Keep {product} clear through safe, standards-aligned engineering or maritime actions."
    return f"Keep {product} clear through safe, gentle, and non-frightening actions."
