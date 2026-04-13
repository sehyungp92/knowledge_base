---
type: entity
title: SQuAD
entity_type: dataset
theme_ids:
- agent_self_evolution
- agent_systems
- alignment_and_safety
- hallucination_and_reliability
- knowledge_and_memory
- long_context_and_attention
- model_architecture
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- retrieval_augmented_generation
- rl_for_llm_reasoning
- scaling_laws
- test_time_compute_scaling
- test_time_learning
- transformer_alternatives
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.0007337321339530992
staleness: 0.0
status: active
tags: []
---
# SQuAD

> SQuAD (Stanford Question Answering Dataset) is a widely-used reading comprehension benchmark in which models must answer questions about Wikipedia passages. It serves as a canonical downstream evaluation target for language model capabilities in knowledge incorporation and question answering — making it a useful probe for assessing how well models retain and retrieve information embedded during training or finetuning.

**Type:** dataset
**Themes:** [[themes/knowledge_and_memory|Knowledge and Memory]], [[themes/post_training_methods|Post-Training Methods]], [[themes/retrieval_augmented_generation|Retrieval-Augmented Generation]], [[themes/test_time_learning|Test-Time Learning]], [[themes/reinforcement_learning|Reinforcement Learning]], [[themes/reasoning_and_planning|Reasoning and Planning]], [[themes/hallucination_and_reliability|Hallucination and Reliability]]

## Overview

SQuAD functions as a stress test for knowledge incorporation: given a passage, can a model absorb and retrieve specific facts from it? This makes it particularly well-suited for evaluating [[themes/test_time_learning|test-time learning]] and self-adaptation methods, where the central question is whether a model's weights can be updated to durably encode new information — not merely surface it from in-context text.

In recent work, SQuAD has been used specifically in the *no-passage-in-context* variant, where the passage is withheld at inference time and the model must answer from memory alone. This harder variant cleanly isolates whether information has been genuinely incorporated into weights rather than attended to from context.

## Key Findings

The Self-Adapting Language Models paper uses SQuAD extensively to benchmark the SEAL framework's knowledge incorporation capability, establishing a revealing performance ladder:

- **Frozen base model:** 32.7% — the ceiling of what the model already knows without any adaptation.
- **Passage-only finetuning:** 33.5% — a negligible gain, confirming that raw data without structured reformulation is insufficient for durable knowledge encoding.
- **Synthetic data (base Qwen-2.5-7B, no RL):** 39.7% — a 6.2-point jump, suggesting that structured reformulation of passage content, even from a small model, meaningfully improves retention.
- **GPT-4.1 implication augmentation:** 46.3% — adding generated implications of a passage yields the largest single-method gain (+12.8 points over passage-only), pointing to the value of *relational encoding* over surface repetition.
- **SEAL (RL-trained self-edits):** 47.0% — SEAL's RL-optimized self-generated synthetic data matches or slightly exceeds GPT-4.1 augmentation despite SEAL being a far smaller model.

In the continued pretraining setting (n=200 documents), GPT-4.1 synthetic data slightly edges out SEAL (59.4% vs. 58.2%), suggesting the gap between oracle-quality and self-generated reformulations narrows at scale but does not fully close.

These results collectively argue that *how* information is reformulated during finetuning matters far more than the raw presence of that information — and that RL-driven self-edit generation can approach the quality of frontier model synthesis without relying on external oracle models.

## Limitations and Open Questions

SQuAD's role here also exposes the limitations of SEAL itself. The RL reward loop that optimizes self-edit quality uses SQuAD performance as a signal, but each evaluation takes approximately 30–45 seconds per self-edit — making the training loop significantly more expensive than standard RL reward signals. This creates a practical ceiling on how much compute can be devoted to self-edit quality optimization.

More structurally, SEAL's RL training requires every context to be paired with an explicit downstream task (e.g., held-out SQuAD queries). This is a hard constraint that prevents scaling to unlabeled corpora — the kind of unsupervised continual learning that would be needed for the method to operate at real-world scale. SQuAD's clean supervised structure makes it ideal for benchmarking but also masks this brittleness.

SEAL also shows susceptibility to catastrophic forgetting across sequential self-edits: as new passages are incorporated, performance on earlier tasks degrades. SQuAD provides the measurement surface for this degradation, though it does not reveal solutions to it.

## Connections

SQuAD intersects with [[themes/retrieval_augmented_generation|retrieval-augmented generation]] through the ALR² paper, which targets long-context question answering tasks of similar form. ALR² addresses a complementary failure mode: rather than weight-level knowledge incorporation, it targets in-context retrieval, where modern LLMs hallucinate or misretrieve relevant facts even when the answer is present in the context. This framing — hallucination during retrieval, not during generation — connects SQuAD-style benchmarks to the [[themes/hallucination_and_reliability|hallucination]] literature in a non-obvious way.

Together, the two lines of work bracket the knowledge access problem: SEAL asks whether a model can *learn* a fact into its weights; ALR² asks whether a model can *find* a fact already in its context. SQuAD sits at the intersection, usable for both.

## Relationships

## Sources
