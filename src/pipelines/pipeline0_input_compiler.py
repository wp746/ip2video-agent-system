"""Pipeline 0: Compile raw user input into a production brief."""

from __future__ import annotations

from typing import Any, Dict, List


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    request = state["request"]
    ip_input = request.get("ip_input", {})
    request_meta = request.get("request", {})
    config = state.get("config", {})
    synthesis = state.get("RESEARCH_SYNTHESIS", {})
    design_strategy = synthesis.get("design_strategy", {})

    duration = ip_input.get("duration") or config.get("default_duration", "30s")
    template_id = (
        request_meta.get("style_template_id")
        or design_strategy.get("style_template_recommendation")
        or config.get("default_template_id", "MED-A")
    )
    platform = ip_input.get("platform", "Seedance 2.5")
    constraints = list(ip_input.get("constraints", []))
    unknowns = _find_unknowns(ip_input)

    compiled_brief = {
        "ip_name": ip_input.get("name", "IP"),
        "ip_type": ip_input.get("type", "虚拟人物"),
        "description": ip_input.get("description", ""),
        "audience": ip_input.get("audience", "大众用户"),
        "product": ip_input.get("product", ""),
        "platform": platform,
        "duration": duration,
        "language": ip_input.get("language", "bilingual"),
        "goal": request_meta.get("goal", "生成 AIGC 短片提示词包"),
        "template_id": template_id,
        "universe_id": request_meta.get("universe_id", "health_heroes"),
        "visual_elements": list(ip_input.get("visual_elements", [])),
        "constraints": constraints,
        "design_strategy": design_strategy,
        "research_profile_id": state.get("RESEARCH_PLANNER", {}).get("research_plan", {}).get("domain_profile_id", "general_ip"),
        "reference_keywords": design_strategy.get("reference_keywords", []),
        "forbidden_tones": design_strategy.get("forbidden_tones", []),
    }

    signoff = {
        "status": "READY_WITH_ASSUMPTIONS" if unknowns else "READY",
        "evidence_grade": {
            "ip_identity": "USER_CONFIRMED" if ip_input.get("name") else "UNKNOWN",
            "visual_elements": "USER_CONFIRMED" if ip_input.get("visual_elements") else "INFERRED_TENTATIVE",
            "product": "USER_CONFIRMED" if ip_input.get("product") else "UNKNOWN",
            "duration": "USER_CONFIRMED" if ip_input.get("duration") else "INFERRED_TENTATIVE",
            "platform": "USER_CONFIRMED" if ip_input.get("platform") else "INFERRED_TENTATIVE",
            "design_research": "RESEARCH_SYNTHESIZED" if design_strategy else "NOT_AVAILABLE",
        },
        "unknowns": unknowns,
        "downstream_gate": "Do not generate final prompts unless compiled_brief and constraints are present.",
    }

    return {
        "pipeline": "INPUT_COMPILER",
        "compiled_brief": compiled_brief,
        "signoff": signoff,
        "production_intent": _production_intent(compiled_brief),
        "prompt_usage": "All downstream pipelines must use compiled_brief rather than raw user input.",
    }


def _find_unknowns(ip_input: Dict[str, Any]) -> List[str]:
    unknowns = []
    for field in ("name", "description", "audience", "visual_elements"):
        if not ip_input.get(field):
            unknowns.append(f"ip_input.{field}")
    return unknowns


def _production_intent(brief: Dict[str, Any]) -> str:
    return (
        f"{brief['ip_name']} for {brief['audience']}; platform={brief['platform']}; "
        f"duration={brief['duration']}; template={brief['template_id']}."
    )
