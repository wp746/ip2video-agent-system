# IP2Video Agent System

`ip2video-agent-system` is a local, reproducible agent skeleton for turning an IP concept into multi-channel AIGC promotion packets.

It is designed as an "IP -> AIGC short film director agent":

- Input: one IP concept, audience, style, duration, platform, and optional product or brand constraints.
- Output: one bilingual Markdown prompt document plus machine-readable production contracts for video, WeChat official-account content, poster prompts, assets, shots, QA, and platform prompts.
- Runtime: local Python pipeline first, LLM/API adapters later.

## Quick Start

```bash
cd ip2video-agent-system
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m src.main --input examples/sprout_guardian_input.yaml
python scripts/validate_production_package.py output/小芽守护者_30s_prompt_pack
```

The generated file will be written to `output/`.

The command also writes a production bundle beside the Markdown file:

```text
output/<ip>_<duration>_prompt_pack/
├── final_prompt_pack.md
├── production_manifest.json
├── client_case_plan.yaml
├── client_case_plan.md
├── channel_plan.yaml
├── campaign_calendar.yaml
├── wechat_content.yaml
├── wechat_content.md
├── poster_prompts.yaml
├── poster_prompts.md
├── asset_ledger.yaml
├── shot_contract.yaml
├── shot_prompts.yaml
├── shot_prompts.md
├── negative_prompts.md
├── qa_report.md
├── seedance_2_0_15s.txt
├── seedance_2_5_30s.txt
└── seedance_2_5_60s.txt
```

## Core Flow

```text
IP Input
  -> Pipeline -3: Research planner
  -> Pipeline -2: Design research
  -> Pipeline -1: Research synthesis and production strategy
  -> Pipeline 0: Input compiler and signoff
  -> Pipeline 1: IP understanding and rule locking
  -> Pipeline 1B: IP bible builder
  -> Pipeline 2: Story and script creation
  -> Pipeline 2B: Compliance review
  -> Pipeline 3: Visual, world, costume, and prop design
  -> Pipeline 3B: Asset ledger and reference-duty split
  -> Pipeline 4: Cinematography, editing rhythm, and audio direction
  -> Pipeline 4B: Storyboard contract
  -> Pipeline 5: Prompt aggregation
  -> Pipeline 5B: Prompt validator
  -> Pipeline 6: QA repair and export
  -> Pipeline 7: Channel planner
  -> Pipeline 8: Campaign calendar
  -> Pipeline 9: WeChat official-account content
  -> Pipeline 10: Poster design prompts
  -> Pipeline 11: Client full case plan and verification matrix
  -> Scoring Engine: structure, IP fit, visual consistency, rhythm, prompt executability
```

## Project Layout

```text
ip2video-agent-system/
├── README.md
├── SKILL.md
├── agents/openai.yaml
├── config/default_config.yaml
├── templates/
├── universe/
├── src/
│   ├── main.py
│   ├── core/
│   ├── pipelines/
│   ├── output/
│   └── utils/
├── examples/
└── output/
```

## Design Principles

1. Compile input before generation so downstream stages do not depend on ambiguous raw chat.
2. Lock the IP first: character identity, worldview, visual constants, brand limits, and audience promise.
3. Separate identity reference boards from execution-state storyboard boards.
4. Split image-generation prompts from video-generation prompts.
5. Keep every generated segment self-contained, especially when producing Seedance 15s or 30s prompts.
6. Run compliance, prompt validation, and QA export before using the prompts in production.

## Current Status

This version is a minimum local system. It does not call the OpenAI API or Seedance directly. Instead, it generates structured production documents from local templates so the pipeline can be inspected, improved, and versioned safely.

The next useful upgrades are:

- Add real LLM calls for each pipeline.
- Add stricter semantic prompt validators.
- Add more IP universes and style templates.
- Add a web UI for entering IP briefs and comparing versions.

## Configuration Libraries

- `config/story_archetypes.yaml`: reusable story beat grammars for `MED-A`, `KID-B`, `BRD-A`, `SUS-A`, and `INF-A`.
- `config/visual_spec_contracts.yaml`: required panels and hard constraints for character boards, scene grids, prop boards, and storyboard boards.
- `config/design_research_framework.yaml`: offline design-research profiles that map IP context to audience insights, visual language, narrative opportunities, forbidden tones, and recommended templates.
- `config/campaign_calendar.yaml`: major China campaign nodes and festivals with content angles, symbols, poster motifs, and forbidden tones.
- `config/channel_strategy.yaml`: channel rules for WeChat content and poster prompt production.

## Engineering / Maritime Case

Run the China Communications Construction test case:

```bash
python -m src.main --input examples/cccc_seafarer_campaign_input.yaml
python scripts/validate_production_package.py output/中国交建工程守护者_30s_prompt_pack
```

This profile uses `engineering_maritime` research logic and the `INF-A` template. It is designed for SOE infrastructure, port, shipping, project-site, safety-production, and official-account campaign scenarios.

The leadership-facing annual campaign plan is available at:

```text
deliverables/cccc_annual_ip_aigc_campaign_plan_2026.md
```
