---
type: entity
title: Cold-Start Phase
entity_type: method
theme_ids:
- agent_systems
- chain_of_thought
- knowledge_and_memory
- long_context_and_attention
- model_architecture
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- retrieval_augmented_generation
- reward_modeling
- rl_for_llm_reasoning
- scaling_laws
- synthetic_data_generation
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0001344489505164417
staleness: 0.0
status: active
tags: []
---
# Cold-Start Phase

> The cold-start phase is a lightweight supervised fine-tuning (SFT) stage applied to a base language model before RLPT training begins. Its sole purpose is to instill the minimum instruction-following capability required for a model to engage in next-segment reasoning tasks — bridging the gap between a raw pre-trained model and the structured prompt-response interface that reinforcement learning over pre-training data demands.

**Type:** method
**Themes:** [[themes/post_training_methods|post_training_methods]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/reasoning_and_planning|reasoning_and_planning]]

## Overview

The cold-start phase arises as a practical prerequisite for RLPT — Reinforcement Learning on Pre-Training Data — a method that dispenses with human annotation by deriving reward signals directly from the pre-training corpus itself. Rather than relying on human-labelled preferences (as RLHF does) or verifiable ground-truth answers (as RLVR does), RLPT reframes RL as a reasoning problem over raw text: the model is asked either to predict the next sentence from preceding context (Autoregressive Segment Reasoning, ASR) or to reconstruct a masked span using both preceding and following context (Middle Segment Reasoning, MSR). Reward is defined as the semantic consistency between the model's prediction and the reference segment, evaluated by a generative reward model.

The challenge is that these tasks, while grounded in pre-training objectives, are posed as instruction-following prompts. A base model straight off next-token pre-training lacks the scaffolding to interpret such prompts reliably. The cold-start phase resolves this by applying a short SFT pass on instruction-following data — not to teach reasoning, but to teach format compliance. Once that minimal capability exists, RLPT can proceed using on-policy GRPO without KL regularisation, with a batch size of 512, maximum response length of 8192, learning rate of 1×10⁻⁶, and 8 sampled outputs per prompt.

## Key Findings

The cold-start phase is less a contribution in itself than a necessary seam in a larger pipeline — but its existence reveals something important about the current state of base model training. Despite training corpora having grown from billions of tokens (BERT) to trillions (Llama), and model sizes scaling from millions to the trillion-parameter range, raw base models still cannot reliably follow structured prompts without a formatting scaffold. This is a quiet admission that instruction-following is not an emergent property of scale alone.

Once the cold-start SFT is in place, RLPT delivers substantial gains. Applied to Qwen3-4B-Base, it yields absolute improvements of 3.0, 5.1, 8.1, 6.0, 6.6, and 5.3 on MMLU, MMLU-Pro, GPQA-Diamond, KOR-Bench, AIME24, and AIME25 respectively — with similar patterns across Qwen3-8B-Base and Llama-3.2-3B-Base. The AIME results are particularly striking: improvements in Pass@1 and Pass@8 suggest that RLPT is not merely improving surface-level benchmark performance but is expanding the reasoning frontier of the base model. When RLPT-trained models are subsequently used as initialisation for RLVR, the gains stack further — an additional 2.3 and 1.3 in Pass@1, and 3.7 and 2.0 in Pass@8, on AIME24 and AIME25 — indicating that the cold-start SFT → RLPT path produces a stronger foundation for downstream RL than raw base models do.

This pattern has an analogue in search agent training: the DeepDive-32B system uses SFT as a foundation before multi-turn RL, with the SFT-only model scoring 9.5% on BrowseComp and RL raising it to 15.3%. The cold-start dynamic — SFT establishes capability floors, RL extends ceilings — appears to be a recurring structural feature across RL-for-reasoning pipelines.

## Limitations and Open Questions

The cold-start phase introduces a dependency that RLPT's authors presumably wanted to avoid: instruction-following data, even if minimal, must come from somewhere. The paper does not specify the source, scale, or composition of the SFT dataset used, which makes it unclear whether the gains attributed to RLPT are fully cleanly separable from the cold-start SFT itself. If the SFT data is domain-adjacent to the evaluation benchmarks, some of the downstream improvement may be attributable to the cold-start rather than to the RL phase.

A deeper open question is whether the cold-start requirement is a fundamental constraint or an engineering convenience. It is conceivable that with sufficiently careful prompt design, a base model could engage in segment prediction tasks without an SFT scaffold — in which case the cold-start phase would be an artefact of the current task formulation rather than a hard prerequisite. Conversely, if instruction-following format compliance genuinely cannot be instilled by scaling alone, the cold-start phase points to a structural gap in current pre-training objectives.

Finally, there is no discussion of how cold-start data quality or quantity affects the RLPT outcome. Whether a minimal SFT (e.g., a few hundred examples) produces the same downstream RL trajectory as a richer one remains unexamined — a gap that matters if the goal is to make RLPT as annotation-free as its framing implies.

## Relationships

- **Reinforcement Learning on Pre-Training Data** — primary source; introduces RLPT and identifies the cold-start phase as a prerequisite
- **DeepDive: Advancing Deep Search Agents with Knowledge Graphs and Multi-Turn RL** — parallel instantiation of the SFT-then-RL pipeline pattern in search agent training
- **DeepSeek-V3.2: Pushing the Frontier of Open Large Language Models** — contextual reference; allocates post-training budget exceeding 10% of pre-training cost, illustrating the growing importance of post-training stages
- Related methods: RLPT, RLVR, RLHF — the cold-start phase sits at the boundary between pre-training and all three RL paradigms
- Related themes: [[themes/post_training_methods|post_training_methods]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/synthetic_data_generation|synthetic_data_generation]]

## Sources
