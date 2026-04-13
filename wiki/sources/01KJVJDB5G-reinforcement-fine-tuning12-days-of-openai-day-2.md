---
type: source
title: 'Reinforcement Fine-Tuning—12 Days of OpenAI: Day 2'
source_id: 01KJVJDB5G5CT52AENVJGX06SP
source_type: video
authors: []
published_at: '2024-12-06 00:00:00'
theme_ids:
- finetuning_and_distillation
- post_training_methods
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Reinforcement Fine-Tuning — 12 Days of OpenAI: Day 2

OpenAI's Day 2 announcement introduces reinforcement fine-tuning (RFT) as a new model customisation paradigm that applies the same RL algorithms responsible for o1's reasoning leap to user-defined domains — enabling developers to create expert models from small, curated datasets without replicating the compute or data scale of frontier training runs.

**Authors:** OpenAI
**Published:** 2024-12-06
**Type:** video

---

## What This Source Argues

RFT is a qualitatively different form of customisation from supervised fine-tuning. Where [[themes/finetuning_and_distillation|SFT]] teaches a model to mimic the surface features of training examples (tone, format, style), RFT teaches the model *how to reason* over a new domain by rewarding correct conclusions and discouraging reasoning paths that led to errors. The grader — not labelled outputs — is the primary supervision signal.

The centrepiece demonstration: fine-tuning o1-mini on ~1,100 curated rare disease case reports to predict causative genes from symptom lists. The result — 31% top-1 accuracy — exceeded base o1 (25%) and far exceeded base o1-mini (17%), a smaller and cheaper model outperforming a larger one through domain specialisation.

---

## Core Mechanism

The [[themes/rl_for_llm_reasoning|RL fine-tuning]] loop works as follows:

1. The model receives a prompt and generates a chain-of-thought response ending in a structured answer.
2. A **grader** compares the answer to the ground-truth label and returns a score in [0, 1], with partial credit permitted.
3. [[themes/reinforcement_learning|Reinforcement learning]] reinforces reasoning traces that produced high scores and discourages those that did not.
4. The model's weights update without ever seeing the correct answer directly — only the scalar reward.

This is the same technique OpenAI uses internally to train GPT-4o and the o1 series. The user supplies the domain expertise (dataset + grader definition); OpenAI supplies the RL infrastructure and the distributed training stack.

**Contrast with SFT:** SFT requires large datasets to shift model behaviour and can only teach the model to replicate what it sees. RFT can induce genuinely new reasoning strategies over custom domains with *as few as a few dozen examples* — a claim the rare disease demo validates empirically at ~1,100 examples.

---

## Capabilities Demonstrated

| Capability | Evidence | Maturity |
|---|---|---|
| Domain adaptation of frontier models via user-defined RL | Thomson Reuters CoCounsel (legal); rare disease gene ID | Demo |
| Smaller model exceeding larger model through RFT specialisation | o1-mini 31% > o1 25% on gene identification task | Demo |
| Partial-credit graders for ranked/structured outputs | Rank-decay scoring on gene lists | Demo |
| Effective learning from small curated datasets | Few dozen to ~1,100 examples sufficient | Demo |
| Expert multi-step biomedical reasoning from symptom lists only | Top-1 gene identification, no genomic sequencing input | Demo |

The rare disease application is illustrative of a broader class of problems: tasks requiring both *expert domain knowledge* and *systematic reasoning over structured data*, where neither retrieval nor SFT alone suffices.

---

## Limitations and Open Questions

Several constraints bound what was demonstrated here.

**Access and availability.** RFT is in limited alpha at announcement; public release is targeted for early 2025. The capability is not generally accessible.

**Grader engineering bottleneck.** Each task requires a task-specific reward grader. OpenAI provides template graders intended to cover common intent types, with custom Python graders forthcoming — but grader design remains a non-trivial engineering effort that is currently the primary specialisation barrier. See [[themes/reward_modeling|reward modeling]].

**Dataset curation cost.** The rare disease dataset required collaboration between OpenAI, Charité Hospital (Germany), Peter Robinson's lab, and the Monarch Initiative. Curating ~1,100 structured examples from unstructured case reports is not a solo developer task. This is a significant friction point for scaling RFT to new domains.

**No apples-to-apples comparison with existing tools.** Standard bioinformatics workflows for rare disease diagnosis use full genomic sequencing data; the RFT demo used symptom lists only. The absolute performance numbers are not directly comparable to the existing clinical literature. Whether RFT o1-mini would generalise to full clinical workflows (with lab data, genomic sequencing, longitudinal records) is unknown.

**Compute latency.** Training runs take hours to days. This is not a fast iteration loop for domain adaptation.

**Memorisation vs. generalisation.** The validation set was explicitly constructed with no overlap in correct genes vs. training — requiring careful data engineering. This constraint adds overhead and, if violated, the model risks memorising rather than learning to reason.

---

## Bottlenecks This Source Illuminates

**Reward grader engineering** is identified as the proximate bottleneck for widespread RFT adoption. Domain-specific graders must be designed for every task, which currently requires understanding both the task structure and the scoring intent. Template graders narrow but do not close this gap. Until grader authoring is substantially easier — whether through tooling, learned graders, or automated grader generation — RFT will remain accessible primarily to sophisticated ML teams.

**Expert data curation** is a second bottleneck that is easy to understate. The 1,100-example dataset was produced by domain experts over a substantial effort. The claim that "a few dozen examples" suffice is technically accurate but obscures that *correctly structured* examples with verified ground-truth labels are expensive to produce in specialised fields (legal, medical, financial, engineering).

---

## Breakthroughs

The demonstration that a smaller, cheaper model (o1-mini) can *exceed* a larger base model (o1) through targeted RFT is significant. It challenges the assumption that capability is primarily a function of model scale, and suggests that [[themes/post_training_methods|post-training]] domain specialisation can partially substitute for scale on constrained tasks. This has direct implications for deployment economics: domain-expert models need not be the largest models.

---

## Connections

- [[themes/rl_for_llm_reasoning|RL for LLM reasoning]] — RFT is a productised instance of the same training paradigm that produced o1's reasoning capabilities; this source makes that lineage explicit.
- [[themes/finetuning_and_distillation|Finetuning and distillation]] — RFT and SFT are positioned as complementary, not competing; SFT for format/style, RFT for reasoning over new domains.
- [[themes/reward_modeling|Reward modeling]] — Grader design is the critical open problem; the source signals OpenAI is actively expanding the grader library and moving toward user-defined custom graders.
- [[themes/post_training_methods|Post-training methods]] — RFT extends the post-training toolkit beyond RLHF/DPO into domain-specific RL, democratising a technique previously available only at frontier labs.

---

## Open Questions

- How does RFT performance scale with dataset size beyond the ~1,100-example regime? Is there a saturation point?
- Can grader quality be automatically evaluated, or does it require human validation of grader correctness before training?
- How do RFT-specialised models behave outside their training domain — do they degrade gracefully or catastrophically?
- Does RFT compound with SFT (format first, then reason), and if so, what is the correct sequencing?
- What is the lower bound on training data for genuine reasoning generalisation vs. pattern matching across different domain types?

## Key Concepts

- [[entities/supervised-fine-tuning-sft|Supervised Fine-Tuning (SFT)]]
- [[entities/o1|o1]]
