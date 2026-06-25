"""Pipeline 3: Visual, world, costume, and prop design."""

from __future__ import annotations

from typing import Any, Dict


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    ip = state["IP_UNDERSTANDING"]["ip_profile"]
    rules = state["IP_UNDERSTANDING"]["fixed_rules"]
    ip_bible = state["IP_BIBLE_BUILDER"]["ip_bible"]
    compliance = state["COMPLIANCE_REVIEW"]
    template = state.get("template", {})
    design_strategy = state["INPUT_COMPILER"]["compiled_brief"].get("design_strategy", {})
    visual_contracts = state.get("visual_contracts", {})
    visual_specs = template.get("visual_specs", {})
    name = ip["name"]
    product = ip.get("product") or "care product"
    anchors = ip_bible["visual_lock"]["must_keep"]

    style_lock = {
        "palette": visual_specs.get("palette", "warm clean color palette"),
        "lighting": visual_specs.get("lighting", "soft cinematic light"),
        "material": visual_specs.get("material", "clean tactile material"),
        "style": visual_specs.get("style", "cinematic 3D character design"),
    }

    asset_specs = _build_asset_specs(visual_contracts)
    prompt_blocks = _build_prompt_blocks(name, product, ip, rules, style_lock, anchors, compliance, design_strategy)
    image_prompts = _build_image_prompts(prompt_blocks, asset_specs)

    return {
        "pipeline": "VISUAL_DESIGN",
        "style_lock": style_lock,
        "asset_specs": asset_specs,
        "prompt_blocks": prompt_blocks,
        "image_prompts": image_prompts,
        "reference_plan": {
            "seedance_20": "Use 3-5 key reference images: character asset, scene board, prop board, final storyboard.",
            "seedance_25": "Use up to 50 references if needed, but keep one identity board and one execution storyboard as the highest-priority references.",
        },
        "prompt_usage": "Generate image boards first, then use selected boards as Seedance references.",
    }


def _build_asset_specs(visual_contracts: Dict[str, Any]) -> Dict[str, Any]:
    return visual_contracts.get("asset_views", {})


def _build_prompt_blocks(
    name: str,
    product: str,
    ip: Dict[str, Any],
    rules: Dict[str, Any],
    style_lock: Dict[str, str],
    anchors: list[str],
    compliance: Dict[str, Any],
    design_strategy: Dict[str, Any],
) -> Dict[str, str]:
    return {
        "subject": f"{name}, {ip.get('description')}",
        "fixed_identity_anchors": ", ".join(anchors),
        "research_visual_direction": design_strategy.get("visual_direction", ""),
        "audience_taste": design_strategy.get("audience_taste", ""),
        "environment": design_strategy.get("visual_direction") or "a coherent production world matching the selected template and audience context",
        "action_state": f"{name} supports the target user while {product} remains an action-related object",
        "composition": "clean production design layout, readable silhouette, clear reference duty",
        "lighting": style_lock["lighting"],
        "material": style_lock["material"],
        "camera": "front, side, back, wide, medium, close-up, and macro views as required by the asset type",
        "continuity_rule": rules.get("silhouette", ""),
        "negative_constraints": "；".join(compliance.get("hard_rules", []) + compliance.get("blocked_claims", [])),
        "style": style_lock["style"],
        "palette": style_lock["palette"],
    }


def _build_image_prompts(prompt_blocks: Dict[str, str], asset_specs: Dict[str, Any]) -> Dict[str, str]:
    character_panels = ", ".join(asset_specs.get("character_asset_board", {}).get("required_panels", []))
    scene_panels = ", ".join(asset_specs.get("scene_9_grid", {}).get("required_panels", []))
    prop_panels = ", ".join(asset_specs.get("prop_board", {}).get("required_panels", []))
    storyboard_panels = ", ".join(asset_specs.get("storyboard_board", {}).get("required_panels", []))

    return {
        "character_asset_board_cn": (
            f"角色资产板。主体：{prompt_blocks['subject']}。必须保留身份锚点：{prompt_blocks['fixed_identity_anchors']}。"
            f"面板：{character_panels}。构图：{prompt_blocks['composition']}。"
            f"色彩：{prompt_blocks['palette']}。光线：{prompt_blocks['lighting']}。材质：{prompt_blocks['material']}。"
            f"连续性：{prompt_blocks['continuity_rule']}。禁止：{prompt_blocks['negative_constraints']}。"
        ),
        "character_asset_board_en": (
            f"Character asset board. Subject: {prompt_blocks['subject']}. Fixed identity anchors: {prompt_blocks['fixed_identity_anchors']}. "
            f"Panels: {character_panels}. Composition: {prompt_blocks['composition']}. Palette: {prompt_blocks['palette']}. "
            f"Lighting: {prompt_blocks['lighting']}. Material: {prompt_blocks['material']}. Continuity: {prompt_blocks['continuity_rule']}. "
            f"Negative constraints: {prompt_blocks['negative_constraints']}."
        ),
        "scene_9_grid_cn": (
            f"场景九宫格。环境：{prompt_blocks['environment']}。面板：{scene_panels}。"
            f"主体和产品关系：{prompt_blocks['action_state']}。风格：{prompt_blocks['style']}。"
            f"统一色彩和光照：{prompt_blocks['palette']}，{prompt_blocks['lighting']}。禁止：{prompt_blocks['negative_constraints']}。"
        ),
        "scene_9_grid_en": (
            f"Nine-grid scene board. Environment: {prompt_blocks['environment']}. Panels: {scene_panels}. "
            f"Subject/product relation: {prompt_blocks['action_state']}. Style: {prompt_blocks['style']}. "
            f"Consistent palette and lighting: {prompt_blocks['palette']}, {prompt_blocks['lighting']}. Negative constraints: {prompt_blocks['negative_constraints']}."
        ),
        "prop_board_cn": (
            f"道具板。面板：{prop_panels}。动作状态：{prompt_blocks['action_state']}。"
            f"材质：{prompt_blocks['material']}。禁止把产品做成漂浮 LOGO，禁止危险使用方式。"
        ),
        "prop_board_en": (
            f"Prop board. Panels: {prop_panels}. Action state: {prompt_blocks['action_state']}. "
            f"Material: {prompt_blocks['material']}. Do not turn the product into a floating logo. No unsafe use."
        ),
        "storyboard_board_cn": (
            f"故事板。面板：{storyboard_panels}。每格必须包含主体、动作、镜头方向、产品位置、情绪变化、首末帧状态。"
            f"身份锚点必须可见：{prompt_blocks['fixed_identity_anchors']}。"
        ),
        "storyboard_board_en": (
            f"Storyboard board. Panels: {storyboard_panels}. Every panel must include subject, action, camera direction, product position, emotional change, first and last frame state. "
            f"Identity anchors must remain visible: {prompt_blocks['fixed_identity_anchors']}."
        ),
    }
