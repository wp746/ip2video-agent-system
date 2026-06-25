"""Pipeline 00: Plan design research before production."""

from __future__ import annotations

from typing import Any, Dict, List


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    request = state["request"]
    ip_input = request.get("ip_input", {})
    framework = state.get("design_research_framework", {})
    profile_id, matched_terms = _detect_profile(ip_input, framework.get("domain_profiles", {}))
    profile = framework.get("domain_profiles", {}).get(profile_id, {})

    research_plan = {
        "mode": "OFFLINE_BASELINE",
        "online_ready": True,
        "domain_profile_id": profile_id,
        "matched_terms": matched_terms,
        "recommended_template_id": profile.get("recommended_template_id", "KID-B"),
        "dimensions": framework.get("research_dimensions", []),
        "questions": _questions(ip_input, profile_id),
        "source_policy": [
            "Use offline framework first for deterministic local runs.",
            "When web research is enabled, collect references before final production and store citations separately.",
        ],
    }

    return {
        "pipeline": "RESEARCH_PLANNER",
        "research_plan": research_plan,
        "profile_summary": f"{profile_id} / template={research_plan['recommended_template_id']}",
        "prompt_usage": "Run before input compilation so research can shape the production brief.",
    }


def _detect_profile(ip_input: Dict[str, Any], profiles: Dict[str, Any]) -> tuple[str, List[str]]:
    text = " ".join(
        str(value)
        for value in [
            ip_input.get("name", ""),
            ip_input.get("type", ""),
            ip_input.get("description", ""),
            ip_input.get("audience", ""),
            ip_input.get("product", ""),
            " ".join(ip_input.get("visual_elements", [])),
            " ".join(ip_input.get("constraints", [])),
        ]
    )
    best_profile = "general_ip"
    best_terms: List[str] = []
    for profile_id, profile in profiles.items():
        terms = [term for term in profile.get("triggers", []) if term and term in text]
        if len(terms) > len(best_terms):
            best_profile = profile_id
            best_terms = terms
    return best_profile, best_terms


def _questions(ip_input: Dict[str, Any], profile_id: str) -> List[str]:
    return [
        f"这个 IP 在 `{profile_id}` 语境下最重要的受众情绪是什么？",
        "同类内容中最容易被误用或过度套模板的视觉语言是什么？",
        "哪些元素必须进入 IP Bible 才能防止后续生成漂移？",
        "哪些合规、品牌或平台限制必须在生成前写成硬规则？",
        f"当前用户输入里还缺哪些信息：{', '.join(_missing_fields(ip_input)) or '无'}",
    ]


def _missing_fields(ip_input: Dict[str, Any]) -> List[str]:
    return [field for field in ("name", "description", "audience", "visual_elements") if not ip_input.get(field)]
