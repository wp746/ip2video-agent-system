"""Pipeline 7: Plan non-video promotion channels."""

from __future__ import annotations

from typing import Any, Dict, List


def run(state: Dict[str, Any]) -> Dict[str, Any]:
    request = state["request"]
    request_meta = request.get("request", {})
    channel_strategy = state.get("channel_strategy", {})
    default_channels = channel_strategy.get("default_channels", ["video", "wechat", "poster"])
    channels = request_meta.get("channels") or request_meta.get("deliverables") or default_channels
    channels = _normalize_channels(channels)
    occasion = _extract_occasion(request, state.get("campaign_calendar", {}).get("annual_nodes", {}))

    channel_plan = {
        "mode": "MULTI_CHANNEL_PROMOTION",
        "requested_channels": channels,
        "occasion": occasion,
        "wechat_directions": ["fuzzy_need", "festival_campaign"],
        "poster_directions": ["festival_or_event_poster", "industry_campaign_poster"],
        "shared_inputs": [
            "design research",
            "IP Bible",
            "compliance rules",
            "visual prompt blocks",
            "asset ledger",
        ],
        "output_policy": "Generate video, WeChat, and poster packages from the same IP truth source.",
    }

    return {
        "pipeline": "CHANNEL_PLANNER",
        "requested_channels": channels,
        "channel_plan": channel_plan,
        "prompt_usage": "Downstream channel pipelines should only generate outputs for requested channels.",
    }


def _normalize_channels(channels) -> List[str]:
    if isinstance(channels, str):
        channels = [channels]
    alias = {
        "公众号": "wechat",
        "微信": "wechat",
        "文章": "wechat",
        "海报": "poster",
        "平面": "poster",
        "视频": "video",
    }
    result = []
    for channel in channels:
        value = alias.get(str(channel), str(channel))
        if value not in result:
            result.append(value)
    return result


def _extract_occasion(request: Dict[str, Any], annual_nodes: Dict[str, Any]) -> str:
    request_meta = request.get("request", {})
    explicit = request_meta.get("occasion") or request_meta.get("festival") or request_meta.get("event")
    if explicit:
        return str(explicit)
    text = f"{request_meta.get('goal', '')} {request.get('ip_input', {}).get('description', '')}"
    for node in annual_nodes:
        if node in text:
            return node
    return ""
