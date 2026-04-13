---
type: source
title: 'Best of 2024: Synthetic Data / Smol Models, Loubna Ben Allal, HuggingFace
  [LS Live! @ NeurIPS 2024]'
source_id: 01KJVGAVH2QZZGJDZYB2Y43W1M
source_type: video
authors: []
published_at: '2024-12-24 00:00:00'
theme_ids:
- finetuning_and_distillation
- post_training_methods
- pretraining_and_scaling
- pretraining_data
- synthetic_data_generation
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Best of 2024: Synthetic Data / Smol Models, Loubna Ben Allal, HuggingFace [LS Live! @ NeurIPS 2024]

> A NeurIPS 2024 retrospective by Loubna Ben Allal (HuggingFace) documenting how synthetic data colonized the entire LLM pipeline in 2024 — from pretraining through post-training to evaluation — and how small models trained on carefully curated synthetic data are closing the gap with models an order of magnitude larger.

**Authors:** Loubna Ben Allal (HuggingFace)
**Published:** 2024-12-24
**Type:** video

---

## The Synthetic Data Revolution

In 2024, synthetic data completed a sweep of the entire LLM training pipeline. The progression was sequential and fast:

1. **Post-training first** — synthetic data replaced human annotators for instruction-following SFT and preference data (DPO), because capable LLMs made annotation cheap and fast.
2. **Evaluation second** — the absence of good benchmarks for instruction quality, creativity, and conversational ability led to LLM-as-judge frameworks (MT-Bench, AlpacaEval) replacing human raters.
3. **Pretraining third** — motivated by the control synthetic generation offers over data quality and format, researchers began generating synthetic tokens to replace or augment web data entirely.

The endpoint is now reachable: a 1B model trained on 150B tokens from [[themes/synthetic_data_generation|Cosmopedia]] — 100% synthetic — then instruction-tuned and DPO-trained on synthetic data, evaluated by LLM judges. No human annotations required at any stage.

The driving conditions for this shift are structural: frontier models are strong enough to serve as capable teachers, inference frameworks (vLLM, TGI, TensorRT) make large-scale generation economically viable, and human annotation is comparatively slow and expensive.

---

## Model Collapse: The Evidence

The concern that training on synthetic data would cause progressive model degradation ("model collapse") was a dominant anxiety heading into 2024. The empirical picture is more reassuring than the theoretical worry suggested.

**Why the collapse studies were misleading:** They operated at small scale, having a small model iteratively self-train on its own completions — a regime where quality degrades by construction. This bears no resemblance to actual practice.

**What actually happens in practice:** A large, capable model distills its knowledge into a smaller target. The direction of information flow matters. You are not asking a weak model to improve itself; you are asking a strong model to teach a weaker one.

**What the data shows:** HuggingFace measured the prevalence of ChatGPT-associated proxy terms ("as a large language model", "delve") across successive Common Crawl dumps. The ratio increased sharply after ChatGPT's release — confirming that significant synthetic content has entered the web. Yet models trained on more recent, more synthetic-contaminated dumps performed *better* on NLP benchmarks, not worse.

The caveat: there is no reliable method to precisely measure what fraction of web data is synthetic. Proxy heuristics are imperfect and incomplete — a [[themes/pretraining_data|pretraining data]] limitation that remains unsolved.

---

## Diversity as the Central Engineering Problem

The most practically important insight from this talk is that diversity is the decisive variable in synthetic data quality — not model capability, not scale alone.

**The failure mode:** Feeding identical prompts to a generator, even with temperature variation, produces near-identical outputs. The resulting dataset fails to scale because it lacks variance.

**The solution (Cosmopedia):** Use web page excerpts as seed examples. Each generation prompt is conditioned on a distinct web extract, inheriting the breadth and variety of the open web. The model is asked to generate a textbook *related to* the extract rather than on a topic in the abstract.

**Style targeting matters too:** Generation style affects benchmark performance in predictable ways. College-level textbook generations improve MMLU performance; middle-school-level generations improve OpenBookQA and similar benchmarks. Cosmopedia exploited this by curating style mixtures deliberately.

The result: Cosmopedia (30B tokens) consistently outperformed FineWeb on a per-token efficiency basis across benchmarks throughout training.

---

## FineWeb-Edu: Synthetic Filtering at Scale

A parallel contribution is using synthetic LLM judgments not to *generate* training data, but to *filter* it. FineWeb-Edu was built by prompting Llama 3 to rate the educational quality of web pages on a 0–5 scale, then filtering to the top tier.

The outcome: a 10:1 compression of the web (15T → 1.5T tokens) that maintains or improves downstream model performance. This demonstrates that [[themes/synthetic_data_generation|LLM-based content classification]] can substitute for expensive human curation at web scale.

The limitation this exposes: using LLMs as evaluators introduces evaluation bias — conflating model similarity with capability — making benchmark results potentially unreliable in ways that are hard to audit.

---

## Small Models Closing the Gap

The second major thread is the surprising performance of small models (1–3.8B parameters) trained with optimized data:

- **Llama 3.2 1B** matches Llama 2 13B (released one year earlier) on LM Arena — a model one-tenth the size achieving parity through better data curation and extended pretraining.
- **SmolLM** (1B) was trained on 11 trillion tokens, versus 1 trillion for earlier 1B models. Performance kept improving without hitting a plateau, contradicting prior intuitions about [[themes/pretraining_and_scaling|scaling]] limits for small models.
- Small models at 3–3.8B now run on consumer mobile hardware (e.g., iPhone via Pocket Palms app) with acceptable latency, enabling genuinely local AI.
- SmolVLM (2B) extends this to vision-language understanding with a low memory footprint.

The implication: frontier inference cost remains prohibitively high for resource-constrained environments, and the field's focus is shifting from building larger models to building smaller ones that achieve more per parameter.

---

## Nvidia Nemotron-CC: Rephrasing at Trillion-Token Scale

Nvidia's Nemotron-CC pushed synthetic pretraining data generation further: rather than generating from scratch, they rephrased 1.9 trillion tokens of existing web content into structured formats (Wikipedia-style passages, Q&A pairs, etc.).

The key observation is that rephrasing does not require extensive world knowledge — it is a style transfer operation. This means small models can perform the rephrasing step cheaply, keeping the cost of trillion-token synthetic corpus generation tractable.

---

## Capabilities

| Capability | Maturity | Evidence |
|---|---|---|
| End-to-end LLM training on 100% synthetic data (pretraining + SFT + DPO + LLM-judge eval) | broad_production | Cosmopedia 1B, 150B tokens |
| 10:1 web compression via synthetic LLM content classification | broad_production | FineWeb-Edu (15T→1.5T tokens) |
| On-device inference of 3–3.8B models on consumer mobile hardware | broad_production | Llama 3.2 via Pocket Palms |
| Continuous performance gains for 1-3B models through extended pretraining (up to 11T tokens) | demo | SmolLM training curves |
| Structured JSON output generation without fine-tuning via schema constraint enforcement | narrow_production | — |
| Vision-language understanding at 2B parameters with low memory footprint | demo | SmolVLM |

---

## Limitations and Open Questions

**Data detection gap:** No standardized method exists to measure what proportion of web content is synthetic. Proxy heuristics (ChatGPT-specific phrases) are directionally useful but methodologically insufficient. This is a [[themes/pretraining_data|pretraining data]] problem that grows as synthetic content proliferates.

**Evaluation circularity:** LLM-as-judge frameworks conflate model similarity with quality, making it possible to "pass" evaluations by matching the judge's style rather than by demonstrating genuine capability. The field adopted LLM judges partly because human benchmarks were inadequate — but the replacement has its own biases that are less well-understood.

**Contamination opacity:** When training data is closed (as in the original Phi/textbooks papers), it is impossible to distinguish genuine capability improvements from benchmark contamination. HuggingFace's open replication of Cosmopedia was partly motivated by this scepticism — the Phi results were credible but unverifiable.

**Engineering complexity:** High-quality synthetic data at scale requires extensive ablation studies, mixture optimization, diversity engineering, and task-specific dataset construction. There is no general recipe; it is a labor-intensive craft that scales with effort, not just compute.

**Inference cost asymmetry:** The largest frontier models remain prohibitively expensive for many deployment contexts. The gap between what is technically achievable and what is economically deployable has widened, reinforcing the strategic case for small models but not eliminating the frontier cost barrier.

---

## Themes

- [[themes/synthetic_data_generation|Synthetic Data Generation]]
- [[themes/pretraining_data|Pretraining Data]]
- [[themes/pretraining_and_scaling|Pretraining and Scaling]]
- [[themes/post_training_methods|Post-Training Methods]]
- [[themes/finetuning_and_distillation|Finetuning and Distillation]]

## Key Concepts

- [[entities/alpacaeval|AlpacaEval]]
- [[entities/cosmopedia|Cosmopedia]]
- [[entities/dclm|DCLM]]
- [[entities/fineweb|FineWeb]]
- [[entities/fineweb-edu|FineWeb-Edu]]
- [[entities/grouped-query-attention|Grouped Query Attention]]
- [[entities/mmlu|MMLU]]
- [[entities/mt-bench|MT-Bench]]
- [[entities/model-collapse|Model Collapse]]
- [[entities/scaling-laws|Scaling Laws]]
