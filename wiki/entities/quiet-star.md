---
type: entity
title: Quiet-STaR
entity_type: method
theme_ids:
- adaptive_computation
- chain_of_thought
- finetuning_and_distillation
- interpretability
- knowledge_and_memory
- latent_reasoning
- mechanistic_interpretability
- model_architecture
- policy_optimization
- post_training_methods
- reasoning_and_planning
- reinforcement_learning
- representation_learning
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- test_time_compute_scaling
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
source_count: 4
sources_since_update: 0
update_count: 1
influence_score: 0.0005862181058583237
staleness: 0.0
status: active
tags: []
---
# Quiet-STaR

Quiet-STaR (Zelikman et al., 2024) is a method that trains language models to silently generate internal rationales before predicting each token in arbitrary text, enabling emergent reasoning capabilities without task-specific fine-tuning. By generalizing the earlier STaR framework to work on unstructured internet text rather than curated QA datasets, it represents a significant step toward models that learn to think as a byproduct of reading — achieving zero-shot gains on mathematical and commonsense reasoning benchmarks purely through continued pretraining.

**Type:** method
**Themes:** [[themes/adaptive_computation|adaptive_computation]], [[themes/chain_of_thought|chain_of_thought]], [[themes/finetuning_and_distillation|finetuning_and_distillation]], [[themes/interpretability|interpretability]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/latent_reasoning|latent_reasoning]], [[themes/mechanistic_interpretability|mechanistic_interpretability]], [[themes/model_architecture|model_architecture]], [[themes/policy_optimization|policy_optimization]], [[themes/post_training_methods|post_training_methods]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/representation_learning|representation_learning]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/transformer_alternatives|transformer_alternatives]]

## Overview

Quiet-STaR addresses a fundamental limitation of its predecessor STaR: training on curated QA datasets constrains both scale and generalization, since high-quality QA data covers only a narrow slice of the reasoning tasks a model might encounter. The approach instead inserts learned rationale generation at every token position in continuous pretraining corpora, using two learnable meta-tokens — `<|startofthought|>` and `<|endofthought|>` — to bracket each silent thought. Both are initialized to the em dash embedding, exploiting the token's natural role as a syntactic pause in natural text.

The training procedure is built around a parallel generation algorithm designed to keep compute tractable: each forward pass is cached and a diagonal attention mask is concatenated to the existing attention mask, so each generated thought token attends only to the tokens used in its own generation. Teacher-forcing is then applied across thought boundaries — the model's log probabilities over true next tokens are computed by assuming it selected the ground-truth tokens, allowing multi-token future predictions without requiring additional sampling passes.

Rationale quality is optimized via REINFORCE. The reward for each rationale is defined as its log-likelihood improvement over future tokens relative to the average across all rationales generated for that token position — a relative, self-supervised signal requiring no external annotation. This sidesteps the off-policy problem that plagues supervised rationale annotation: human-written reasoning traces follow a different distribution from what the model itself would produce, and cannot provide a path to solving problems harder than the annotators can handle.

## Empirical Results

The method achieves zero-shot improvements on GSM8K from 5.9% to 10.9% and on CommonsenseQA from 36.3% to 47.2%, purely through continued pretraining on internet text — no task-specific fine-tuning is applied. These gains are not architectural but emerge from the learned habit of internal deliberation. Crucially, improvements scale with the number of thought tokens allocated during training and inference, consistent with the broader [[themes/test_time_compute_scaling|test-time compute scaling]] picture: more thorough reasoning through more tokens yields better predictions.

Training data distribution matters significantly. Pretraining on OpenWebMath — math-focused web text with a higher density of tokens that benefit from reasoning — yields larger gains than training on general web text (C4), suggesting the method extracts more signal where reasoning is most load-bearing.

Multi-token rationales are meaningfully more effective than single-token "pause" tokens. While pause token fine-tuning shows minor CommonsenseQA gains (26.9% → 28.8%), the gap versus Quiet-STaR's improvements indicates that the content of the internal thought, not merely its presence as a computational delay, is doing substantive work.

## Relationship to Chain-of-Thought

Quiet-STaR and chain-of-thought prompting are orthogonal interventions. Chain-of-thought prompts the model to reason explicitly and visibly on demand; Quiet-STaR trains a distribution for silent, automatic deliberation at every step. Rather than competing, they are additive: combining Quiet-STaR pretraining with CoT prompting raises majority-vote accuracy (cot-maj@8) on GSM8K from 40.6% to 47.7% on a sample of 128 test items, compared to CoT alone. This suggests the internal rationale distribution learned by Quiet-STaR enriches the latent representations that CoT then makes explicit, rather than redundantly covering the same ground.

## Limitations and Open Questions

Several important unknowns remain. Most significantly, it is unknown whether Quiet-STaR works when training a model from scratch rather than as continued pretraining on an already-capable base model. If the method requires a model that has already internalized enough structure to produce useful proto-rationales, it may not be a path to reasoning from first principles — only an amplification mechanism for existing capability.

The efficiency of parallel thought generation, while substantially better than naïve approaches, still imposes compute overhead proportional to thought length at every token position, not just at designated reasoning steps. This makes Quiet-STaR expensive relative to standard pretraining and raises questions about where internal deliberation is worth paying for in the token stream. The finding that OpenWebMath outperforms C4 hints at an answer — not all tokens equally reward internal thought — but a principled token-adaptive allocation strategy remains undeveloped.

The interpretability of the generated rationales is also unclear. Because they are internal and never decoded during inference, there is no direct mechanism to inspect what the model is "thinking." This places Quiet-STaR in tension with the goals of [[themes/interpretability|interpretability]] and [[themes/mechanistic_interpretability|mechanistic interpretability]] research: the method moves reasoning capability inward and makes it less, not more, legible.

## Sources

- Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking
- Thinking LLMs: General Instruction Following with Thought Generation
- Continuous Thought Machines
- Reinforcement Learning Improves Traversal of Hierarchical Knowledge in LLMs

## Key Findings

## Relationships
