---
type: source
title: To CoT or not to CoT? Chain-of-thought helps mainly on math and symbolic reasoning
source_id: 01KJV8DVH3CJGCY00XAEE8YT2P
source_type: paper
authors:
- Zayne Sprague
- Fangcong Yin
- Juan Diego Rodriguez
- Dongwei Jiang
- Manya Wadhwa
- Prasann Singhal
- Xinyu Zhao
- Xi Ye
- Kyle Mahowald
- Greg Durrett
published_at: '2024-09-18 00:00:00'
theme_ids:
- benchmark_design
- chain_of_thought
- evaluation_and_benchmarks
- mathematical_and_formal_reasoning
- reasoning_and_planning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# To CoT or not to CoT? Chain-of-thought helps mainly on math and symbolic reasoning

This paper delivers a systematic empirical correction to one of the most pervasive assumptions in LLM prompting research: that chain-of-thought reasoning broadly improves performance across diverse task types. Through a meta-analysis of 110 papers (1,218 comparisons) and original experiments spanning 20 datasets and 14 models, the authors demonstrate that CoT's benefits are tightly confined to mathematical and symbolic reasoning, with negligible or negative effects elsewhere — exposing a significant publication bias that has distorted the field's understanding of LLM reasoning capabilities.

**Authors:** Zayne Sprague, Fangcong Yin, Juan Diego Rodriguez, Dongwei Jiang, Manya Wadhwa, Prasann Singhal, Xinyu Zhao, Xi Ye, Kyle Mahowald, Greg Durrett
**Published:** 2024-09-18
**Type:** paper

---

## Motivation

[[themes/chain_of_thought|Chain-of-thought]] prompting had become the default technique for eliciting reasoning from LLMs, yet the literature had systematically over-represented math tasks while claiming broad reasoning benefits. Papers framed as addressing "complex multi-step reasoning" reported results exclusively on GSM8K and MATH; LLM release announcements cited improved "reasoning capabilities" supported only by math benchmarks. Outside math, the picture was contradictory — some work suggested CoT was unhelpful or harmful on non-symbolic tasks — but no rigorous cross-domain analysis had been conducted to settle the question.

The tacit assumption that deliberate step-by-step reasoning improves performance on *any* task requiring some form of reasoning lacked empirical grounding across the full task space.

---

## Approach

The study used two complementary methodologies:

**Meta-analysis.** 4,642 papers from ICLR 2024, EACL 2024, and NAACL 2024 were filtered to 110 papers reporting direct CoT vs. direct-answer comparisons (1,218 experimental comparisons). Tasks were categorized by reasoning type: symbolic/algorithmic, math, logical, encyclopedic knowledge, commonsense, soft reasoning, and mixed.

**Original experiments.** 20 datasets × 14 LLMs under zero-shot and few-shot prompting, with greedy decoding via vLLM and per-dataset answer parsers calibrated for low unparseable rates.

To diagnose *why* CoT helps on symbolic tasks, the authors decomposed symbolic reasoning into a **planning stage** (mapping the question to a formal specification) and an **execution stage** (solving that specification). They compared five settings: direct answer, CoT, Plan + Direct Solver, Plan + CoT Solver, and Plan + Tool Solver (Python via PAL; Z3 SMT solver via SatLM). This decomposition isolates whether CoT's gains come from better problem formulation or better step-by-step computation, and whether external solvers can replace CoT's execution role.

---

## Key Findings

### CoT benefits are domain-specific, not general

The meta-analysis average CoT deltas by category tell a stark story:

| Category | CoT Gain |
|---|---|
| Symbolic reasoning | +14.2 pp |
| Math | +12.3 pp |
| Logical reasoning | +6.9 pp |
| All other categories (avg) | +0.7 pp |

For non-symbolic categories, mean performance with CoT was 56.8 vs. 56.1 without — a difference the authors decline to characterize as meaningful. Original experiments confirm: [[themes/mathematical_and_formal_reasoning|math benchmarks]] show CoT gains as large as 41.6% (MATH) and 66.9% (GSM8K), while commonsense datasets (CSQA, PIQA, SiQA), language understanding (WinoGrande), and reading comprehension (ARC, AGI LSAT) show near-zero separation.

Few-shot CoT prompts perform similarly to zero-shot CoT prompts; the prompting regime has little impact on *when* CoT helps.

### MMLU's "reasoning" gains are almost entirely math

As much as 95% of CoT's total performance gain on MMLU — one of the most-cited broad [[themes/evaluation_and_benchmarks|reasoning benchmarks]] — is attributable to questions whose text or generated response contains an `=` sign, indicating math-related symbolic operations. For non-math MMLU questions, no features reliably predict when CoT will help. This `=` heuristic provides a practical, lightweight signal for selective CoT application: restrict CoT to contexts involving symbolic computation.

### CoT helps execution, not planning

The planning/execution decomposition reveals that CoT's gains are concentrated in **execution** — tracing intermediate computation — not in problem formulation. Having a plan alone (Plan + Direct Solver) accounts for little of CoT's performance gain. Plan + CoT Solver is needed for strong performance. This implies CoT is functioning as an inline symbolic interpreter, not as a higher-level reasoning scaffold.

### External solvers dominate CoT on symbolic tasks

Plan + Tool Solver (external symbolic solver) dominates both CoT and Plan + CoT Solver across nearly all models and datasets tested on GSM8K, GSM8K-Hard, ContextHub, and FOLIO. CoT functions as a weak, universal approximation to symbolic solvers — present when tools are unavailable, but clearly inferior when they are. The implication: for symbolic tasks, [[themes/reasoning_and_planning|LLMs should be paired with symbolic solvers at inference time]] wherever possible.

### Outlier datasets contain hidden symbolic structure

Datasets that appeared to contradict the pattern largely contained concealed symbolic operations: BIG-Bench Hard includes arithmetic counting (Navigate) and deductive temporal reasoning; MMLU-Moral Scenarios requires combining two independent sub-questions symbolically; Legal Argument Reasoning (SemEval-2024) demands substantial deductive inference. Genuine exceptions to the math/symbolic pattern are scarce once this structure is recognized.

---

## Limitations and Open Questions

**CoT cannot improve non-symbolic reasoning.** On commonsense, language understanding, and reading comprehension, CoT provides no meaningful benefit. Whether this reflects a fundamental pre-training limitation or an architectural and training gap is unknown — a critical open question for general reasoning improvement.

**Pre-planning fails to transfer benefits.** Generating a solution plan before a free-form response yields only mild improvement on BiGGen Bench and does not account for most CoT gains. Pre-planning alone is insufficient for unlocking reasoning capabilities in open-ended generation contexts.

**Compute-unfair comparisons.** CoT produces substantially more tokens than direct answering. A valid comparison requires compute-matched baselines — e.g., ensembling multiple direct-answer samples — which most existing evaluations omit. Reported CoT gains may be partly attributable to additional compute rather than the reasoning structure itself.

**Publication bias in reasoning benchmarks.** Many "reasoning" methods for LLMs are evaluated exclusively on math tasks while claiming general reasoning improvements. This systematic bias — documented across ICLR 2024, EACL 2024, and NAACL 2024 — has produced an inflated view of CoT's generality. [[themes/benchmark_design|Benchmark design]] practices need to diversify task coverage and explicitly separate symbolic from non-symbolic reasoning.

**Data contamination unaddressed.** Most CoT evaluations, including this study, do not control for model contamination on benchmark content, potentially inflating apparent gains where models may have memorized benchmark items.

---

## Implications

**Selective CoT application is sufficient and cost-efficient.** Since CoT benefits concentrate in symbolic and math domains, applying it only there maintains aggregate performance while eliminating unnecessary inference costs on the majority of tasks. The `=` heuristic provides a simple routing signal.

**Prompt-based CoT is neither the most powerful nor the most general paradigm.** On symbolic tasks where CoT genuinely helps, tool-augmented approaches already outperform it. On non-symbolic tasks where tools don't apply, CoT fails to help. This positions CoT as an interim technique — valuable without tool access, outpaced when tools are available.

**The field needs post-CoT reasoning paradigms.** For non-symbolic domains (commonsense, soft reasoning), the paper motivates research into approaches that better leverage intermediate computation: search, interacting multi-agent systems, or models fine-tuned to develop new deliberation modes (e.g., process of elimination for multiple choice) rather than relying on CoT's symbolic execution strength.

**Evaluation reform is necessary.** Credible claims about reasoning capability improvements require benchmark suites that explicitly separate symbolic from non-symbolic reasoning, enforce compute-fair comparisons, and are not dominated by math tasks.

---

## Themes

- [[themes/chain_of_thought|Chain-of-Thought Prompting]]
- [[themes/reasoning_and_planning|Reasoning and Planning]]
- [[themes/mathematical_and_formal_reasoning|Mathematical and Formal Reasoning]]
- [[themes/evaluation_and_benchmarks|Evaluation and Benchmarks]]
- [[themes/benchmark_design|Benchmark Design]]

## Key Concepts

- [[entities/chain-of-thought-prompting|Chain-of-Thought Prompting]]
- [[entities/gsm8k|GSM8K]]
- [[entities/llm-as-a-judge|LLM-as-a-Judge]]
- [[entities/mmlu|MMLU]]
- [[entities/musique|MuSiQue]]
