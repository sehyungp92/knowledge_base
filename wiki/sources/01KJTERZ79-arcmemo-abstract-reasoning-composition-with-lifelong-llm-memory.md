---
type: source
title: 'ArcMemo: Abstract Reasoning Composition with Lifelong LLM Memory'
source_id: 01KJTERZ79G152RV16WRGF0A3Q
source_type: paper
authors:
- Matthew Ho
- Chen Si
- Zhaoxiang Feng
- Fangxu Yu
- Yichi Yang
- Zhijian Liu
- Zhiting Hu
- Lianhui Qin
published_at: '2025-09-04 00:00:00'
theme_ids:
- agent_memory_systems
- continual_learning
- knowledge_and_memory
- post_training_methods
- pretraining_and_scaling
- test_time_learning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# ArcMemo: Abstract Reasoning Composition with Lifelong LLM Memory

**Authors:** Matthew Ho, Chen Si, Zhaoxiang Feng, Fangxu Yu, Yichi Yang, Zhijian Liu, Zhiting Hu, Lianhui Qin
**Published:** 2025-09-04 00:00:00
**Type:** paper

## Analysis

# ArcMemo: Abstract Reasoning Composition with Lifelong LLM Memory
2025-09-04 · paper · Matthew Ho, Chen Si, Zhaoxiang Feng, Fangxu Yu, Yichi Yang et al. (8 total)
https://arxiv.org/pdf/2509.04439

---

### Motivation & Prior Limitations
Inference-time scaling allows LLMs to perform extended reasoning, but all patterns and insights uncovered during these traces are discarded when the context window resets, meaning each query starts from scratch with no accumulated understanding — a stark contrast to how humans build on prior experience when solving compositional problems.
- Prior external memory approaches for reasoning tasks (e.g., Buffer of Thoughts, Yang et al. 2024) stored instance-level entries — query/response pairs or problem-specific summaries — that remain tightly coupled to their original context, limiting transfer to superficially different problems.
  - Instance-level memories capture composite solution patterns (e.g., ideas A∧B⇒C bundled together); when only part of a composite is relevant to a new problem, the model must actively disentangle the irrelevant components, creating unnecessary friction.
- Dynamic Cheatsheet (Suzgun et al. 2025) partially addresses instance-specificity by maintaining an evolving unified buffer, but its lack of modularity makes scaling with more experiences difficult: without selective retrieval the full buffer must be appended to every prompt, capping memory size and burdening the model with irrelevant content.
- Test-time weight adaptation approaches (Akyürek et al. 2025) face a complementary problem: low-rank adapters are poorly suited to retaining practical experience across puzzles, and weight updates are expensive relative to the inference budget.

---

### Proposed Approach
ArcMemo introduces a concept-level external memory framework that distills solution traces into reusable, modular natural-language abstractions rather than storing full problem-solution pairs, enabling test-time continual learning without any weight updates.
- The framework is defined by three operations: Memory Format (what is stored), Memory Write (how traces are converted to entries), and Memory Read (how entries are selected for a new query); the core novelty lies in designing all three to prioritize abstraction and modularity over specificity.
- Two format implementations are explored: Open-Ended (OE), which imposes a minimal "situation X → suggestion Y" structure and defers formatting to the model; and Program Synthesis (PS), which frames concepts as parameterized types, structures, and routines with typed input/output interfaces and support for higher-order functions, directly encoding composability.
  - PS abstraction first converts solutions to pseudocode to suppress low-level implementation details, then runs a memory-aware writing pass that can revise existing concepts rather than always appending new ones, using a compressed memory representation to keep context tractable.
- Memory Read for PS uses reasoning-model-driven exploration (System 2-style selection): the model first identifies candidate concepts via relevance cues, then uses type annotations to explore which other concepts can compose with them — addressing the problem that abstract concepts resist standard embedding similarity retrieval.
  - OE selection uses a lightweight preprocessing step: a vision-language model converts the spatial ARC puzzle into a natural-language description at multiple abstraction levels, then a top-k query against stored situation clauses identifies relevant entries.
- Continual updating is supported natively: memory write operations are lightweight LLM queries that can ingest traces from either the system itself or external sources, and the framework explicitly supports updates during test evaluation with a configurable update interval k.

---

### Results & Capabilities
ArcMemo-PS is the only memory design that consistently outperforms the no-memory baseline across all tested inference compute scales on ARC-AGI-1, achieving an official score of 59.33 versus the no-memory baseline of 55.17 (a +7.5% relative gain), and further improving to 70.83 with two sequential retries.
- ArcMemo-PS is the only evaluated method to beat the baseline at every inference scale; competing approaches (Cheatsheet, ArcMemo-OE) surpass the baseline in some regimes but fall below it in others, suggesting their improvements are not robust.
- The memory advantage is largest at low inference compute and diminishes as compute increases, consistent with the hypothesis that memory reduces redundant rediscovery — with sufficient compute, the model can re-derive ideas through exploration alone.
- Ablating the reasoning-based selection mechanism from ArcMemo-PS reduces official score from 59.33 to 55.17 at zero retries, confirming selection is essential not only for context efficiency but for downstream solve quality; importantly, the selection-free variant also consumes far more tokens.
- Qualitative analysis of new solves attributable to memory shows 100% of ArcMemo-PS new solves can be linked to specific concept memory contents, versus only 40% for the Cheatsheet baseline — suggesting ArcMemo's improvements are more causally traceable to the memory component rather than sampling variance.
- Continual memory updating during evaluation improves performance, but only at higher sequential retry depths (2 retries), consistent with the mechanism: new solutions are found in later passes, new memories are abstracted, and those memories unlock further solves in subsequent passes.

---

### Implications
The paper demonstrates that moving from instance-level to concept-level memory is a qualitatively important design axis for reasoning-augmented LLMs: modularity and abstraction determine whether a memory system scales gracefully with accumulated experience or degrades from overspecification and context saturation.

- For retrieval-augmented generation, the work shows that standard embedding-similarity retrieval

## Key Claims

1. LLMs discard all patterns and insights uncovered during inference-time reasoning once the context window is reset for a new query.
2. Instance-level memory entries have diminished utility for problems that are superficially different from the experiences they were derived from.
3. ArcMemo-PS achieves a 7.5% relative gain over a strong no-memory baseline on ARC-AGI-1, improving official score from 55.17 to 59.33.
4. ArcMemo-PS is the only memory design that consistently outperforms the no-memory baseline at all tested inference compute scales.
5. Abstract concept-level memory outscores the no-memory baseline at all tested inference compute scales, making it the most consistent memory design.
6. Continual memory updates improve puzzle-solving performance specifically at high sequential retry depth, not at zero retries.
7. The performance benefit of memory over the no-memory baseline diminishes at higher inference compute because models can rediscover ideas through exploration.
8. Concept selection improves downstream problem-solving performance and substantially reduces token cost compared to including all memory entries.
9. 100% of new solves from ArcMemo-PS (without selection) can be linked to concept memory contents, compared to only 40% for the Dynamic Cheatsheet.
10. Standard embedding-based retrieval represents System 1-style intuition that may be insufficient for frontier reasoning tasks, particularly when concepts are highly abstract.

## Capabilities

- Abstract concept-level external memory — storing modular, parameterized concepts distilled from solution traces rather than instance-level query/response pairs — achieves consistent gains on compositional reasoning benchmarks at all inference compute scales, with ArcMemo-PS improving ARC-AGI-1 offic
- Test-time continual learning via external concept memory — accumulating and abstracting patterns during evaluation without any weight updates — produces measurable self-improvement over multiple inference passes on compositional reasoning tasks
- Reasoning-model-driven (System 2) memory selection — using structured exploration with backtracking to identify relevant abstract concepts for a given problem — outperforms embedding-based (System 1) retrieval for highly abstract memory entries while simultaneously reducing token cost
- Functional-programming-style parameterized concept memory — framing stored concepts as typed types, structures, and routines with higher-order function support — enables compact representation of concept families and explicit interface-guided composition of abstract reasoning strategies

## Limitations

- Credit assignment for failed reasoning traces is unsolved — the system cannot learn from incorrect solution attempts because identifying which parts of a failed trace were valuable vs. harmful remains an open problem, so only successful traces update memory
- Abstract concept-level memory renders standard embedding-based retrieval ineffective — the semantic gap between a concrete problem instance and a highly abstract concept is too large for cosine similarity to bridge reliably at scale
- Memory advantage over no-memory baselines diminishes and disappears at high inference compute — the model can rediscover stored patterns through exploration given sufficient compute, making memory primarily useful only in the compute-constrained regime
- The memory system requires an externally verifiable feedback signal at inference time to operate — tasks without automatic test cases, execution feedback, or self-reflection criteria cannot use continual memory updates at all
- Continual memory updates introduce evaluation-order dependencies that create a fundamental accuracy-throughput trade-off — parallel inference batching prevents ordering guarantees, so maximising throughput sacrifices the cross-problem learning signal
- Flat, unstructured memory organisation with no consolidation mechanism limits scalability — as the concept library grows, structural redundancy and unresolved conflicts between entries accumulate without any pruning or hierarchical reorganisation
- OE memory write operations are unaware of existing memory contents, producing redundant or overlapping entries — deduplication and consolidation are deferred entirely to downstream retrieval and problem-solving stages
- Low-rank adapters (LoRA) are poorly suited for retaining practical cross-task experience during test-time weight adaptation on compositional reasoning — parametric weight adaptation via LoRA fails to accumulate generalizable knowledge across unrelated ARC puzzles
- DeepSeek R1's 8000 output token limit causes systematic failure on complex compositional reasoning tasks — solutions are consistently left incomplete, making the model unusable for problems requiring extended generation chains
- 60% of new puzzle solves attributed to non-modular cheatsheet memory cannot be linked to any relevant memory content — the mechanism by which unstructured memory helps (if it does) is opaque, suggesting sampling variance rather than genuine knowledge transfer explains most gains
- Reasoning-based memory selection still introduces irrelevant distractor concepts into context — even System 2 exploration cannot reliably predict abstract concept relevance before attempting the problem, leaving headroom for improvement

## Bottlenecks

- Abstract concept memory cannot use standard embedding retrieval — high-level abstractions lack surface-level semantic overlap with concrete problem instances, so cosine-similarity-based lookup systematically misses relevant entries as the concept library scales

## Breakthroughs

- Abstract modular concept-level memory consistently outperforms instance-level memory and unstructured cheatsheet memory at every tested inference compute scale on ARC-AGI — establishing concept abstraction as a strictly superior memory design with attributable, verifiable gains

## Themes

- [[themes/agent_memory_systems|agent_memory_systems]]
- [[themes/continual_learning|continual_learning]]
- [[themes/knowledge_and_memory|knowledge_and_memory]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/pretraining_and_scaling|pretraining_and_scaling]]
- [[themes/test_time_learning|test_time_learning]]

## Key Concepts

- [[entities/arc-agi-1|ARC-AGI-1]]
- [[entities/dynamic-cheatsheet|Dynamic Cheatsheet]]
- [[entities/o4-mini|o4-mini]]
