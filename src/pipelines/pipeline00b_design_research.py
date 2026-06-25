"""Pipeline 00B: Produce deterministic design research from the selected profile."""

from __future__ import annotations

from typing import Any, Dict


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    plan = state["RESEARCH_PLANNER"]["research_plan"]
    profiles = state.get("design_research_framework", {}).get("domain_profiles", {})
    profile = profiles.get(plan["domain_profile_id"], profiles.get("general_ip", {}))
    ip_input = state["request"].get("ip_input", {})

    design_research = {
        "domain_profile_id": plan["domain_profile_id"],
        "research_mode": plan["mode"],
        "ip_context": {
            "name": ip_input.get("name", "IP"),
            "type": ip_input.get("type", "虚拟人物"),
            "audience": ip_input.get("audience", "大众用户"),
            "product": ip_input.get("product", ""),
        },
        "audience_insights": profile.get("audience_insights", []),
        "category_context": profile.get("category_context", []),
        "visual_language": profile.get("visual_language", []),
        "narrative_opportunity": profile.get("narrative_opportunity", ""),
        "forbidden_tones": profile.get("forbidden_tones", []),
        "reference_keywords": profile.get("reference_keywords", []),
        "assumptions": _assumptions(ip_input, plan),
        "research_limitations": [
            "This run uses the local research framework, not live web search.",
            "External market references should be refreshed before commercial launch or final brand approval.",
        ],
    }

    return {
        "pipeline": "DESIGN_RESEARCH",
        "design_research": design_research,
        "research_summary": _summary(design_research),
        "prompt_usage": "Use design_research to choose template, story direction, visual language, and risk boundaries.",
    }


def _assumptions(ip_input: Dict[str, Any], plan: Dict[str, Any]) -> list[str]:
    assumptions = []
    if not ip_input.get("audience"):
        assumptions.append("Audience is inferred from IP/product context.")
    if not ip_input.get("visual_elements"):
        assumptions.append("Visual anchors need to be inferred and should be confirmed by the user.")
    assumptions.append(f"Template recommendation is based on matched terms: {', '.join(plan.get('matched_terms', [])) or 'none'}.")
    return assumptions


def _summary(research: Dict[str, Any]) -> str:
    return (
        f"{research['domain_profile_id']} research: "
        f"{len(research['audience_insights'])} audience insights, "
        f"{len(research['visual_language'])} visual-language notes, "
        f"{len(research['forbidden_tones'])} forbidden tones."
    )
