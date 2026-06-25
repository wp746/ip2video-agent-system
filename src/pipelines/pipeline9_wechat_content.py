"""Pipeline 9: Generate WeChat official-account content package."""

from __future__ import annotations

from typing import Any, Dict, List


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    brief = state["INPUT_COMPILER"]["compiled_brief"]
    ip_bible = state["IP_BIBLE_BUILDER"]["ip_bible"]
    research = state["RESEARCH_SYNTHESIS"]["design_strategy"]
    campaign = state["CAMPAIGN_CALENDAR"]["campaign_focus"]
    strategy = state.get("channel_strategy", {}).get("wechat", {})
    image_plan = strategy.get("directions", {}).get("fuzzy_need", {}).get("image_plan", [])

    article_draft = _article_draft(brief, research, campaign)
    festival_plan = _festival_plan(brief, campaign, research)
    image_prompts = _image_prompts(brief, ip_bible, campaign, image_plan)

    return {
        "pipeline": "WECHAT_CONTENT",
        "wechat_package": {
            "general_direction": "fuzzy_need",
            "festival_direction": "festival_campaign",
            "no_ai_voice_rules": strategy.get("directions", {}).get("fuzzy_need", {}).get("tone_rules", []),
            "annual_node_usage": "Use annual_calendar to create a monthly editorial plan.",
        },
        "article_draft": article_draft,
        "festival_content_plan": festival_plan,
        "image_prompts": image_prompts,
        "prompt_usage": "Use this package for official-account writing and IP-based article illustrations.",
    }


def _article_draft(brief: Dict[str, Any], research: Dict[str, Any], campaign: Dict[str, Any]) -> Dict[str, Any]:
    ip_name = brief["ip_name"]
    product = brief.get("product") or "这件事"
    occasion = campaign.get("occasion") or "日常关怀"
    return {
        "title_options": [
            f"{occasion}，{ip_name}想把这份关心说得具体一点",
            f"别急着勇敢，先让{ip_name}陪你把步骤看清楚",
            f"有些照顾，不需要很大声，但要刚刚好",
        ],
        "subtitle": f"一篇结合 {brief['audience']}、行业关怀和 IP 叙事的公众号内容草案。",
        "opening": f"很多时候，用户需要的不是一句口号，而是一个能把复杂事情讲清楚的陪伴者。{ip_name}的作用，就是把紧张、陌生或不好开口的场景，变成一步一步能理解的行动。",
        "sections": [
            {
                "heading": "先看见真实场景，而不是先讲道理",
                "body": f"在{brief['audience']}的语境里，真正有用的内容要从一个具体场景开始：看到{product}时的迟疑、家人想帮忙却不知道怎么开口、专业信息太多带来的不确定感。",
            },
            {
                "heading": f"{ip_name}要做的是把关心变成动作",
                "body": f"它不是替用户做决定，也不是把问题说得很轻。它更像一个小小的提示灯，把下一步放到用户眼前：先看见、再理解、然后完成。",
            },
            {
                "heading": "行业内容要有温度，也要有边界",
                "body": f"这类内容最怕写成万能鸡汤。真正可信的表达，是承认用户的顾虑，同时给出清楚、不过度承诺的行动提示。调研建议的叙事方向是：{research.get('story_direction', '')}",
            },
            {
                "heading": "把节日情绪落到一个具体瞬间",
                "body": campaign.get("industry_integration", "如果遇到节日节点，就让节日符号服务真实关怀，而不是只换一张节日皮肤。"),
            },
        ],
        "closing": f"好的 IP 内容，不是把{ip_name}放在每一张图里刷存在感，而是让用户在需要被理解的时刻，真的记住它。",
    }


def _festival_plan(brief: Dict[str, Any], campaign: Dict[str, Any], research: Dict[str, Any]) -> Dict[str, Any]:
    occasion = campaign.get("occasion") or "全年节点"
    symbols = campaign.get("visual_symbols", [])
    return {
        "occasion": occasion,
        "content_hook": f"把「{campaign.get('audience_emotion', '节点情绪')}」翻译成 {brief['ip_name']} 能完成的一个小动作。",
        "industry_angle": campaign.get("industry_integration", ""),
        "ip_integration": f"{brief['ip_name']}作为陪伴者出现，用身份锚点承接节日符号：{', '.join(symbols)}。",
        "suggested_article_titles": [
            f"{occasion}，把这份关心包进一个具体动作里",
            f"{brief['ip_name']}的{occasion}提醒：别把照顾只留在祝福里",
            f"今天不说大道理，只把一件小事做好",
        ],
        "avoid": campaign.get("forbidden_tones", []) + research.get("forbidden_tones", []),
    }


def _image_prompts(
    brief: Dict[str, Any],
    ip_bible: Dict[str, Any],
    campaign: Dict[str, Any],
    image_plan: List[str],
) -> Dict[str, str]:
    anchors = ", ".join(ip_bible["visual_lock"]["must_keep"])
    symbols = ", ".join(campaign.get("visual_symbols", []))
    occasion = campaign.get("occasion") or "日常内容"
    return {
        slot: (
            f"公众号配图，{brief['ip_name']}，身份锚点：{anchors}，主题：{occasion}，"
            f"节日/节点符号：{symbols}，行业语境清晰，画面温暖克制，预留文字区域，不能像通用节日模板。"
        )
        for slot in image_plan
    }
