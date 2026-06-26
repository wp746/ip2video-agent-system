"""Pipeline 1: IP understanding and rule locking."""

from __future__ import annotations

from typing import Any, Dict


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    ip_input = state["INPUT_COMPILER"]["compiled_brief"]
    template = state.get("template", {})
    universe = state.get("universe", {})
    duration = state.get("duration", "30s")
    research_profile = ip_input.get("research_profile_id", "general_ip")

    name = ip_input.get("ip_name", "IP")
    visual_elements = ip_input.get("visual_elements", [])
    constraints = ip_input.get("constraints", [])

    return {
        "pipeline": "IP_UNDERSTANDING",
        "ip_profile": {
            "name": name,
            "type": ip_input.get("ip_type", "虚拟人物"),
            "description": ip_input.get("description", ""),
            "audience": ip_input.get("audience", "大众用户"),
            "product": ip_input.get("product", ""),
            "duration": duration,
            "platform": ip_input.get("platform", "Seedance 2.5"),
        },
        "fixed_rules": {
            "silhouette": "Keep the character readable in every shot: " + ", ".join(visual_elements),
            "world_rules": universe.get("rules", []),
            "brand_constraints": constraints,
            "visual_constants": template.get("visual_specs", {}),
        },
        "audience_promise": _audience_promise(name, research_profile),
        "prompt_usage": "This profile anchors all image prompts, storyboard prompts, and Seedance video prompts.",
    }


def _audience_promise(name: str, research_profile: str) -> str:
    if research_profile == "engineering_maritime":
        return f"{name}把宏大的基建、航运与安全主题，转化为可看见的一线岗位动作和可信的官方宣发表达。"
    if research_profile == "brand_product":
        return f"{name}把产品价值转化为清晰、可信、有行动场景的品牌短片任务。"
    if research_profile == "suspense_reveal":
        return f"{name}把异常钩子转化为有逻辑、有反转、有记忆点的短片任务。"
    return f"{name}把复杂或紧张的体验变成一次可理解、可完成、被陪伴的短片任务。"
