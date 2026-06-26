"""Pipeline 00C: Convert design research into production strategy."""

from __future__ import annotations

from typing import Any, Dict


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    plan = state["RESEARCH_PLANNER"]["research_plan"]
    research = state["DESIGN_RESEARCH"]["design_research"]
    ip_input = state["request"].get("ip_input", {})

    design_strategy = {
        "style_template_recommendation": plan["recommended_template_id"],
        "audience_taste": _join(research["audience_insights"]),
        "emotional_positioning": _emotional_positioning(research),
        "visual_direction": _join(research["visual_language"]),
        "story_direction": _as_text(research["narrative_opportunity"]),
        "asset_priorities": _asset_priorities(research, ip_input),
        "forbidden_tones": research["forbidden_tones"],
        "reference_keywords": research["reference_keywords"],
        "production_hypothesis": (
            "Use the research-selected template to create an IP-consistent, platform-ready prompt package "
            "with clear identity anchors, reference-duty separation, and compliance boundaries."
        ),
    }

    return {
        "pipeline": "RESEARCH_SYNTHESIS",
        "design_strategy": design_strategy,
        "synthesis_signoff": {
            "status": "READY_FOR_INPUT_COMPILER",
            "recommended_template_id": design_strategy["style_template_recommendation"],
            "requires_user_confirmation": bool(research.get("assumptions")),
            "assumptions": research.get("assumptions", []),
        },
        "prompt_usage": "Input compiler must merge this strategy into the production brief.",
    }


def _join(items: list[str]) -> str:
    return "；".join(items)


def _as_text(value) -> str:
    if isinstance(value, list):
        return "；".join(str(item) for item in value)
    return str(value)


def _emotional_positioning(research: Dict[str, Any]) -> str:
    if research["domain_profile_id"] == "health_children":
        return "紧张被看见 -> 规则被理解 -> 被陪伴完成 -> 放松和信任"
    if research["domain_profile_id"] == "brand_product":
        return "问题显现 -> 机制可信 -> 结果清楚 -> 品牌记忆"
    if research["domain_profile_id"] == "suspense_reveal":
        return "异常 -> 误判 -> 反转 -> 余韵"
    if research["domain_profile_id"] == "engineering_maritime":
        return "宏大工程现场 -> 一线岗位动作 -> 安全与担当被看见 -> 节点致敬 -> 品牌可信收束"
    return "好奇 -> 尝试 -> 小困难 -> 完成 -> 奖励"


def _asset_priorities(research: Dict[str, Any], ip_input: Dict[str, Any]) -> list[str]:
    priorities = ["CHAR-001 identity board", "BOARD-001 storyboard execution board"]
    if ip_input.get("product"):
        priorities.append("PROP-001 product/action prop board")
    priorities.append("SCENE-001 world and lighting board")
    if research["domain_profile_id"] == "brand_product":
        priorities.append("PACK-001 clean product end-frame or packshot reference")
    return priorities
