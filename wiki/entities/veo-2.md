---
type: entity
title: Veo 2
entity_type: entity
theme_ids:
- agent_systems
- ai_business_and_economics
- ai_market_dynamics
- chain_of_thought
- computer_use_and_gui_agents
- generative_media
- model_commoditization_and_open_source
- multi_agent_coordination
- multimodal_models
- reasoning_and_planning
- software_engineering_agents
- vertical_ai_and_saas_disruption
- video_and_world_models
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0024366299938147844
staleness: 0.0
status: active
tags: []
---
# Veo 2

> Veo 2 is Google DeepMind's video generation model, announced in December 2024 and released in April 2025, marking a significant step in Google's video synthesis capabilities. It serves primarily as the baseline against which Veo 3 is benchmarked, and its comparative performance across visual reasoning tasks reveals both how far the field advanced in roughly six months and where systematic limitations persist across model generations.

**Type:** entity
**Themes:** [[themes/generative_media|Generative Media]], [[themes/video_and_world_models|Video and World Models]], [[themes/multimodal_models|Multimodal Models]], [[themes/vision_language_models|Vision Language Models]]

## Overview

Veo 2 (model ID `veo-2.0-generate-001`) was Google DeepMind's second major video generation model, entering public availability in April 2025 — approximately six months before Veo 3's July 2025 release. It emerged in the same period as broader industry acceleration in multimodal generation, alongside Google Labs operating on compressed 50–100 day development cycles. Veo 2 is less notable for what it achieved than for what it reveals through contrast: its performance profile against Veo 3 across zero-shot visual tasks provides one of the cleaner quantitative windows into the pace and direction of progress in video generation models.

## Performance Profile and Limitations

The most revealing data on Veo 2 comes from benchmarks in "Video models are zero-shot learners and reasoners", which evaluated both Veo 2 and Veo 3 on a suite of zero-shot visual reasoning tasks — tasks the models were never explicitly trained on.

On **object extraction**, Veo 2 performs at approximately chance level, while Veo 3 reaches up to 93% pass@10. On **5×5 maze solving**, Veo 2 achieves only 14% pass@10 against Veo 3's 78% — a gap that the authors attribute to advancing reasoning capabilities rather than simple generation quality improvements. On **zero-shot edge detection** (BIPEDv2), Veo 3 achieves 0.77 OIS pass@10; Veo 2's performance is not separately reported but is implicitly weaker.

These numbers suggest Veo 2 represented a generation of video models that could synthesize plausible visual content but had not yet internalized the kind of structured spatial and logical reasoning that Veo 3 began to exhibit. The improvement is not incremental — the object extraction gap in particular (chance vs. 93%) implies a qualitative shift, not just fine-tuning.

**Where both models fail equally** is the more structurally interesting finding. Both Veo 2 and Veo 3 perform *below chance* (below 0.33) on reflect and rotate visual analogies, indicating a systematic erroneous bias rather than mere underperformance. Veo 3 correctly handles color and resize transformations, so the failure is transformation-specific rather than a general reasoning deficit. This shared failure mode across model generations suggests the limitation is architectural or stems from training data distribution rather than being addressable through scale alone.

## Significance as a Baseline

Veo 2's primary scientific role is comparative. The six-month gap between its announcement (December 2024) and Veo 3's announcement (May 2025) is unusually short for a generational successor, and the performance deltas — especially on structured reasoning tasks — suggest rapid internal capability development at Google DeepMind during this period. This trajectory fits the broader pattern of Google Labs operating under aggressive speed constraints, with teams like those behind Google Mariner (built in 84 days) moving from capability observation to public product at pace.

The benchmark results also underscore a methodological point that applies beyond Veo 2 specifically: prompt design has an outsized effect on measured performance, with pass@1 differences between best and worst prompts reaching 40–64 percentage points on some tasks. This makes it difficult to treat any single reported number for Veo 2 (or Veo 3) as a stable capability assessment — the model's apparent ability is highly sensitive to how the task is framed.

## Open Questions

- Whether Veo 2's near-chance performance on object extraction reflects a fundamental absence of spatial grounding or simply inadequate prompting has not been isolated.
- The shared below-chance failure on reflect/rotate analogies across both Veo 2 and Veo 3 is unexplained — whether this is a training data artifact, an architecture constraint, or a prompt sensitivity issue remains open.
- Veo 2's capabilities in domains beyond the benchmarked tasks (e.g., long-form coherence, physics plausibility) are not well-documented in the sources present.

## Relationships

Veo 2 is the direct predecessor to Veo 3, with the two models sharing a development lineage at Google DeepMind. Its public release coincided with Google Labs' broader push toward rapid multimodal product deployment, including Google Mariner. The zero-shot benchmarking methodology used to evaluate it is documented in "Video models are zero-shot learners and reasoners"; contextual notes on Google's 2024–2025 development cadence appear in "Josh Woodward: Google Labs is Rapidly Building AI Products from 0-to-1" and "2024 Year in Review".

## Key Findings

## Limitations and Open Questions

## Sources
