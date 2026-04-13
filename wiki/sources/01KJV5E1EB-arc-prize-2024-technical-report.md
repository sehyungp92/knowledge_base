---
type: source
title: 'ARC Prize 2024: Technical Report'
source_id: 01KJV5E1EBTAMS77SPACEPGAMJ
source_type: paper
authors:
- Francois Chollet
- Mike Knoop
- Gregory Kamradt
- Bryan Landers
published_at: '2024-12-05 00:00:00'
theme_ids:
- benchmark_design
- evaluation_and_benchmarks
- mathematical_and_formal_reasoning
- post_training_methods
- reasoning_and_planning
- test_time_learning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# ARC Prize 2024: Technical Report

> This report documents the ARC Prize 2024 competition and its technical findings, chronicling how three emergent approaches — LLM-guided program synthesis, test-time training, and their combination — pushed the ARC-AGI state-of-the-art from 33% to 55.5% while exposing fundamental limitations of classical deep learning for novel-task generalisation and surfacing critical reliability problems with the benchmark itself.

**Authors:** Francois Chollet, Mike Knoop, Gregory Kamradt, Bryan Landers
**Published:** 2024-12-05
**Type:** paper

---

## Context and Motivation

[[themes/evaluation_and_benchmarks|ARC-AGI]] was designed to measure what its creators define as the core of intelligence: efficient acquisition of new skills and generalisation to novel tasks. The benchmark's formal definition of AGI — a system capable of efficiently acquiring new skills and solving novel problems for which it was neither explicitly designed nor trained — explicitly rejects the classical deep learning paradigm, which generalises by relating new situations to training-time situations rather than adapting at test time.

This structural critique was empirically confirmed from the benchmark's inception. GPT-3 scored 0% via direct prompting. In the 2020 Kaggle competition, no deep learning approach exceeded 1%. Over the four years from 2020 to early 2024, despite the massive scaling of LLMs, the private evaluation set high score crept only from 20% to 33% — improving task-specific skill while leaving general intelligence unaddressed. As of December 5, 2024, five years after creation, the benchmark remains unbeaten.

ARC Prize 2024 was designed to counteract a second problem: frontier AI research moving behind closed doors at industry labs. The competition awarded prizes exclusively to teams who open-sourced reproducible solutions, converting competitive pressure into public research artifacts.

---

## The Benchmark Structure

ARC-AGI-1 consists of 1,000 tasks across four subsets: 400 public training tasks, 400 public evaluation tasks, 100 semi-private evaluation tasks, and 100 private evaluation tasks. Tasks require only Core Knowledge priors — objectness, basic topology, elementary integer arithmetic — and no specialised world knowledge or language.

The benchmark is easy for humans. Two testers scored 97% and 98% on the private evaluation set, together solving all 100 tasks. A Mechanical Turk study found 99% of public evaluation tasks were solved by at least one of ten assigned workers. The human–AI gap is therefore not a difficulty gap; it is a structural gap in generalisation.

### Benchmark Reliability Problems

The report is candid about ARC-AGI-1's degrading reliability as a measurement instrument:

- The 100-task private evaluation set has received approximately 10,000 cumulative score reports across four competitions, creating significant overfitting risk as each report leaks marginal information about the held-out distribution.
- Brute-force program search was technically capable of solving 49% of private evaluation tasks as early as 2020, meaning a substantial fraction of tasks never genuinely required generalisation.
- The public, semi-private, and private splits are not drawn from a consistent human difficulty distribution, making cross-evaluation score comparisons unreliable.
- For search-based approaches, scores are now inseparable from compute budget — it is no longer possible to assign a score to an approach independent of the resources available to it.

These issues collectively block valid cross-approach comparisons and constitute a [[themes/benchmark_design|benchmark design]] bottleneck that the report flags as requiring near-term resolution (horizon: months) via ARC-AGI-2.

---

## Competition Structure

The **Kaggle track** constrained participants to a single P100 GPU, under 12 hours, and no internet access — forcing algorithmic efficiency with a compute budget equivalent to roughly $10. The **ARC-AGI-Pub secondary leaderboard** allowed up to $10,000 in API credits and internet access, approximately 1,000 times more compute, enabling separate evaluation of frontier model approaches.

The close tracking between Kaggle scores and ARC-AGI-Pub scores is one of the report's most significant empirical findings: algorithmic improvements contribute far more than raw compute to ARC-AGI performance.

---

## Technical Approaches

### 1. LLM-Guided Program Synthesis

Ryan Greenblatt's approach reached 42% on ARC-AGI-Pub by using GPT-4o to generate, evaluate, and iteratively debug thousands of candidate Python programs per task — replacing brute-force DSL search with learned heuristics for program generation and selection. This was the first significant LLM-based program synthesis result on ARC-AGI and demonstrated that [[themes/mathematical_and_formal_reasoning|program synthesis]] with learned guidance could substantially outperform direct model prompting.

The approach's scaling profile reveals a critical limitation: achieving 85% accuracy via this method would require approximately 100 million program generations per task — a multi-million dollar compute budget for 100 tasks, making high-accuracy search economically unviable at current costs.

The report also notes that deep learning-guided program synthesis does not yet decisively outperform brute-force DSL search; both score in the 40% range on the private evaluation set with comparable compute, negating the expected advantage of learned guidance. One unexplored direction — using specialist models to guide branching decisions in DSL-based search, analogous to AlphaProof — is identified as technically promising but untried.

### 2. Test-Time Training (TTT)

[[themes/test_time_learning|Test-time training]] fine-tunes a pretrained LLM on the demonstration pairs of each individual task at inference time, creating a task-specific model variant. The conceptual framing offered in the report is important: TTT performs *shallow recombination* of many specialised weight-space building blocks via gradient descent, in contrast to program synthesis which performs *deep recombination* of a small set of generic primitives. This distinction matters for assessing the depth of novel concept composition achievable through adaptation.

Key implementation elements across top TTT teams:
- Pretraining on large synthetic ARC-like datasets (Re-ARC for infinite training task sampling; ARC-Heavy/ARC-Potpourri with 400,000 tasks)
- LoRA or full fine-tuning on augmented demonstration pairs
- 2D-aware transformer architectures with 2D attention mechanisms and positional encodings to capture spatial structure

Akyürek et al.'s 8B parameter TTT model achieved 53% on the public evaluation set, demonstrating that relatively small models with test-time adaptation can dramatically outperform much larger frontier models under static inference.

TTT has a direct dependency on large synthetic corpora: without 400,000+ auxiliary ARC-like pretraining tasks, the approach fails. Success is conditioned on corpus availability rather than task-intrinsic generalisation.

### 3. Ensembles and Novel Hybrids

Combining induction (program synthesis) and transduction (TTT) into ensembles is now universal among top scorers. The empirical motivation is straightforward: each approach solves substantially different subsets of tasks, and neither alone exceeds approximately 40% on the private set. All top 2024 scores — Akyürek and Berman on the public leaderboard, ARChitects and Barbadillo on Kaggle — use combinations of both.

The ARChitects introduced a novel selection criterion: filtering generated answers by consistency across augmented variants of the same task, using solution stability under data augmentation as a quality signal.

A further hybrid approach (Bonnet and MacFarlane) performs random search and gradient descent in the LLM's *latent space* to find better program representations — occupying a middle ground between discrete program search and weight-space fine-tuning.

---

## Results

| System | Score (semi-private) | Score (public) | Track |
|---|---|---|---|
| MindsAI | 55.5% | — | Kaggle (not open-sourced) |
| ARChitects | 53.5% | — | Kaggle (prize winner) |
| Barbadillo | 40% | — | Kaggle |
| Jeremy Berman | 53.6% | 58.5% | ARC-AGI-Pub |
| Akyürek et al. | 47.5% | 62.8% | ARC-AGI-Pub |
| Ryan Greenblatt | 43% | — | ARC-AGI-Pub |
| OpenAI o1-preview | 18% | 21% | Direct prompting |
| Claude 3.5 Sonnet | 14% | 21% | Direct prompting |
| GPT-4o | 5% | 9% | Direct prompting |
| Gemini 1.5 | 4.5% | 8% | Direct prompting |

The gap between frontier LLMs under direct prompting (4.5–18%) and TTT-based approaches (47–62%) is the report's sharpest empirical statement: static inference cannot generalise to novel tasks. No static inference-style transduction solution scores above 11%, establishing what the authors treat as an empirical ceiling for non-adaptive approaches.

---

## Capabilities Demonstrated

- **LLM-guided program synthesis** achieves 42% on ARC-AGI-Pub via iterative GPT-4o-guided Python program generation and debugging. *(maturity: research only)*
- **Induction + transduction ensembles** are the dominant strategy, with all top scores relying on combined approaches. *(maturity: research only)*
- **Latent space search** via random search and gradient descent in LLM latent space provides a novel hybrid between fine-tuning and discrete search. *(maturity: research only)*
- **2D-aware transformer architectures** with specialised attention and positional encodings improve spatial [[themes/reasoning_and_planning|reasoning]] on grid-based tasks. *(maturity: research only)*

---

## Limitations and Open Questions

**Fundamental:**
- Classical frozen-inference deep learning cannot generalise to novel ARC-AGI tasks. The 11% ceiling on static transduction is not a compute problem — it is a structural one. [[themes/post_training_methods|Test-time adaptation]] is a necessary condition for competitive performance.
- TTT performs shallow recombination over pretrained weight building-blocks. The depth of novel concept composition achievable through gradient-based adaptation at test time is architecturally bounded — an open theoretical question.

**Economic:**
- Achieving 85% via program synthesis requires ~100 million program generations per task at multi-million dollar cost for 100 tasks. High-accuracy generalisation via search is not economically viable at current compute costs.

**Operational:**
- TTT is too engineering-intensive for production systems; per-instance gradient descent at serving time is incompatible with standard deployment infrastructure. Expected non-productionised for ~2 years from late 2024.
- LLM-powered program synthesis requires heavy prompt engineering and deterministic code execution infrastructure, making it brittle and expensive beyond expert research settings.

**Benchmark:**
- ARC-AGI-1's private evaluation set is over-reported (~10,000 cumulative scores), partially brute-force-susceptible (49% solvable by 2020), split across inconsistent difficulty distributions, and now compute-budget-dependent — collectively blocking reliable measurement of generalisation progress. See [[themes/benchmark_design|benchmark design]].

**Frontier models:**
- Despite essentially unlimited API compute, frontier LLMs under direct prompting score only 4.5–18% — demonstrating that scale alone, without test-time adaptation, cannot bridge the generalisation gap.

---

## Breakthroughs and Bottlenecks

The TTT + program synthesis ensemble constitutes a **major breakthrough** in [[themes/test_time_learning|test-time learning]]: raising the ARC-AGI state-of-the-art from 33% to 55.5% through algorithmic innovation rather than compute scaling. The compute-algorithm decoupling finding — Kaggle entries at $10 matching ARC-AGI-Pub entries at $10,000 — is a **notable signal** that generalisation may be primarily an algorithmic rather than a resource problem.

Active bottlenecks:
1. **Economic viability of search-based synthesis** — 85% accuracy via program search requires ~100M generations per task; blocking horizon 3–5 years.
2. **Benchmark reliability** — ARC-AGI-1 is no longer a trustworthy measurement instrument; blocking horizon months (ARC-AGI-2 planned).
3. **AlphaProof-style guided DSL search** — specialist models guiding branching in discrete program search remain untried; blocking ceiling on single-approach program synthesis; horizon 1–2 years.
4. **Production TTT integration** — engineering complexity blocks deployment; horizon 1–2 years.

---

## Related Themes

- [[themes/benchmark_design|Benchmark Design]]
- [[themes/evaluation_and_benchmarks|Evaluation and Benchmarks]]
- [[themes/mathematical_and_formal_reasoning|Mathematical and Formal Reasoning]]
- [[themes/post_training_methods|Post-Training Methods]]
- [[themes/reasoning_and_planning|Reasoning and Planning]]
- [[themes/test_time_learning|Test-Time Learning]]

## Key Concepts

- [[entities/arc-agi|ARC-AGI]]
- [[entities/artificial-general-intelligence-agi|Artificial General Intelligence (AGI)]]
- [[entities/test-time-training|Test-Time Training]]
