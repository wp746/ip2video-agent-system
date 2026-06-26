"""Pipeline 1B: Build a durable IP bible for identity and drift control."""

from __future__ import annotations

from typing import Any, Dict


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    brief = state["INPUT_COMPILER"]["compiled_brief"]
    ip_profile = state["IP_UNDERSTANDING"]["ip_profile"]
    fixed_rules = state["IP_UNDERSTANDING"]["fixed_rules"]
    template = state.get("template", {})
    design_strategy = state.get("INPUT_COMPILER", {}).get("compiled_brief", {}).get("design_strategy", {})
    research_profile = state.get("INPUT_COMPILER", {}).get("compiled_brief", {}).get("research_profile_id", "general_ip")
    anchors = ip_profile_anchors = brief.get("visual_elements", [])

    visual_specs = template.get("visual_specs", {})
    ip_bible = {
        "identity": {
            "name": ip_profile["name"],
            "type": ip_profile.get("type", ""),
            "core_promise": state["IP_UNDERSTANDING"]["audience_promise"],
            "personality": "温柔、可靠、鼓励式陪伴，不替代专业人员。",
        },
        "visual_lock": {
            "must_keep": ip_profile_anchors,
            "silhouette_rule": fixed_rules.get("silhouette", ""),
            "palette": visual_specs.get("palette", ""),
            "lighting": visual_specs.get("lighting", ""),
            "materials": visual_specs.get("material", ""),
            "style": visual_specs.get("style", ""),
        },
        "allowed_variation": _allowed_variation(research_profile),
        "forbidden_variation": _forbidden_variation(research_profile, design_strategy),
        "continuity_hooks": _continuity_hooks(anchors, research_profile),
    }

    return {
        "pipeline": "IP_BIBLE_BUILDER",
        "ip_bible": ip_bible,
        "identity_lock": ip_bible["visual_lock"]["must_keep"],
        "prompt_usage": "Use this bible as the source of truth for all image boards, shots, and video prompts.",
    }


def _allowed_variation(research_profile: str) -> list[str]:
    if research_profile == "engineering_maritime":
        return [
            "表情可以在专注、微笑、致敬、协作之间变化。",
            "动作可以围绕巡检、掌舵、看图纸、对讲、挥手送航展开。",
            "场景可在驾驶舱、甲板、港口、桥梁、施工现场之间切换。",
        ]
    return [
        "表情可以随剧情在紧张、鼓励、放松之间变化。",
        "道具可以产生轻微发光、摆动和缩放。",
        "场景可以围绕用户任务需要切换，但身份锚点必须稳定。",
    ]


def _forbidden_variation(research_profile: str, design_strategy: Dict[str, Any]) -> list[str]:
    if research_profile == "engineering_maritime":
        base = [
            "不得改变安全帽、中国交建标识、蓝白工装和 Q 版工程 IP 轮廓。",
            "不得出现不规范安全作业或错误工程设备操作。",
            "不得让卖萌压过岗位动作、工程场景和央企官方传播气质。",
        ]
    else:
        base = [
            "不得改变头部核心形状、主色、关键身份锚点和道具职责。",
            "不得让 IP 执行不符合品牌、行业或受众安全边界的行为。",
            "不得用高刺激画面破坏内容可信度。",
        ]
    base.extend(f"不得使用调研禁止调性：{tone}。" for tone in design_strategy.get("forbidden_tones", []))
    return base


def _continuity_hooks(anchors: list[str], research_profile: str) -> list[str]:
    anchor_text = "、".join(anchors[:5]) if anchors else "关键身份锚点"
    if research_profile == "engineering_maritime":
        return [
            f"每个镜头至少保留一个中国交建 IP 身份锚点：{anchor_text}。",
            "每个镜头必须有具体岗位动作或工程场景，不做纯摆拍。",
            "最终画面需要同时保留 IP、行业节点、工程/航运场景和官方品牌气质。",
        ]
    return [
        f"每个镜头至少保留一个身份锚点：{anchor_text}。",
        "产品或道具出现时必须与剧情动作相关，不做漂浮式硬贴标。",
        "最终画面需要同时保留 IP、情绪结果和产品/道具关系。",
    ]
