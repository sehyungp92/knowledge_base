---
type: entity
title: Long Chain-of-Thought
entity_type: method
theme_ids:
- chain_of_thought
- finetuning_and_distillation
- mathematical_and_formal_reasoning
- multimodal_models
- policy_optimization
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- scaling_laws
- test_time_compute_scaling
created: '2026-04-09'
updated: '2026-04-09'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 3.485597103088439e-05
staleness: 0.0
status: active
tags: []
---
# Long Chain-of-Thought

> Long chain-of-thought (LCoT) is an extended reasoning technique in which language models generate lengthy, step-by-step internal reasoning traces before producing final answers. It sits at the center of the Large Reasoning Model (LRM) paradigm and has become the primary mechanism through which reinforcement learning unlocks emergent problem-solving in models like DeepSeek-R1 and Kimi k1.5. Its significance lies not just in improved benchmark scores, but in demonstrating that structured deliberation can emerge from training signals alone, without human-annotated reasoning trajectories.

**Type:** method
**Themes:** [[themes/chain_of_thought|chain_of_thought]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/multimodal_models|multimodal_models]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/scaling_laws|scaling_laws]], [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Overview

Long chain-of-thought emerged as a central technique when DeepSeek-R1 demonstrated that extended reasoning traces can be elicited through pure reinforcement learning, without any human-labeled reasoning trajectories. The key insight is that correctness-based reward signals alone, applied to final predictions, are sufficient to develop rich intermediate reasoning behavior. DeepSeek-R1-Zero, the ablation that bypasses supervised fine-tuning entirely before RL, saw its AIME 2024 pass@1 score climb from 15.6% to 77.9% through RL training alone, and further to 86.7% with self-consistency decoding across 16 samples. This positions LCoT not as a prompt engineering trick but as a learnable capability that emerges under appropriate training pressure.

The relationship between SFT and RL in cultivating long chain-of-thought is actively contested. DeepSeek-R1-Zero's design explicitly bypasses conventional SFT, based on the hypothesis that human-defined reasoning patterns may artificially constrain the model's exploration of the reasoning space. The full DeepSeek-R1, however, uses a multi-stage pipeline (cold-start SFT, first RL stage, rejection sampling plus SFT, second RL stage), suggesting that raw RL-only training has practical limits. VibeThinker-1.5B formalizes this tension into the Spectrum-to-Signal Principle (SSP): SFT is reframed as a diversity-maximization phase (Pass@K), spreading the model's output distribution broadly across solution approaches, while RL then amplifies the correct signals from that spectrum. Under this framing, SFT and RL are not alternatives but complementary stages with distinct objectives.

Curriculum and difficulty targeting are increasingly recognized as critical for effective LCoT training. VibeThinker's MaxEnt-Guided Policy Optimization (MGPO) prioritizes problems where the model's empirical accuracy is closest to 0.5, arguing that these represent the zone of maximum productive uncertainty. As the regularization coefficient increases, MGPO focuses more intensely on this uncertainty band, and at zero regularization it degrades to standard GRPO. This is a concrete operationalization of a broader principle: LCoT training benefits from staying at the edge of the model's competence rather than reinforcing easy problems or struggling with intractable ones.

LCoT has shown reach beyond text into multimodal settings. Models equipped with LCoT can reason about physical common sense, including space, time, and fundamental physics, from video input, achieving scores competitive with or exceeding OpenAI o1 on structured physical reasoning benchmarks. This suggests the technique generalizes across modalities, though the evidence remains at demonstration maturity.

## Limitations and Open Questions

Despite impressive benchmark numbers, LCoT training carries several underappreciated failure modes. DeepSeek-R1-Zero, trained without SFT cold-start, suffers from poor readability and language mixing: the model occasionally produces reasoning traces that blend English and Chinese within a single chain-of-thought. This is not merely an aesthetic issue; it signals that the model's internal reasoning representation is not fully aligned with human-interpretable structure, which complicates inspection and distillation.

Prompt sensitivity is a persistent practical limitation. DeepSeek-R1 is sensitive to prompt formatting, and few-shot prompting consistently degrades its performance; zero-shot is the recommended configuration. This is a meaningful constraint for deployment, as it limits the composability of LCoT models with standard prompting pipelines.

The cost of producing capable LCoT models at small scale remains non-trivial. VibeThinker-1.5B required approximately 3,900 GPU hours on NVIDIA H800 GPUs at a total cost of roughly $7,800, even with careful data curation including 10-gram decontamination to prevent evaluation leakage. Scaling this to larger models, or to domains without clean verifiable rewards, raises open questions about feasibility.

The deepest open question concerns the nature of what LCoT actually learns. When reasoning emerges from correctness rewards alone, without any human-labeled trace supervision, it is unclear whether the model is discovering structurally valid reasoning patterns or learning to produce outputs that correlate with correct answers via reasoning-shaped artifacts. This distinction matters for generalization: a model that genuinely reasons should transfer to out-of-distribution problems; one that mimics reasoning structure may not.

## Relationships

Long chain-of-thought is the primary mechanism through which [[themes/rl_for_llm_reasoning|RL for LLM reasoning]] produces capability gains, with GRPO and its variants (MGPO) serving as the policy optimization backbone. It connects directly to [[themes/test_time_compute_scaling|test-time compute scaling]], since longer reasoning traces consume more inference compute and self-consistency decoding multiplies that cost further. The technique is central to [[themes/mathematical_and_formal_reasoning|mathematical and formal reasoning]] performance, where verifiable rewards make LCoT training tractable, but its extension to domains without clean ground-truth signals remains an open frontier in [[themes/reward_modeling|reward modeling]]. Distillation of LCoT traces into smaller models links it to [[themes/finetuning_and_distillation|finetuning and distillation]], and the emergence of LCoT capabilities without SFT touches fundamental questions in [[themes/pretraining_and_scaling|pretraining and scaling]] about what base models already know.

## Key Findings

## Sources
