"""Pipeline loading and execution."""

from __future__ import annotations

from importlib import import_module
from typing import Any, Dict, Iterable, List


PIPELINE_MODULES = {
    "RESEARCH_PLANNER": "src.pipelines.pipeline00_research_planner",
    "DESIGN_RESEARCH": "src.pipelines.pipeline00b_design_research",
    "RESEARCH_SYNTHESIS": "src.pipelines.pipeline00c_research_synthesis",
    "INPUT_COMPILER": "src.pipelines.pipeline0_input_compiler",
    "IP_UNDERSTANDING": "src.pipelines.pipeline1_ip_understanding",
    "IP_BIBLE_BUILDER": "src.pipelines.pipeline1b_ip_bible_builder",
    "STORY_CREATION": "src.pipelines.pipeline2_story_creation",
    "COMPLIANCE_REVIEW": "src.pipelines.pipeline2b_compliance_review",
    "VISUAL_DESIGN": "src.pipelines.pipeline3_visual_design",
    "ASSET_LEDGER": "src.pipelines.pipeline3b_asset_ledger",
    "CINEMATOGRAPHY": "src.pipelines.pipeline4_cinematography",
    "STORYBOARD_CONTRACT": "src.pipelines.pipeline4b_storyboard_contract",
    "PROMPT_GENERATION": "src.pipelines.pipeline5_prompt_generation",
    "PROMPT_VALIDATOR": "src.pipelines.pipeline5b_prompt_validator",
    "QA_REPAIR_EXPORT": "src.pipelines.pipeline6_qa_repair_export",
    "CHANNEL_PLANNER": "src.pipelines.pipeline7_channel_planner",
    "CAMPAIGN_CALENDAR": "src.pipelines.pipeline8_campaign_calendar",
    "WECHAT_CONTENT": "src.pipelines.pipeline9_wechat_content",
    "POSTER_DESIGN": "src.pipelines.pipeline10_poster_design",
    "CLIENT_CASE_PLAN": "src.pipelines.pipeline11_client_case_plan",
}


class PipelineManager:
    def __init__(self, pipeline_keys: Iterable[str] | None = None):
        self.pipeline_keys: List[str] = list(pipeline_keys or PIPELINE_MODULES.keys())

    def run_pipeline(self, key: str, state: Dict[str, Any]) -> Dict[str, Any]:
        if key not in PIPELINE_MODULES:
            raise KeyError(f"Unknown pipeline: {key}")
        module = import_module(PIPELINE_MODULES[key])
        return module.run(state)

    def run_all(self, state: Dict[str, Any]) -> Dict[str, Any]:
        for key in self.pipeline_keys:
            state[key] = self.run_pipeline(key, state)
        return state
