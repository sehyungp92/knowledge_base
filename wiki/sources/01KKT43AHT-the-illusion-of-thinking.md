---
type: source
title: 'The Illusion of Thinking:'
source_id: 01KKT43AHTG56N92XRTA1GB293
source_type: paper
authors: []
published_at: '2025-06-04 00:00:00'
theme_ids:
- alignment_and_safety
- benchmark_design
- chain_of_thought
- evaluation_and_benchmarks
- hallucination_and_reliability
- reasoning_and_planning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# The Illusion of Thinking:

**Authors:** 
**Published:** 2025-06-04 00:00:00
**Type:** paper

## Analysis

# The Illusion of Thinking:
2025-06-04 · paper
https://ml-site.cdn-apple.com/papers/the-illusion-of-thinking.pdf

---

### Motivation & Prior Limitations
- Current evaluations of Large Reasoning Models (LRMs) rely almost exclusively on established mathematical and coding benchmarks, which are insufficient for understanding the fundamental capabilities, scaling properties, and failure modes of these models.
  - Benchmarks like MATH-500 and AIME suffer from data contamination: models perform worse on AIME25 than AIME24 despite AIME25 being easier for humans, strongly suggesting training data leakage rather than genuine capability differences.
  - Existing evaluation paradigms measure only final answer accuracy and provide no insight into the structure, quality, or efficiency of intermediate reasoning traces.
- It remains unclear whether LRM performance gains stem from genuine reasoning capabilities developed via reinforcement learning, increased exposure to benchmark data during training, or simply greater inference-time compute allocation.
  - Pass@k analyses on MATH-500 show that non-thinking LLMs given equivalent token budgets reach comparable performance to thinking models, raising questions about whether extended chain-of-thought provides real reasoning advantages or just probabilistic coverage.

---

### Proposed Approach
- The authors introduce a controlled experimental testbed using four algorithmic puzzle environments — Tower of Hanoi, Checker Jumping, River Crossing, and Blocks World — that allow precise manipulation of compositional complexity while holding logical structure constant.
  - Unlike standard benchmarks, these puzzles offer fine-grained control over difficulty (e.g., number of disks, checkers, or crossing pairs), are unlikely to appear verbatim in training data, require only explicitly provided rules (no world knowledge), and support simulator-based verification of both final answers and every intermediate step in the reasoning trace.
  - This setup enables a novel dual analysis: correctness of the final answer AND correctness, position, and density of intermediate solutions extracted from the model's `<think>` tokens, allowing quantitative characterization of reasoning behavior as a function of complexity.
- The study evaluates frontier LRMs including o3-mini (medium and high), DeepSeek-R1, DeepSeek-R1-Qwen-32B, and Claude-3.7-Sonnet-Thinking, paired against their non-thinking counterparts (DeepSeek-V3, Claude-3.7-Sonnet without thinking), with up to 25 samples per puzzle instance and a 64k token budget.

---

### Results & Capabilities
- All tested LRMs exhibit complete accuracy collapse to zero beyond a model-specific complexity threshold across all four puzzle environments, regardless of available token budget.
  - Claude-3.7-Sonnet-Thinking achieves near-perfect accuracy on Tower of Hanoi with N=5 (31 required moves) but fails entirely at higher N; DeepSeek-R1 and o3-mini show the same collapse pattern across all puzzles.
- Three distinct performance regimes emerge as a function of complexity: (1) at low complexity, standard non-thinking LLMs match or outperform LRMs while using fewer tokens; (2) at medium complexity, LRMs gain a meaningful advantage through extended chain-of-thought; (3) at high complexity, both model types collapse to zero accuracy regardless of compute allocation.
  - Pass@k analysis confirms this three-regime structure in puzzle environments, whereas math benchmarks only reveal the medium-complexity advantage, masking both the low-complexity inefficiency and the high-complexity collapse.
- LRMs exhibit a counterintuitive scaling limit: thinking token usage initially increases with problem complexity but then *decreases* as problems approach the collapse threshold, despite the models operating well below their 64k token generation limits.
  - This phenomenon is most pronounced in o3-mini variants and less severe in Claude-3.7-Sonnet-Thinking, and occurs consistently across all four puzzle types, suggesting an intrinsic compute-scaling ceiling rather than a token-budget constraint.
- Analysis of intermediate reasoning traces reveals complexity-dependent patterns: at low complexity, correct solutions appear early and the model wastes tokens continuing to explore incorrect alternatives ("overthinking"); at medium complexity, the model explores many incorrect paths before eventually finding the correct solution; at high complexity, no correct intermediate solutions appear at any point in the trace.
  - For Tower of Hanoi, solution accuracy within sequential segments of the thinking trace decreases or oscillates for small N (overthinking signature) but increases with progression for moderate N — up to the collapse threshold.
- Providing the explicit recursive algorithm for Tower of Hanoi directly in the prompt does not improve performance: accuracy collapse occurs at approximately the same complexity point as without the algorithm.
  - This result isolates a fundamental limitation in exact symbolic execution: LRMs cannot reliably follow prescribed logical steps even when search and solution-finding are removed from the task.
- LRMs demonstrate highly inconsistent reasoning across puzzle types that cannot be explained by complexity alone: Claude-3.7-Sonnet-Thinking produces up to ~100 correct consecutive moves in Tower of Hanoi (N=10) but fails after only ~4 correct moves in River Crossing (N=3), despite River Crossing requiring only 11 total moves at that complexity.
  - This inconsistency likely reflects training data distribution: Tower of Hanoi is abundant on the web, while River Crossing instances with N>2 are rare, suggesting LRM performance is partially pattern-matching against memorized solution structures rather than generalizable planning.

---

### Implications
- The three-regime complexity finding challenges the prevailing assumption that extended chain-of-thought reasoning uniformly improves performance: for simple tasks it wastes comp

## Key Claims

1. Frontier LRMs face a complete accuracy collapse beyond certain problem complexity thresholds across all tested puzzle environments
2. LRMs exhibit a counterintuitive scaling limit where reasoning effort (measured by thinking tokens) increases with problem complexity up to a point, then declines despite having an adequate token budge
3. Three distinct performance regimes exist when comparing LRMs to standard LLMs: (1) low-complexity tasks where standard models outperform LRMs, (2) medium-complexity tasks where LRMs demonstrate advant
4. LRMs fail to use explicit algorithms to improve performance; providing the Tower of Hanoi solution algorithm in the prompt does not improve performance and collapse occurs at roughly the same complexi
5. LRMs reason inconsistently across puzzle types; Claude 3.7 Sonnet Thinking can produce ~100 correct moves in Tower of Hanoi (N=10) but fails after only ~4 moves in River Crossing (N=3)
6. On the MATH-500 benchmark, thinking models' pass@k performance is comparable to non-thinking counterparts when provided with the same inference token budget
7. Models perform worse on AIME25 than AIME24, despite human performance being higher on AIME25, suggesting data contamination during training of frontier LRMs on AIME24
8. At low complexity, LRMs exhibit 'overthinking': they find the correct solution early in their reasoning trace but continue exploring incorrect alternatives, wasting compute
9. At medium complexity, LRMs first explore incorrect solutions and only arrive at correct ones later in the thinking trace, suggesting that extended reasoning is genuinely useful in this regime
10. In failed cases at high complexity, LRMs fixate on an early wrong answer and waste the remaining token budget rather than correcting course

## Capabilities

- Large Reasoning Models (LRMs) with extended chain-of-thought demonstrate superior performance over standard LLMs on medium-complexity planning and reasoning tasks, showing measurable advantage when compositional depth is moderate
- Reasoning models can explore and self-correct reasoning traces, finding correct solutions after initial incorrect paths in medium-complexity problems
- LRMs can execute up to ~100 sequential correct moves in well-represented planning tasks (Tower of Hanoi N=10), demonstrating extended multi-step reasoning within a single inference

## Limitations

- All frontier LRMs (o3-mini, DeepSeek-R1, Claude-3.7-Sonnet Thinking) experience complete accuracy collapse to zero beyond a model-specific complexity threshold — no amount of additional inference compute prevents this
- LRMs exhibit a counterintuitive inverse scaling phenomenon: reasoning effort (token usage) decreases as problem complexity approaches the collapse threshold, despite having ample token budget remaining
- Providing the explicit solution algorithm to LRMs does not improve performance — models still fail at the same complexity thresholds, indicating fundamental inability to execute prescribed logical steps
- LRMs reason inconsistently across structurally similar puzzle types — performance is dramatically better on tasks heavily represented in training data (Tower of Hanoi) versus tasks that are rare (River Crossing), independent of solution length
- LRMs exhibit 'overthinking' on simple problems — finding the correct solution early but wastefully continuing to explore incorrect alternatives, causing unnecessary inference compute overhead
- Standard math benchmarks (MATH-500, AIME24) are likely contaminated with training data, making it difficult to distinguish genuine reasoning capability gains from memorization
- Under equivalent inference token budgets, thinking and non-thinking models converge to comparable pass@k performance on MATH-500, suggesting LRM advantages on standard math benchmarks may not reflect genuine reasoning superiority
- LRMs fail to develop generalizable problem-solving from RL training — capabilities are domain-fragile and do not transfer to structurally novel but logically analogous problems
- Existing LRM evaluations are conducted on black-box API access, preventing analysis of internal states or architectural components that would explain observed failure modes
- LRM reasoning in failed cases shows fixation on an early incorrect solution, wasting the remaining token budget — active self-correction mechanisms are insufficient to escape local attractor states

## Bottlenecks

- LRMs lack a mechanism to scale reasoning effort proportionally with problem complexity — near their capability threshold, they reduce thinking tokens rather than increasing them, creating a hard ceiling on what extended reasoning can solve
- LRMs cannot execute exact sequential algorithmic computation reliably — even when given the algorithm, they fail to follow prescribed logical steps, blocking tasks requiring precise symbolic manipulation
- Benchmark contamination in established math/coding evaluations makes it impossible to reliably assess true reasoning capabilities of frontier models, blocking evidence-based progress tracking

## Breakthroughs

- Systematic controlled puzzle environments reveal three distinct complexity regimes that explain the relationship between problem difficulty and LRM vs. standard LLM performance — a previously unobservable structure hidden by benchmark contamination

## Themes

- [[themes/alignment_and_safety|alignment_and_safety]]
- [[themes/benchmark_design|benchmark_design]]
- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]]
- [[themes/hallucination_and_reliability|hallucination_and_reliability]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/chain-of-thought-cot|Chain-of-Thought (CoT)]]
- [[entities/reinforcement-learning-with-verifiable-rewards|Reinforcement Learning with Verifiable Rewards]]
- [[entities/passk|pass@k]]
