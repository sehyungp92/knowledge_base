---
type: source
title: Reasoning LLMs are Wandering Solution Explorers
source_id: 01KJTSBRDCSG1M2EPCGYDH94HS
source_type: paper
authors:
- Jiahao Lu
- Ziwei Xu
- Mohan Kankanhalli
published_at: '2025-05-26 00:00:00'
theme_ids:
- alignment_and_safety
- benchmark_design
- chain_of_thought
- evaluation_and_benchmarks
- hallucination_and_reliability
- reasoning_and_planning
- search_and_tree_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 17
tags: []
---
# Reasoning LLMs are Wandering Solution Explorers

**Authors:** Jiahao Lu, Ziwei Xu, Mohan Kankanhalli
**Published:** 2025-05-26 00:00:00
**Type:** paper

## Analysis

# Reasoning LLMs are Wandering Solution Explorers
2025-05-26 · paper · Jiahao Lu, Ziwei Xu, Mohan Kankanhalli
https://arxiv.org/pdf/2505.20296

---

### Motivation & Prior Limitations
Test-time computation (TTC) techniques — chain-of-thought prompting, tree-based reasoning, long chain reasoning — have been widely adopted under the assumption that allowing models to "think longer" leads to more thorough exploration of the solution space, and thus better answers.
- This assumption is challenged by the paper: longer thinking does not imply better or more systematic thinking, and existing RLLMs (GPT-o3, Sonnet-3.7, DeepSeek-R1) lack the ability to systematically traverse solution spaces.
  - Models exhibit performance "plateaus" at low problem complexity, particularly when multiple valid solutions exist, creating misleading impressions of robustness on shallow benchmarks.
  - The mathematical model in Equation 1 shows that success probability drops exponentially with search depth d for wandering RLLMs, but this deterioration remains hidden until a problem complexity threshold is crossed — at which point performance collapses abruptly.
- There is no established, standardized method for auditing the quality of reasoning traces rather than just final outputs, because tasks often lack uniform solution procedures, natural language reasoning is ambiguous to evaluate step-by-step, and real-world solution spaces are too large to specify ground-truth traces.

---

### Proposed Approach
The paper formalizes what constitutes systematic problem solving and provides a structured audit methodology to detect and classify failures in reasoning traces, shifting evaluation from final-answer accuracy to the structure of the reasoning process itself.
- Systematic exploration is defined via three formal properties applied to a reasoning trace J over a problem P = (S, T, s0, G): (a) **validity** — every state transition must conform to the problem's reachability structure T; (b) **effectiveness** — the trace must reach at least one goal state; (c) **necessity** — every state in the trace must be necessary, meaning removing it would either invalidate the trace or reduce the count of goals or dead-ends reachable.
  - This formalization distinguishes purposeful exploration from the "wandering" pattern where models generate superfluously large or structurally incoherent traces without guaranteeing coverage.
- Failure modes are taxonomized into three classes: **Invalid Explorations** (boundary violation, procedure omission, incorrect backtracking), **Unnecessary Explorations** (state revisitation, infinite self-loop), and **Evaluation Errors** (state staleness, execution error, unfaithful conclusion).
- To enable reliable auditing, the authors project real-world reasoning problems into well-defined computational tasks with three required properties: controllable problem size (reasoning steps scale with problem specifications), verifiable traces (decomposable into atomic steps in a shared symbolic system), and canonical solution procedures. Eight tasks are selected: Counting Elements, Sliding Window Max, Flood Fill, Edit Distance, Hierarchical Clustering Order, Prime Number Factorization, Permutation with Duplicates, and the 24 Game.
  - Format constraints are imposed on model outputs so that traces can be audited by rule-based string-level processors against programmatically generated ground-truth traces, enabling precise failure-mode attribution rather than just binary correctness scoring.

---

### Results & Capabilities
No existing RLLM demonstrates systematic problem solving consistently across different problem classes and scales — all models exhibit at least some failure modes from all three categories across the eight evaluated tasks.
- The mathematical analysis shows that a wandering agent's success probability follows ps(d, m, qw) = 1 − (1 − qw^(d−1))^m, where d is search depth, m is the number of valid solutions, and qw is per-step systematic accuracy; success degrades exponentially in d regardless of the value of qw < 1, with plateau regions at small d and large m masking the underlying fragility.
- **Boundary violations** are observed when models rely excessively on local context and fail to maintain global constraint awareness — for example, RLLMs hallucinate non-existent characters by referencing position indices beyond actual string length in counting tasks, or reuse numbers in the 24 Game in violation of game rules.
- **Procedure omissions** occur when models lack backtracking criteria or a global plan, causing premature termination before covering required sub-regions of the search space — e.g., enumerating only a subset of permutations.
- **Incorrect backtracking** corrupts subsequent search trajectories by restoring inconsistent partial states during recursive or branching tasks such as DFS and permutation enumeration, producing redundant or missing branches.
- **State revisitation** and **infinite self-loops** manifest as the model revisiting already-explored states without a memory mechanism, or becoming stuck repeating a step without a loop-exit condition.
- **Unfaithful conclusions** — where the final stated answer is inconsistent with the model's own chain-of-thought trace — are identified as a distinct failure class, reflecting weak summarization rather than a reasoning failure per se.

---

### Implications
The findings directly undermine a foundational assumption of the TTC scaling paradigm: that inference-time compute translates into qualitatively better reasoning rather than just longer wandering through the solution space.
- Benchmark evaluations that use problems with shallow reasoning depth (small d) and many valid solutions (large m) systematically overestimate RLLM capability, creating illusions of near-perfect performance that will not transfer to more complex deployment conditions — this is a structural evaluation problem, not a marginal accuracy gap.
- The exponential degradation t

## Key Claims

1. Current reasoning LLMs lack the ability to systematically explore the solution space and are wanderers rather than systematic explorers.
2. Longer thinking via test-time computation does not necessarily make reasoning LLMs think better.
3. Wandering exploration causes exponential performance deterioration as problem complexity grows.
4. Performance deterioration from wandering exploration may remain hidden for small to moderately complex problems, creating illusions of perfect performance on limited benchmarks.
5. The success probability for a wandering RLLM drops exponentially with reasoning depth d, following the formula ps(d, m, qw) = 1 − (1 − qw^(d−1))^m.
6. RLLMs exhibit performance plateaus at low problem depth (especially when multiple solutions exist) that mislead evaluators into believing the models are more capable than they are.
7. None of the existing reasoning LLMs demonstrate systematic problem solving capabilities consistently over different problem classes and scales.
8. Systematic exploration must satisfy three properties: validity (traces must follow reachability structure), effectiveness (must reach a goal), and necessity (every state must contribute to goal discov
9. Auditing LLM reasoning traces is difficult due to lack of standardized procedures, difficulties evaluating individual reasoning steps, and huge solution spaces.
10. The paper projects real-world problems into well-defined computational tasks with structured solution spaces to enable reliable auditing of reasoning traces using rule-based, string-level processors.

## Capabilities

- State-of-the-art reasoning LLMs (GPT-o3, Claude Sonnet-3.7, DeepSeek-R1) demonstrate strong benchmark performance on computational reasoning tasks via test-time computation techniques including chain-of-thought, tree-based reasoning, and long-chain reasoning

## Limitations

- Reasoning LLMs exhibit exponential performance degradation as problem complexity increases — success probability drops exponentially with reasoning depth (d), while near-perfect performance on shallow benchmarks creates a misleading 'plateau' that masks this fundamental collapse
- Current reasoning LLMs cannot perform systematic solution space exploration — they fail the three core properties: validity (generating transitions that violate problem constraints), effectiveness (missing goal states), and necessity (including redundant states) — across all tested state-of-the-art 
- 'Longer thinking' via test-time computation does not guarantee systematic or qualitatively better reasoning — increased compute budget enables more wandering but not more structured exploration of solution spaces
- Reasoning LLMs generate boundary violations — exploring states outside the defined problem space (illegal indices, out-of-bounds coordinates, reusing consumed operands) due to over-reliance on local context rather than maintaining global constraint awareness
- Reasoning LLMs perform procedure omissions — prematurely terminating reasoning before covering necessary sub-regions of the search space, producing incomplete solutions due to lack of backtracking criteria and global planning
- Reasoning LLMs fail at backtracking — restoring inconsistent or outdated partial states when reverting to previous decision points, corrupting subsequent search trajectories in tasks requiring recursive or DFS-style exploration
- Reasoning LLMs revisit already-explored states and partial solutions (state revisitation) due to lack of state maintenance, causing redundant computation and in extreme cases infinite loops — particularly in graph traversal, subset enumeration, and DP memoization tasks
- Reasoning LLMs suffer from state staleness — using outdated problem states during dynamic subproblem tasks (DP, recursive reductions) because they lack working memory management, causing invalid intermediate reasoning steps
- Reasoning LLMs produce unfaithful conclusions — final answers inconsistent with the reasoning trace generated, revealing a structural disconnect between the thinking process and the conclusion, even when the reasoning trace was correct
- Reasoning benchmarks create a systematic capability illusion — RLLMs score near-perfect on tasks with shallow reasoning depth and multiple valid solutions, but this plateau conceals exponential degradation that only emerges when task complexity crosses a threshold
- No standardized methodology exists for auditing the quality of LLM reasoning processes — ambiguity of natural language, absence of canonical solution procedures, and vast solution spaces make reliable step-level evaluation infeasible for most real-world tasks

## Bottlenecks

- Reasoning LLMs lack structured solution-space exploration — all current models wander probabilistically through search spaces rather than maintaining systematic coverage guarantees, causing exponential performance degradation on complex tasks while benchmark plateaus conceal this structural failure 
- Absence of process-aware reasoning evaluation tools — current metrics assess only final outputs, not reasoning trace quality (validity, necessity, effectiveness), making it impossible to systematically detect or train against wandering failure modes

## Themes

- [[themes/alignment_and_safety|alignment_and_safety]]
- [[themes/benchmark_design|benchmark_design]]
- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]]
- [[themes/hallucination_and_reliability|hallucination_and_reliability]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/search_and_tree_reasoning|search_and_tree_reasoning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/chain-of-thought-prompting|Chain-of-Thought Prompting]]
