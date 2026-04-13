---
type: entity
title: STaR
entity_type: method
theme_ids:
- agent_systems
- ai_market_dynamics
- chain_of_thought
- finetuning_and_distillation
- latent_reasoning
- model_commoditization_and_open_source
- multi_agent_coordination
- policy_optimization
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- software_engineering_agents
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
source_count: 7
sources_since_update: 0
update_count: 1
influence_score: 0.0038057367246627965
staleness: 0.0
status: active
tags: []
---
# STaR

**Type:** method
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/chain_of_thought|chain_of_thought]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/latent_reasoning|latent_reasoning]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Overview

Self-Taught Reasoner (Zelikman et al. 2022): trains LMs to bootstrap reasoning ability on QA datasets by sampling rationales, training on those leading to correct answers, and iterating to solve harder problems.

## Key Findings

1. Quiet-STaR achieves zero-shot improvements on CommonsenseQA from 36.3% to 47.2% without any fine-tuning on the task. (from "Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking")
2. Teacher-forcing is applied to include ground-truth tokens in the loss for future tokens after a thought, allowing computation of log probabilities for multiple future tokens without sampling. (from "Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking")
3. STaR's limitation is that training from curated QA datasets limits the scale and generalizability of rationales, since QA datasets will inherently only cover a subset of reasoning tasks. (from "Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking")
4. Quiet-STaR uses learnable <|startofthought|> and <|endofthought|> meta-tokens to mark the boundaries of each rationale, initialized to the em dash embedding. (from "Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking")
5. Quiet-STaR achieves zero-shot improvements on GSM8K from 5.9% to 10.9% without any fine-tuning on the task. (from "Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking")
6. Reasoning improvements from Quiet-STaR scale with the number of thought tokens used during training and inference. (from "Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking")
7. Training on OpenWebMath (math-focused web text) provides larger reasoning improvements than training on C4 (general web text). (from "Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking")
8. Multi-token rationales produced by Quiet-STaR are more effective for reasoning than single-token 'pause' tokens. (from "Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking")
9. Whether Quiet-STaR works when training a model from scratch (rather than continued pretraining) remains unknown. (from "Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking")
10. Annotating reasoning traces manually is off-policy for LMs (the distribution of human-written reasoning differs from what the LM would generate) and provides no clear path to solving problems harder t (from "Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking")
11. Quiet-STaR and chain-of-thought prompting are orthogonal and complementary: CoT prompts the model to think out loud on demand, while Quiet-STaR trains a distribution for useful silent thinking at ever (from "Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking")
12. Quiet-STaR generalizes STaR by training LMs to generate rationales at every token position in arbitrary text, rather than only on curated QA datasets. (from "Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking")
13. The parallel generation algorithm achieves efficiency by caching each forward pass and concatenating a diagonal attention mask so each generated thought token attends to all tokens used to generate it (from "Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking")
14. Quiet-STaR uses REINFORCE with a reward defined as the difference between a rationale's log-likelihood of future tokens and the average across all rationales for that token, to optimize rationale gene (from "Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking")
15. Quiet-STaR's internal rationales are complementary to chain-of-thought prompting; combining both improves GSM8K majority-vote accuracy from 40.6% to 47.7% (cot-maj@8 on 128 test items). (from "Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking")

## Capabilities

- Graduated trust-building framework for agent autonomy expansion: starting agents on low-risk tasks (web scraping) and advancing to complex domains (financial decisions) based on demonstrated reliabili (maturity: demo)
- DexMimicGen automated simulation trajectory synthesis generates 780,000 demonstration trajectories equivalent to 6,500 hours of human demonstration data in just 11 hours of compute, starting from a fe (maturity: narrow_production)
- Generating diverse alternative futures (multiple plausible continuations) from a single gameplay starting point, capturing the full distribution of human player behaviors and visual character appearan (maturity: demo)
- Visual (non-language) prompting of world models using starting frames to condition generation, enabling direct image-based creative input rather than requiring text descriptions (maturity: demo)
- Hope achieves perfect scores on all formal language recognition tasks — including non-star-free regular, counter, and parity tasks — where transformers score near zero (maturity: research_only)

## Known Limitations

- GPU idle time during agentic RL rollouts due to slow environment feedback (VM startup, code execution) — training compute is systematically wasted while waiting for environment responses (severity: significant, trajectory: unclear)
- AI startups dependent on incumbent SaaS platforms for data access face an existential strategic risk as incumbents tighten API access and terms (severity: significant, trajectory: worsening)
- App-layer AI startups built on API access face structural dependency risk: the model provider that powers them has full visibility into their usage patterns and can replicate or acquire them at any ti (severity: significant, trajectory: worsening)
- Without BoLT, the performance ceiling of a latent thought model is bounded by the quality of the teacher model used for warmstart synthesis; this fundamentally limits the approach's potential to advan (severity: significant, trajectory: improving)
- The approach involves limited exploration of critical design choices: latent generative structure, chunk size, MC sampling strategy, and warmstart model choice are all under-explored, meaning the repo (severity: minor, trajectory: unclear)

## Relationships

## Limitations and Open Questions

## Sources
