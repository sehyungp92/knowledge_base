---
type: entity
title: Hallucination Rate
entity_type: metric
theme_ids:
- agent_systems
- ai_business_and_economics
- alignment_and_safety
- benchmark_design
- evaluation_and_benchmarks
- hallucination_and_reliability
- knowledge_and_memory
- long_context_and_attention
- medical_and_biology_ai
- model_architecture
- multi_agent_coordination
- multimodal_models
- retrieval_augmented_generation
- scientific_and_medical_ai
- vertical_ai_and_saas_disruption
- vision_language_models
created: '2026-04-08'
updated: '2026-04-08'
source_count: 3
sources_since_update: 0
update_count: 1
influence_score: 0.001528131893354071
staleness: 0.0
status: active
tags: []
---
# Hallucination Rate

Hallucination rate is a quantitative metric for measuring the faithfulness of large language model outputs to their input context — specifically, the percentage of sentences generated or retrieved by an LLM that cannot be traced back to any sentence in the actual input. Defined formally as one minus the fraction of retrieved sentences present in the context, it serves as a direct signal of fabricated content and has become a central diagnostic in evaluating retrieval-augmented systems, long-context reasoning, and high-stakes deployments such as legal and medical AI.

**Type:** metric
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/ai_business_and_economics|ai_business_and_economics]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/benchmark_design|benchmark_design]], [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]], [[themes/hallucination_and_reliability|hallucination_and_reliability]], [[themes/knowledge_and_memory|knowledge_and_memory]], [[themes/long_context_and_attention|long_context_and_attention]], [[themes/medical_and_biology_ai|medical_and_biology_ai]], [[themes/model_architecture|model_architecture]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/multimodal_models|multimodal_models]], [[themes/retrieval_augmented_generation|retrieval_augmented_generation]], [[themes/scientific_and_medical_ai|scientific_and_medical_ai]], [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]], [[themes/vision_language_models|vision_language_models]]

---

## Overview

Hallucination rate operationalises a question that matters deeply across all LLM deployments: when a model cites or retrieves content, is that content actually present in the input? The metric is straightforward — count the generated sentences that have no match in the context, divide by total retrieved sentences, and you get the fraction of fabricated output. A hallucination rate of 0% means every sentence is grounded; 61% means most of what the model retrieves is invented.

The metric gains particular salience in retrieval-augmented generation (RAG) pipelines, where the premise is that grounding a model in a curated knowledge base should suppress confabulation. Research into legal AI tools — evaluated by Stanford and Yale researchers — illustrates the gap between this promise and reality: leading commercial tools, despite using RAG, were found to produce legally unreliable outputs at meaningful rates. The mechanism of RAG (inserting retrieved documents directly into the prompt alongside the user's question) should in principle constrain generation to the context, but naive prompting-based retrieve-then-reason approaches fail to align the model's generation objective with its retrieval objective, leaving the door open for hallucination.

---

## Key Findings

The starkest quantitative evidence comes from ALR²: A Retrieve-then-Reason Framework for Long-context Question Answering, which benchmarked hallucination rates on HotpotQA. The Command-R model with a standard retrieve-then-reason (RR) prompting strategy produced a hallucination rate of approximately **61.1%** — meaning the majority of retrieved sentences it generated were not present in the input context. This is not a marginal failure; it is a near-total collapse of groundedness under naive prompting. The ALR² method, by contrast, fine-tunes the model to jointly optimise for both retrieval and reasoning objectives using golden supporting facts as retrieval targets, reducing the hallucination rate to **0.29%** — a roughly 200× improvement. Retrieval recall also roughly doubled (34% for CMD-R+RR versus 68.79% for ALR²), confirming that the issue is not retrieval quality alone but the alignment between what is retrieved and what is generated.

A key structural finding from the same work is that **reasoning performance degrades faster than retrieval performance as context length grows**. This asymmetry suggests that hallucination rate is not a fixed property of a model but a function of context window pressure — longer contexts produce more fabrication even when retrieval itself remains adequate. This is a meaningful constraint on the scalability of RAG-based systems.

In the medical domain, AMIE's multimodal OSCE study surfaces hallucination rate as a safety-critical concern rather than a benchmark abstraction. The state-aware reasoning framework that drives AMIE's three-phase dialogue (history taking → diagnosis and management → follow-up) was found to introduce slightly higher hallucination rates in some configurations compared to the vanilla baseline. For a system evaluated against 19 board-certified PCPs across 105 structured scenarios, even marginal increases in fabricated content carry clinical risk — which is part of why the codebase and prompts are not being open-sourced and why the authors explicitly position AMIE as a research system not ready for clinical deployment. The 105-scenario OSCE evaluation (35 skin photos, 35 ECGs, 35 clinical documents, reviewed by 18 specialist physicians) provides a controlled environment, but real-world validation remains absent.

---

## Capabilities and Mitigations

The ALR² result demonstrates that hallucination rate is not an irreducible property of LLMs — it can be driven to near-zero through training-time alignment of generation and retrieval objectives. This is a capability with direct implications for any system that depends on faithfulness to a knowledge base, from legal research tools to clinical dialogue agents. The key insight is that prompting alone is insufficient when the model's generation distribution is not explicitly shaped by retrieval targets.

- **Training-level retrieval-generation alignment** reduces hallucination rate from ~61% to ~0.29% on HotpotQA (ALR², maturity: research_only)
- **State-aware inference-time reasoning** can improve diagnostic accuracy in clinical dialogue but may trade off against groundedness in some settings (AMIE, maturity: research_only)

---

## Known Limitations and Open Questions

The most significant open question is **generalisability**: ALR²'s 0.29% figure is on HotpotQA, a controlled multi-hop QA benchmark. Whether similar alignment techniques transfer to open-domain legal or medical contexts — where knowledge bases are messier, queries are more ambiguous, and ground truth is harder to define — remains undemonstrated. The legal AI reliability paper shows that even systems built with RAG fail in practice, suggesting that benchmark-derived hallucination rates may understate real-world failure modes.

The **context-length dependency** identified in ALR² is a structural limitation: as input contexts grow, hallucination risk grows faster than retrieval degrades. This creates a ceiling on how much context can be safely handed to a model without additional mitigation. It also means that hallucination rate as measured on short-context benchmarks is likely an optimistic lower bound on operational hallucination rates in long-document settings.

In safety-critical deployments, **hallucination rate interacts with error asymmetry** in ways the metric does not capture. A 0.29% hallucination rate sounds negligible, but in a medical or legal context, the question is not the rate but the severity distribution — whether the fabricated sentences happen to be inconsequential or whether they land precisely in the high-stakes assertions that drive decisions. The metric is necessary but not sufficient for deployment readiness.

---

## Relationships

Hallucination rate is most directly relevant to [[themes/retrieval_augmented_generation|retrieval_augmented_generation]] and [[themes/hallucination_and_reliability|hallucination_and_reliability]], but its implications extend outward. In [[themes/long_context_and_attention|long_context_and_attention]], it surfaces as a scaling constraint — longer contexts amplify fabrication faster than they degrade retrieval. In [[themes/medical_and_biology_ai|medical_and_biology_ai]] and [[themes/scientific_and_medical_ai|scientific_and_medical_ai]], it is a deployment gate: systems like AMIE cannot move from research to clinical use until hallucination behaviour under real-world conditions is characterised. In [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]], the legal AI reliability findings suggest that hallucination rate is a competitive differentiator and a liability surface for commercial tools. The [[themes/alignment_and_safety|alignment_and_safety]] dimension is implicit throughout — hallucination is a form of misalignment between stated grounding and actual generation, and closing that gap is a prerequisite for trustworthy deployment.

**Primary sources:**
- ALR²: A Retrieve-then-Reason Framework for Long-context Question Answering
- Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools (Paper Explained)
- AMIE Multimodal OSCE Study (2025-05-06)

## Limitations and Open Questions

## Sources
