"""Pipeline 8: Build annual festival/node campaign plan."""

from __future__ import annotations

from typing import Any, Dict


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    nodes = state.get("campaign_calendar", {}).get("annual_nodes", {})
    channel_plan = state["CHANNEL_PLANNER"]["channel_plan"]
    occasion = channel_plan.get("occasion", "")
    brief = state["INPUT_COMPILER"]["compiled_brief"]
    research = state["RESEARCH_SYNTHESIS"]["design_strategy"]

    matched = nodes.get(occasion, {}) if occasion else {}
    annual_calendar = {
        name: {
            "date_rule": spec.get("date_rule", ""),
            "category": spec.get("category", ""),
            "campaign_angle": _campaign_angle(name, spec, brief, research),
            "poster_motifs": spec.get("poster_motifs", []),
            "content_angles": spec.get("content_angles", []),
            "forbidden_tones": spec.get("forbidden_tones", []),
        }
        for name, spec in nodes.items()
    }

    campaign_focus = {
        "occasion": occasion or "全年节点规划",
        "matched": bool(matched),
        "date_rule": matched.get("date_rule", ""),
        "audience_emotion": matched.get("audience_emotion", ""),
        "visual_symbols": matched.get("visual_symbols", []),
        "content_angles": matched.get("content_angles", []),
        "poster_motifs": matched.get("poster_motifs", []),
        "forbidden_tones": matched.get("forbidden_tones", []),
        "industry_integration": _industry_integration(brief, research, matched),
    }

    return {
        "pipeline": "CAMPAIGN_CALENDAR",
        "annual_calendar": annual_calendar,
        "campaign_focus": campaign_focus,
        "prompt_usage": "Use campaign_focus for a current festival/event; use annual_calendar for yearly content planning.",
    }


def _campaign_angle(name: str, spec: Dict[str, Any], brief: Dict[str, Any], research: Dict[str, Any]) -> str:
    angles = spec.get("content_angles", [])
    base = angles[0] if angles else "节点关怀"
    return f"{name}: 用 {brief['ip_name']} 表达「{base}」，结合行业方向：{research.get('story_direction', '')}"


def _industry_integration(brief: Dict[str, Any], research: Dict[str, Any], matched: Dict[str, Any]) -> str:
    if not matched:
        return f"围绕 {brief['ip_name']} 的行业语境，规划全年节点内容。"
    return (
        f"把「{matched.get('audience_emotion', '')}」和行业关怀结合；"
        f"IP 负责承载情绪，产品/服务负责给出具体行动。"
    )
