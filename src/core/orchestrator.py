"""Orchestrates the IP2Video production pipelines."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import yaml

from src.core.pipeline_manager import PipelineManager
from src.core.scoring_engine import ScoringEngine
from src.output.markdown_generator import MarkdownGenerator
from src.output.package_writer import PackageWriter


class Orchestrator:
    def __init__(self, root: Path, config: Dict[str, Any]):
        self.root = root
        self.config = config
        self.pipeline_manager = PipelineManager()
        threshold = int(config.get("scoring", {}).get("threshold", 95))
        self.scoring_engine = ScoringEngine(threshold=threshold)

    def run(self, request: Dict[str, Any], output_path: str | None = None) -> str:
        state = self._initial_state(request)
        max_retries = int(self.config.get("max_retries", 3))

        for pipeline_key in self.pipeline_manager.pipeline_keys:
            for attempt in range(1, max_retries + 1):
                content = self.pipeline_manager.run_pipeline(pipeline_key, state)
                score, dimensions, missing = self.scoring_engine.score(pipeline_key, content)
                content["_score"] = score
                content["_score_dimensions"] = dimensions
                content["_missing"] = list(missing)
                content["_attempt"] = attempt
                state[pipeline_key] = content
                if pipeline_key == "INPUT_COMPILER":
                    self._refresh_runtime_from_compiled_brief(state)
                if self.scoring_engine.passed(score) or attempt == max_retries:
                    break

        generator = MarkdownGenerator(state=state, config=self.config)
        path = output_path or self._default_output_path(state)
        markdown_content = generator.generate()
        saved_path = generator.save(path, content=markdown_content)
        bundle = PackageWriter(state=state, markdown_content=markdown_content).save_bundle(saved_path)
        state["EXPORT_BUNDLE"] = bundle
        return saved_path

    def _initial_state(self, request: Dict[str, Any]) -> Dict[str, Any]:
        template_id = request.get("request", {}).get("style_template_id") or self.config.get("default_template_id")
        duration = request.get("ip_input", {}).get("duration") or self.config.get("default_duration", "30s")
        universe_id = request.get("request", {}).get("universe_id", "health_heroes")

        template = self._load_optional_yaml(self.root / "templates" / f"{template_id}.yaml")
        universe = self._load_optional_yaml(self.root / "universe" / f"{universe_id}_universe.yaml")
        crossover = self._load_optional_yaml(self.root / "universe" / "crossover_rules.yaml")
        story_archetypes = self._load_optional_yaml(self.root / "config" / "story_archetypes.yaml")
        visual_contracts = self._load_optional_yaml(self.root / "config" / "visual_spec_contracts.yaml")
        design_research_framework = self._load_optional_yaml(self.root / "config" / "design_research_framework.yaml")
        campaign_calendar = self._load_optional_yaml(self.root / "config" / "campaign_calendar.yaml")
        channel_strategy = self._load_optional_yaml(self.root / "config" / "channel_strategy.yaml")

        return {
            "request": request,
            "config": self.config,
            "template_id": template_id,
            "duration": duration,
            "template": template,
            "universe": universe,
            "crossover_rules": crossover,
            "story_archetypes": story_archetypes,
            "visual_contracts": visual_contracts,
            "design_research_framework": design_research_framework,
            "campaign_calendar": campaign_calendar,
            "channel_strategy": channel_strategy,
        }

    def _refresh_runtime_from_compiled_brief(self, state: Dict[str, Any]) -> None:
        compiled = state["INPUT_COMPILER"]["compiled_brief"]
        template_id = compiled.get("template_id") or state["template_id"]
        duration = compiled.get("duration") or state["duration"]
        if template_id != state["template_id"]:
            state["template_id"] = template_id
            state["template"] = self._load_optional_yaml(self.root / "templates" / f"{template_id}.yaml")
        state["duration"] = duration

    @staticmethod
    def _load_optional_yaml(path: Path) -> Dict[str, Any]:
        if not path.exists():
            return {}
        with path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}
        if not isinstance(data, dict):
            raise ValueError(f"YAML root must be a mapping: {path}")
        return data

    def _default_output_path(self, state: Dict[str, Any]) -> str:
        output_dir = self.root / self.config.get("paths", {}).get("output_dir", "./output")
        ip_name = state["request"].get("ip_input", {}).get("name", "ip")
        slug = self._slugify(ip_name)
        return str(output_dir / f"{slug}_{state['duration']}_prompt_pack.md")

    @staticmethod
    def _slugify(value: str) -> str:
        keep = []
        for char in value.lower():
            if char.isalnum():
                keep.append(char)
            elif char in {" ", "-", "_"}:
                keep.append("_")
        slug = "".join(keep).strip("_")
        return slug or "ip"
