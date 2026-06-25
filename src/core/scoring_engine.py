"""Deterministic scoring gates for pipeline outputs."""

from __future__ import annotations

from typing import Any, Dict, Iterable, Tuple


REQUIRED_KEYS = {
    "RESEARCH_PLANNER": ["research_plan", "profile_summary"],
    "DESIGN_RESEARCH": ["design_research", "research_summary"],
    "RESEARCH_SYNTHESIS": ["design_strategy", "synthesis_signoff"],
    "INPUT_COMPILER": ["compiled_brief", "signoff", "production_intent"],
    "IP_UNDERSTANDING": ["ip_profile", "fixed_rules", "audience_promise"],
    "IP_BIBLE_BUILDER": ["ip_bible", "identity_lock"],
    "STORY_CREATION": ["logline_cn", "logline_en", "story_beats", "theme", "archetype", "story_constraints"],
    "COMPLIANCE_REVIEW": ["risk_flags", "hard_rules", "signoff"],
    "VISUAL_DESIGN": ["image_prompts", "style_lock", "reference_plan", "asset_specs", "prompt_blocks"],
    "ASSET_LEDGER": ["asset_ledger", "reference_duty", "asset_signoff"],
    "CINEMATOGRAPHY": ["shots", "audio_direction", "seedance_notes"],
    "STORYBOARD_CONTRACT": ["shot_contract", "shot_prompt_pack", "storyboard_signoff"],
    "PROMPT_GENERATION": ["seedance_20_15s", "seedance_25_30s", "usage_steps"],
    "PROMPT_VALIDATOR": ["status", "validations", "negative_prompt"],
    "QA_REPAIR_EXPORT": ["status", "export_files", "qa_summary"],
    "CHANNEL_PLANNER": ["channel_plan", "requested_channels"],
    "CAMPAIGN_CALENDAR": ["annual_calendar", "campaign_focus"],
    "WECHAT_CONTENT": ["wechat_package", "article_draft", "image_prompts"],
    "POSTER_DESIGN": ["poster_package", "poster_prompts"],
}


class ScoringEngine:
    def __init__(self, threshold: int = 95):
        self.threshold = threshold

    def score(self, pipeline_key: str, content: Dict[str, Any]) -> Tuple[int, Dict[str, int], Iterable[str]]:
        missing = [key for key in REQUIRED_KEYS.get(pipeline_key, []) if not content.get(key)]
        if not missing:
            dimensions = {
                "structure": 20,
                "ip_fit": 20,
                "visual_consistency": 20,
                "rhythm": 20,
                "prompt_executability": 20,
            }
            return 100, dimensions, missing

        dimensions = {
            "structure": 20 if not missing else max(0, 20 - 6 * len(missing)),
            "ip_fit": self._score_text_presence(content, ["ip", "name", "character", "角色", "IP"]),
            "visual_consistency": self._score_text_presence(content, ["visual", "style", "color", "镜头", "视觉"]),
            "rhythm": self._score_text_presence(content, ["beat", "shot", "duration", "节奏", "秒"]),
            "prompt_executability": self._score_text_presence(content, ["prompt", "Seedance", "使用", "生成"]),
        }
        total = sum(dimensions.values())
        return total, dimensions, missing

    def passed(self, score: int) -> bool:
        return score >= self.threshold

    @staticmethod
    def _score_text_presence(content: Dict[str, Any], needles: Iterable[str]) -> int:
        text = str(content)
        hits = sum(1 for needle in needles if needle in text)
        if hits >= 2:
            return 20
        if hits == 1:
            return 16
        return 12
