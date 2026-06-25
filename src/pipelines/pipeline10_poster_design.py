"""Pipeline 10: Generate poster design prompts for events and festivals."""

from __future__ import annotations

from typing import Any, Dict


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    brief = state["INPUT_COMPILER"]["compiled_brief"]
    ip_bible = state["IP_BIBLE_BUILDER"]["ip_bible"]
    visual = state["VISUAL_DESIGN"]
    campaign = state["CAMPAIGN_CALENDAR"]["campaign_focus"]
    poster_strategy = state.get("channel_strategy", {}).get("poster", {})

    poster_prompts = _poster_prompts(brief, ip_bible, visual, campaign, poster_strategy)

    return {
        "pipeline": "POSTER_DESIGN",
        "poster_package": {
            "occasion": campaign.get("occasion") or "日常宣传",
            "count": len(poster_prompts),
            "formats": poster_strategy.get("formats", []),
            "design_rules": poster_strategy.get("design_rules", []),
        },
        "poster_prompts": poster_prompts,
        "prompt_usage": "Use poster_prompts directly in image generation tools; add final Chinese typography manually when needed.",
    }


def _poster_prompts(
    brief: Dict[str, Any],
    ip_bible: Dict[str, Any],
    visual: Dict[str, Any],
    campaign: Dict[str, Any],
    poster_strategy: Dict[str, Any],
) -> Dict[str, Dict[str, str]]:
    anchors = ", ".join(ip_bible["visual_lock"]["must_keep"])
    style = visual["style_lock"]
    occasion = campaign.get("occasion") or "品牌宣传节点"
    symbols = ", ".join(campaign.get("visual_symbols", []))
    motifs = campaign.get("poster_motifs", [])
    industry = campaign.get("industry_integration", "")
    forbidden = "；".join(campaign.get("forbidden_tones", []))
    formats = poster_strategy.get("formats", [])
    if not formats:
        formats = [{"name": "social_square", "ratio": "1:1", "usage": "social poster"}]

    variants = {}
    for index, fmt in enumerate(formats[: poster_strategy.get("default_count", 3)], start=1):
        motif = motifs[(index - 1) % len(motifs)] if motifs else f"{brief['ip_name']}与节点符号互动"
        variants[f"poster_{index}_{fmt['name']}"] = {
            "ratio": fmt.get("ratio", ""),
            "usage": fmt.get("usage", ""),
            "headline_direction": _headline_direction(occasion, brief["ip_name"], index),
            "prompt_cn": (
                f"平面宣传海报，比例 {fmt.get('ratio', '')}，主题：{occasion}。"
                f"IP：{brief['ip_name']}，必须保留身份锚点：{anchors}。"
                f"行业特点：{_clean_sentence(industry)}。节日/节点符号：{symbols}。创意画面：{motif}。"
                f"视觉风格：{style['style']}，色彩：{style['palette']}，光线：{style['lighting']}，材质：{style['material']}。"
                f"构图要求：主视觉突出 IP 和节日符号，预留清晰中文标题区和品牌署名区，适合企业公众号/朋友圈传播。"
                f"禁止：{forbidden}，不要通用模板换皮，不要让小字由模型生成，不要遮挡 IP 识别元素。"
            ),
            "prompt_en": (
                f"Poster design, aspect ratio {fmt.get('ratio', '')}, theme: {occasion}. "
                f"IP character: {brief['ip_name']}; fixed identity anchors: {anchors}. "
                f"Industry context: {_clean_sentence(industry)}. Festival/event symbols: {symbols}. Creative motif: {motif}. "
                f"Visual style: {style['style']}; palette: {style['palette']}; lighting: {style['lighting']}; material: {style['material']}. "
                "Composition: strong key visual with clear empty space for Chinese headline and brand signature, suitable for enterprise social media. "
                f"Negative constraints: {forbidden}; no generic festival template, no AI-generated small Chinese text, do not hide identity anchors."
            ),
        }
    return variants


def _headline_direction(occasion: str, ip_name: str, index: int) -> str:
    options = [
        f"{occasion}，让{ip_name}把关心送到身边",
        f"把节日祝福，变成一个具体的守护动作",
        f"今天的祝福不只好看，也要真的有用",
    ]
    return options[(index - 1) % len(options)]


def _clean_sentence(value: str) -> str:
    return value.rstrip("。.")
