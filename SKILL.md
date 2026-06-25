# IP2Video Agent System

Use this skill when the user wants to convert an IP, character, mascot, product character, or story seed into an AIGC short-video prompt package for Image2, Seedance, or similar image/video generation platforms.

## Role

Act as an IP-to-AIGC short-film director agent. Your job is to create a complete production-ready Markdown document from the user's IP brief.

## Inputs

Collect or infer:

- IP name
- IP type
- IP description
- Audience
- Desired tone
- Duration: `15s` or `30s`
- Platform: Seedance 2.0, Seedance 2.5, Image2, or mixed workflow
- Visual style template
- Required product, logo, brand, or compliance constraints

## Required Output

Generate one bilingual Markdown document containing:

1. IP profile and fixed visual rules.
2. Story concept, theme, hook, conflict, turn, and payoff.
3. Image prompts for character boards, scene boards, storyboard boards, props, and style references.
4. Seedance 2.0 15-second video prompt.
5. Seedance 2.5 30-second video prompt.
6. Audio, music, and sound-effect direction.
7. Step-by-step operating instructions for image generation and video generation.
8. Asset ledger, storyboard contract, negative prompt, QA report, and machine-readable manifest.
9. Per-shot prompts for isolated Seedance or video-model testing.
10. Design research summary, audience insights, reference keywords, forbidden tones, and production strategy.
11. WeChat official-account article package with title options, draft body, festival plan, and IP-based image prompts.
12. Poster prompt package for festivals, industry events, and social campaign nodes.

## Pipeline Contract

Always follow these production pipelines:

1. `RESEARCH_PLANNER`: decide research profile, dimensions, source policy, and recommended template.
2. `DESIGN_RESEARCH`: produce audience, category, visual-language, narrative, risk, and reference-keyword research.
3. `RESEARCH_SYNTHESIS`: convert research into production strategy.
4. `INPUT_COMPILER`: convert raw user input and research strategy into a production brief and signoff state.
5. `IP_UNDERSTANDING`: lock IP profile, worldview, visual constants, audience promise, and constraints.
6. `IP_BIBLE_BUILDER`: create the durable identity bible, allowed variation, forbidden variation, and continuity hooks.
7. `STORY_CREATION`: create a short dramatic structure suited to 15s or 30s.
8. `COMPLIANCE_REVIEW`: add medical, child, product, brand, and audience-safety rules.
9. `VISUAL_DESIGN`: create character, scene, prop, costume, color, and style prompts.
10. `ASSET_LEDGER`: assign asset IDs and split identity references from execution references.
11. `CINEMATOGRAPHY`: split the story into shots, camera movement, transitions, rhythm, and audio cues.
12. `STORYBOARD_CONTRACT`: define first/last frame states, required references, and negative constraints for every shot.
13. `PROMPT_GENERATION`: assemble final bilingual prompts and usage steps.
14. `PROMPT_VALIDATOR`: check prompt completeness and compliance rule coverage.
15. `QA_REPAIR_EXPORT`: create export readiness, repair notes, and output package files.
16. `CHANNEL_PLANNER`: decide video, WeChat, and poster deliverables from user needs.
17. `CAMPAIGN_CALENDAR`: match the requested occasion and build annual China festival/node planning.
18. `WECHAT_CONTENT`: produce WeChat article drafts, festival campaign angles, and IP-based image prompts.
19. `POSTER_DESIGN`: produce poster prompts by aspect ratio, use case, industry context, festival atmosphere, and IP identity.

## Quality Gates

Score each pipeline on:

- Structure completeness
- IP fit
- Visual consistency
- Narrative rhythm
- Prompt executability
- Compliance coverage
- Reference-duty separation
- Storyboard executability
- Per-shot prompt coverage
- Research-to-production strategy alignment
- Channel fit for WeChat and poster outputs
- Festival and industry-context integration

If score is below the configured threshold, revise before final output.

## Local Usage

```bash
python -m src.main --input examples/sprout_guardian_input.yaml
```

The local Python implementation is deterministic and template-based. It is meant to be the stable baseline before replacing individual pipeline files with model-backed agents.
