"""Pipeline 2: Story and script creation."""

from __future__ import annotations

from typing import Any, Dict, List


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    ip = state["IP_UNDERSTANDING"]["ip_profile"]
    template = state.get("template", {})
    duration = state.get("duration", "30s")
    request_goal = state["INPUT_COMPILER"]["compiled_brief"].get("goal", "")
    archetype = state.get("story_archetypes", {}).get(state.get("template_id"), {})
    design_strategy = state["INPUT_COMPILER"]["compiled_brief"].get("design_strategy", {})
    name = ip["name"]
    product = ip.get("product") or "关键道具/核心对象"

    beats = _build_beats(name, product, duration, archetype)
    logline_cn = _format_pattern(
        archetype.get("logline_pattern_cn"),
        fallback=f"{name}把一个关键场景变成一次有情绪、有行动、有记忆点的短片任务。",
        name=name,
        product=product,
    )
    logline_en = _format_pattern(
        archetype.get("logline_pattern_en"),
        fallback=f"{name} turns a key moment into a short film with emotion, action, and a clear memory point.",
        name=name,
        product=product,
    )
    return {
        "pipeline": "STORY_CREATION",
        "theme": template.get("narrative_specs", {}).get("theme_preference", "第一次勇气"),
        "goal": request_goal,
        "archetype": archetype.get("name", state.get("template_id")),
        "logline_cn": logline_cn,
        "logline_en": logline_en,
        "story_beats": beats,
        "story_constraints": _story_constraints(state),
        "research_story_direction": design_strategy.get("story_direction", ""),
        "emotional_curve": template.get("narrative_specs", {}).get("emotional_curve", ""),
        "structure_note": f"{duration} short-video rhythm generated from {state.get('template_id')} archetype.",
    }


def _build_beats(name: str, product: str, duration: str, archetype: Dict[str, Any]) -> List[Dict[str, str]]:
    beat_rows = archetype.get("beats_30s", [])
    if duration == "15s":
        selected_ids = set(archetype.get("beats_15s", []))
        beat_rows = [beat for beat in beat_rows if beat.get("id") in selected_ids]
    if not beat_rows:
        beat_rows = _fallback_beats()

    return [
        {
            "id": beat.get("id", f"B{index:02d}"),
            "time": beat.get("time", ""),
            "beat": beat.get("beat", ""),
            "purpose": beat.get("purpose", ""),
            "cn": _fill(beat.get("cn", ""), name, product),
            "en": _fill(beat.get("en", ""), name, product),
        }
        for index, beat in enumerate(beat_rows, start=1)
    ]


def _fill(value: str, name: str, product: str) -> str:
    return value.format(name=name, product_or_object=product, product=product)


def _format_pattern(pattern: str | None, fallback: str, name: str, product: str) -> str:
    return _fill(pattern or fallback, name, product)


def _story_constraints(state: Dict[str, Any]) -> List[str]:
    constraints = [
        "每个 beat 必须推动情绪或信息，不做纯装饰镜头。",
        "每个故事必须有钩子、行动变化和最终情绪结果。",
        "产品或道具必须通过动作进入，不做无动作硬露出。",
    ]
    story_direction = state.get("INPUT_COMPILER", {}).get("compiled_brief", {}).get("design_strategy", {}).get("story_direction")
    if story_direction:
        constraints.append(f"调研推荐叙事机会必须被体现：{story_direction}")
    constraints.extend(state.get("COMPLIANCE_REVIEW", {}).get("hard_rules", []))
    return constraints


def _fallback_beats() -> List[Dict[str, str]]:
    return [
        {"id": "B01", "time": "0-4s", "beat": "钩子", "purpose": "建立问题", "cn": "{name}遇到一个具体阻碍。", "en": "{name} faces a concrete obstacle."},
        {"id": "B02", "time": "4-10s", "beat": "介入", "purpose": "开始行动", "cn": "{name}找到{product_or_object}并开始解决。", "en": "{name} finds {product_or_object} and starts solving the problem."},
        {"id": "B03", "time": "10-18s", "beat": "转变", "purpose": "形成变化", "cn": "场景状态发生清晰变化。", "en": "The scene state changes clearly."},
        {"id": "B04", "time": "18-25s", "beat": "验证", "purpose": "证明结果", "cn": "目标用户看到结果并放松。", "en": "The target user sees the result and relaxes."},
        {"id": "B05", "time": "25-30s", "beat": "收束", "purpose": "留下记忆点", "cn": "{name}和{product_or_object}在最终画面中形成记忆。", "en": "{name} and {product_or_object} form the final memory point."},
    ]
