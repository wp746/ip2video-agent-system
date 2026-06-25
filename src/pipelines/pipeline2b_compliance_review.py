"""Pipeline 2B: Compliance, brand, and audience safety review."""

from __future__ import annotations

from typing import Any, Dict, List


MEDICAL_KEYWORDS = ("注射", "治疗", "药", "医疗", "医院", "医生", "针")
CHILD_KEYWORDS = ("儿童", "孩子", "小孩", "6-10")


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    brief = state["INPUT_COMPILER"]["compiled_brief"]
    story = state["STORY_CREATION"]
    constraints = brief.get("constraints", [])
    forbidden_tones = brief.get("forbidden_tones", [])
    text = f"{brief} {story}"

    risk_flags = []
    if any(keyword in text for keyword in MEDICAL_KEYWORDS):
        risk_flags.append("medical_safety")
    if any(keyword in text for keyword in CHILD_KEYWORDS):
        risk_flags.append("child_audience")
    if brief.get("product"):
        risk_flags.append("product_claims")

    hard_rules = list(constraints)
    hard_rules.extend(_default_rules(risk_flags))
    hard_rules.extend(f"避免调研判定的不适配调性：{tone}" for tone in forbidden_tones)

    return {
        "pipeline": "COMPLIANCE_REVIEW",
        "risk_flags": risk_flags,
        "hard_rules": _dedupe(hard_rules),
        "blocked_claims": [
            "不得承诺治疗效果、恢复速度或医学结果。",
            "不得展示危险动作的教学化细节。",
            "不得把产品塑造成替代医生诊疗的角色。",
        ],
        "required_disclaimers": [
            "医疗相关内容只用于情绪陪伴与科普表达，真实操作遵循医生或说明书指导。",
        ]
        if "medical_safety" in risk_flags
        else [],
        "signoff": "PASS_WITH_RULES",
        "prompt_usage": "All final prompts must include hard_rules and blocked_claims as negative constraints.",
    }


def _default_rules(risk_flags: List[str]) -> List[str]:
    rules = []
    if "medical_safety" in risk_flags:
        rules.extend(
            [
                "医疗动作由成年人或专业人员完成。",
                "不展示针头刺入、血液、痛苦表情或恐怖医疗细节。",
                "产品只作为道具或流程提示，不承诺疗效。",
            ]
        )
    if "child_audience" in risk_flags:
        rules.extend(
            [
                "画面情绪必须儿童友好，避免惊吓、威胁和惩罚式表达。",
                "动作必须安全，不能鼓励儿童自行操作医疗用品。",
            ]
        )
    return rules


def _dedupe(items: List[str]) -> List[str]:
    result = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result
