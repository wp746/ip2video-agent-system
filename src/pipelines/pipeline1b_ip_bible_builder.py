"""Pipeline 1B: Build a durable IP bible for identity and drift control."""

from __future__ import annotations

from typing import Any, Dict


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    brief = state["INPUT_COMPILER"]["compiled_brief"]
    ip_profile = state["IP_UNDERSTANDING"]["ip_profile"]
    fixed_rules = state["IP_UNDERSTANDING"]["fixed_rules"]
    template = state.get("template", {})
    design_strategy = state.get("INPUT_COMPILER", {}).get("compiled_brief", {}).get("design_strategy", {})

    visual_specs = template.get("visual_specs", {})
    ip_bible = {
        "identity": {
            "name": ip_profile["name"],
            "type": ip_profile.get("type", ""),
            "core_promise": state["IP_UNDERSTANDING"]["audience_promise"],
            "personality": "温柔、可靠、鼓励式陪伴，不替代专业人员。",
        },
        "visual_lock": {
            "must_keep": brief.get("visual_elements", []),
            "silhouette_rule": fixed_rules.get("silhouette", ""),
            "palette": visual_specs.get("palette", ""),
            "lighting": visual_specs.get("lighting", ""),
            "materials": visual_specs.get("material", ""),
            "style": visual_specs.get("style", ""),
        },
        "allowed_variation": [
            "表情可以随剧情在紧张、鼓励、放松之间变化。",
            "披风和盾牌可以产生轻微发光、摆动和缩放。",
            "场景可在家、医院、诊室、夜间床边之间切换。",
        ],
        "forbidden_variation": [
            "不得改变头部核心形状、主色、披风识别色和道具职责。",
            "不得让 IP 执行医生、成年人或监管角色才应完成的行为。",
            "不得用恐怖医疗特写制造刺激。",
            *[f"不得使用调研禁止调性：{tone}。" for tone in design_strategy.get("forbidden_tones", [])],
        ],
        "continuity_hooks": [
            "每个镜头至少保留一个身份锚点：头顶嫩芽、橙色披风、透明盾牌。",
            "产品出现时必须与剧情动作相关，不做漂浮式硬贴标。",
            "最终画面需要同时保留 IP、情绪结果和产品/道具关系。",
        ],
    }

    return {
        "pipeline": "IP_BIBLE_BUILDER",
        "ip_bible": ip_bible,
        "identity_lock": ip_bible["visual_lock"]["must_keep"],
        "prompt_usage": "Use this bible as the source of truth for all image boards, shots, and video prompts.",
    }
