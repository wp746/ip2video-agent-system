"""Write machine-readable production package files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import yaml


class PackageWriter:
    def __init__(self, state: Dict[str, Any], markdown_content: str):
        self.state = state
        self.markdown_content = markdown_content

    def save_bundle(self, markdown_path: str) -> Dict[str, str]:
        md_path = Path(markdown_path)
        bundle_dir = md_path.with_suffix("")
        bundle_dir.mkdir(parents=True, exist_ok=True)

        files = {
            "final_prompt_pack.md": self.markdown_content,
            "production_manifest.json": self._manifest_json(),
            "client_case_plan.yaml": self._yaml(self.state["CLIENT_CASE_PLAN"]),
            "client_case_plan.md": self._client_case_plan_markdown(),
            "channel_plan.yaml": self._yaml(self.state["CHANNEL_PLANNER"]["channel_plan"]),
            "campaign_calendar.yaml": self._yaml(self.state["CAMPAIGN_CALENDAR"]["annual_calendar"]),
            "wechat_content.yaml": self._yaml(self.state["WECHAT_CONTENT"]),
            "wechat_content.md": self._wechat_markdown(),
            "poster_prompts.yaml": self._yaml(self.state["POSTER_DESIGN"]["poster_prompts"]),
            "poster_prompts.md": self._poster_markdown(),
            "asset_ledger.yaml": self._yaml(self.state["ASSET_LEDGER"]["asset_ledger"]),
            "shot_contract.yaml": self._yaml(self.state["STORYBOARD_CONTRACT"]["shot_contract"]),
            "shot_prompts.yaml": self._yaml(self.state["STORYBOARD_CONTRACT"]["shot_prompt_pack"]),
            "shot_prompts.md": self._shot_prompts_markdown(),
            "negative_prompts.md": self.state["PROMPT_VALIDATOR"]["negative_prompt"] + "\n",
            "qa_report.md": self._qa_report(),
            "seedance_2_0_15s.txt": self.state["PROMPT_GENERATION"]["seedance_20_15s"] + "\n",
            "seedance_2_5_30s.txt": self.state["PROMPT_GENERATION"]["seedance_25_30s"] + "\n",
        }

        written = {}
        for filename, content in files.items():
            path = bundle_dir / filename
            path.write_text(content, encoding="utf-8")
            written[filename] = str(path)
        return written

    def _manifest_json(self) -> str:
        brief = self.state["INPUT_COMPILER"]["compiled_brief"]
        manifest = {
            "ip": brief,
            "research": {
                "plan": self.state["RESEARCH_PLANNER"]["research_plan"],
                "design_research": self.state["DESIGN_RESEARCH"]["design_research"],
                "design_strategy": self.state["RESEARCH_SYNTHESIS"]["design_strategy"],
                "synthesis_signoff": self.state["RESEARCH_SYNTHESIS"]["synthesis_signoff"],
            },
            "template_id": self.state["template_id"],
            "duration": self.state["duration"],
            "ip_bible": self.state["IP_BIBLE_BUILDER"]["ip_bible"],
            "story": {
                "archetype": self.state["STORY_CREATION"]["archetype"],
                "theme": self.state["STORY_CREATION"]["theme"],
                "emotional_curve": self.state["STORY_CREATION"].get("emotional_curve", ""),
                "beats": self.state["STORY_CREATION"]["story_beats"],
                "constraints": self.state["STORY_CREATION"]["story_constraints"],
            },
            "visual": {
                "style_lock": self.state["VISUAL_DESIGN"]["style_lock"],
                "prompt_blocks": self.state["VISUAL_DESIGN"]["prompt_blocks"],
                "asset_specs": self.state["VISUAL_DESIGN"]["asset_specs"],
            },
            "compliance": {
                "risk_flags": self.state["COMPLIANCE_REVIEW"]["risk_flags"],
                "hard_rules": self.state["COMPLIANCE_REVIEW"]["hard_rules"],
                "blocked_claims": self.state["COMPLIANCE_REVIEW"]["blocked_claims"],
            },
            "reference_duty": self.state["ASSET_LEDGER"]["reference_duty"],
            "storyboard_signoff": self.state["STORYBOARD_CONTRACT"]["storyboard_signoff"],
            "shot_prompt_pack": self.state["STORYBOARD_CONTRACT"]["shot_prompt_pack"],
            "channels": {
                "channel_plan": self.state["CHANNEL_PLANNER"]["channel_plan"],
                "campaign_focus": self.state["CAMPAIGN_CALENDAR"]["campaign_focus"],
                "annual_calendar": self.state["CAMPAIGN_CALENDAR"]["annual_calendar"],
                "wechat_content": self.state["WECHAT_CONTENT"]["wechat_package"],
                "poster_package": self.state["POSTER_DESIGN"]["poster_package"],
            },
            "qa_summary": self.state["QA_REPAIR_EXPORT"]["qa_summary"],
            "client_case_plan": self.state["CLIENT_CASE_PLAN"]["case_plan"],
            "verification_matrix": self.state["CLIENT_CASE_PLAN"]["verification_matrix"],
        }
        return json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"

    def _client_case_plan_markdown(self) -> str:
        client = self.state["CLIENT_CASE_PLAN"]
        tone = client["research_tone_summary"]
        plan = client["case_plan"]
        matrix = client["verification_matrix"]
        lines = [
            "# Client Full Case Plan",
            "",
            "## Research Tone Summary",
            "",
            f"- Core tone: {tone['core_tone']}",
            "",
            "### Adoptable Expression",
            "",
        ]
        lines.extend(f"- {item}" for item in tone.get("adoptable_expression", []))
        lines.extend(["", "### Local Reference Reading", ""])
        lines.extend(f"- {item}" for item in tone.get("local_reference_reading", []))
        lines.extend(["", "### Forbidden Tones", ""])
        lines.extend(f"- {item}" for item in tone.get("forbidden_tones", []))
        lines.extend(
            [
                "",
                "## Case Plan",
                "",
                f"- Current test node: {plan['current_test_node']}",
                f"- Communication proposition: {plan['communication_proposition']}",
                "",
                "### Strategic Axis",
                "",
            ]
        )
        lines.extend(f"- {item}" for item in plan.get("strategic_axis", []))
        lines.extend(["", "### Channel Architecture", ""])
        for channel, item in plan.get("channel_architecture", {}).items():
            lines.extend(
                [
                    f"#### {channel}",
                    "",
                    f"- Role: {item['role']}",
                    f"- First test: {item['first_test']}",
                    f"- Must have: {'；'.join(item['must_have'])}",
                    "",
                ]
            )
        lines.extend(["## Annual Node Strategy", ""])
        for item in plan.get("annual_node_strategy", []):
            lines.append(f"- {item['node']} ({item['date_rule']}): {item['role']}；{item['angle']}")
        lines.extend(["", "## First Round Delivery", ""])
        lines.extend(f"- {item['item']}: {item['output']}" for item in plan.get("first_round_delivery", []))
        lines.extend(["", "## Client Review Order", ""])
        lines.extend(f"{index}. {item}" for index, item in enumerate(plan.get("client_review_order", []), start=1))
        lines.extend(["", "## Verification Matrix", ""])
        for item in matrix:
            lines.extend(
                [
                    f"### {item['channel']}",
                    "",
                    f"- Artifact: {item['artifact']}",
                    f"- Sample evidence: {item['sample_evidence']}",
                    "- Checks:",
                ]
            )
            lines.extend(f"  - {check}" for check in item.get("checks", []))
            lines.append("")
        return "\n".join(lines)

    def _wechat_markdown(self) -> str:
        wechat = self.state["WECHAT_CONTENT"]
        article = wechat["article_draft"]
        festival = wechat["festival_content_plan"]
        lines = [
            "# WeChat Official Account Package",
            "",
            "## Title Options",
            "",
        ]
        lines.extend(f"- {title}" for title in article["title_options"])
        lines.extend(
            [
                "",
                f"## Subtitle",
                "",
                article["subtitle"],
                "",
                "## Opening",
                "",
                article["opening"],
                "",
                "## Body",
                "",
            ]
        )
        for section in article["sections"]:
            lines.extend([f"### {section['heading']}", "", section["body"], ""])
        lines.extend(
            [
                "## Closing",
                "",
                article["closing"],
                "",
                "## Festival Campaign Plan",
                "",
                f"- Occasion: {festival['occasion']}",
                f"- Hook: {festival['content_hook']}",
                f"- Industry angle: {festival['industry_angle']}",
                f"- IP integration: {festival['ip_integration']}",
                "",
                "## Image Prompts",
                "",
            ]
        )
        for slot, prompt in wechat["image_prompts"].items():
            lines.extend([f"### {slot}", "", prompt, ""])
        return "\n".join(lines)

    def _poster_markdown(self) -> str:
        lines = ["# Poster Prompt Package", ""]
        for key, item in self.state["POSTER_DESIGN"]["poster_prompts"].items():
            lines.extend(
                [
                    f"## {key}",
                    "",
                    f"- Ratio: {item['ratio']}",
                    f"- Usage: {item['usage']}",
                    f"- Headline direction: {item['headline_direction']}",
                    f"- Weibo caption: {item.get('weibo_caption', '')}",
                    "",
                    "### CN Prompt",
                    "",
                    item["prompt_cn"],
                    "",
                    "### EN Prompt",
                    "",
                    item["prompt_en"],
                    "",
                ]
            )
        return "\n".join(lines)

    def _shot_prompts_markdown(self) -> str:
        lines = ["# Shot Prompts", ""]
        for shot_id, prompt in self.state["STORYBOARD_CONTRACT"]["shot_prompt_pack"].items():
            lines.extend([f"## {shot_id}", "", prompt, ""])
        return "\n".join(lines)

    def _qa_report(self) -> str:
        qa = self.state["QA_REPAIR_EXPORT"]
        validator = self.state["PROMPT_VALIDATOR"]
        lines = [
            "# QA Report",
            "",
            f"- Status: {qa['status']}",
            f"- Prompt validation: {qa['qa_summary']['prompt_validation']}",
            f"- Compliance: {qa['qa_summary']['compliance']}",
            f"- Asset coverage: {qa['qa_summary']['asset_coverage']}",
            "",
            "## Open Issues",
            "",
        ]
        issues = qa.get("open_issues", [])
        if issues:
            lines.extend(f"- {issue}" for issue in issues)
        else:
            lines.append("- None")
        lines.extend(["", "## Validator Details", "", self._yaml(validator)])
        return "\n".join(lines)

    @staticmethod
    def _yaml(data: Any) -> str:
        return yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
