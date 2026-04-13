---
type: source
title: 'Beyond Semantics: The Unreasonable Effectiveness of Reasonless Intermediate
  Tokens'
source_id: 01KJTTV05KQ6NC72PZTZMNSWG8
source_type: paper
authors:
- Karthik Valmeekam
- Kaya Stechly
- Vardhan Palod
- Atharva Gundawar
- Subbarao Kambhampati
published_at: '2025-05-19 00:00:00'
theme_ids:
- chain_of_thought
- latent_reasoning
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Beyond Semantics: The Unreasonable Effectiveness of Reasonless Intermediate Tokens

**Authors:** Karthik Valmeekam, Kaya Stechly, Vardhan Palod, Atharva Gundawar, Subbarao Kambhampati
**Published:** 2025-05-19 00:00:00
**Type:** paper

## Analysis

# Beyond Semantics: The Unreasonable Effectiveness of Reasonless Intermediate Tokens
2025-05-19 · paper · Karthik Valmeekam, Kaya Stechly, Vardhan Palod, Atharva Gundawar, Subbarao Kambhampati
https://arxiv.org/pdf/2505.13775

---

### Motivation & Prior Limitations
The field has widely assumed that Chain-of-Thought (CoT) intermediate tokens improve model performance because they constitute semantically meaningful reasoning steps — an assumption that is nearly impossible to verify in large frontier models whose training data and procedures are opaque and whose outputs are polysemantic natural language.
- Anthropomorphic framings pervade the literature: claims about models "thinking," "deliberating," or experiencing "aha moments" imply that intermediate tokens faithfully reflect internal computation, yet no controlled study had directly tested whether this semantic content is what drives the performance gains.
  - Worrying downstream consequences exist on both ends: some works treat CoT traces as evidence of deceptive behavior (raising safety concerns), while others call for keeping chains-of-thought monitorable for AI safety — both positions depend on traces being semantically faithful.
- Prior evaluations of trace faithfulness (CoT faithfulness literature) relied on large pre-trained models and messy manual or LLM-based evaluations, since natural language traces lack formal ground truth, making it impossible to cleanly disentangle whether performance improvements come from trace semantics or from something else entirely.
- Earlier work that trained transformers from scratch on formal search traces (Searchformer, Stream of Search) demonstrated performance improvements from trace-augmented training but did not evaluate whether the model-generated traces at inference time were actually valid, leaving the causal mechanism of the improvement unexamined.

---

### Proposed Approach
The paper designs a controlled "model organism" study: 0.5B-parameter Qwen2.5 models are trained entirely from scratch on a formally verifiable domain — shortest-path planning in 30×30 grid mazes — using linearized A* execution traces as intermediate tokens, allowing rigorous formal validation of both solutions and traces.
- The key technical contribution is a formal A* trace verifier that replays model-generated token sequences against ground-truth open/closed list semantics, flagging precise error types (parsing errors, invalid neighbor expansions, already-closed node re-closures, missing goal closure), enabling the first clean binary distinction between trace-valid and trace-invalid responses.
- To test whether trace semantics are load-bearing, the authors construct **Swapped** training datasets in which A* traces from one problem are randomly permuted to accompany a different, unrelated problem — preserving trace form and generic domain statistics while entirely severing any connection between the trace and the problem it accompanies.
- Five structurally diverse maze generation algorithms (Wilson's, Kruskal's, DFS, Drunkard's Walk, Searchformer-style) are used to construct both in-distribution and out-of-distribution test sets, enabling measurement of how trace semantics affect generalization; GRPO-based RL post-training is layered on top to test whether reinforcement learning recovers semantic correctness.

---

### Results & Capabilities
Models trained on corrupted (Swapped) traces — whose intermediate steps bear zero relation to the problem being solved — achieve plan accuracy comparable to, and frequently exceeding, models trained on correct A* traces, despite maintaining 0% trace validity across all evaluation distributions.
- On in-distribution Wilson mazes, the Swapped Wilson model achieves 83.3% plan accuracy vs. 79.9% for the Normal model; on out-of-distribution Drunkard mazes the Swapped model achieves 11.7% vs. the Normal model's 0.0%, demonstrating superior generalization despite semantically incoherent traces.
- For SF-style trained models the effect is even more pronounced: Swapped SF achieves 95.4% on Drunkard mazes and 89.1% on SF-style mazes vs. 62.1% and 56.2% respectively for Normal SF, reversing what one would expect if semantic correctness were driving performance.

Even for models trained on correct traces, solution correctness and trace validity are only loosely coupled — models frequently produce invalid reasoning traces while arriving at correct solutions, with the correlation deteriorating sharply as problem difficulty increases.
- For the Wilson length-generalization experiment, trace validity within valid plans falls from 93.2% on easy problems (0–1000 tokens) to 51.8% on the hardest out-of-distribution problems (4000–4500 tokens), showing that the apparent correlation is an artifact of training distribution proximity rather than a fundamental property.

GRPO post-training improves solution accuracy across both in- and out-of-distribution settings but does not improve trace validity, and in several cases actively degrades it.
- For SF-style Normal models, GRPO training over 140 checkpoints raises plan accuracy substantially while trace validity falls monotonically from ~89% to ~52%; Swapped models post-trained with GRPO reach 99.5% plan accuracy on Wilson mazes while maintaining 0% trace validity, demonstrating that RL optimization pressure on final answers has no corrective effect on intermediate token semantics.

Trace length is largely uncorrelated with the computational complexity of the underlying problem, undermining inference-time scaling interpretations.
- Scatter plots of model-generated trace length against ground-truth A* trace length show high dispersion with no meaningful correlation; apparent alignment in the Wilson in-distribution setting disappears entirely when the same model is evaluated on SearchFormer-style mazes, indicating that any length-complexity correlation is a training-distribution artifact.

---

### Implications
These results challenge the foundational a

## Key Claims

1. Models trained on entirely correct reasoning traces can still produce invalid reasoning traces even when arriving at correct solutions.
2. Models trained on corrupted traces — whose intermediate reasoning steps bear no relation to the problem they accompany — achieve performance largely comparable to those trained on correct traces.
3. Corrupted-trace models generalize better on out-of-distribution tasks than models trained on correct traces.
4. GRPO-based RL post-training improves solution accuracy but does not improve trace validity.
5. Reasoning trace length is largely agnostic to the underlying computational complexity of the problem being solved, undermining the notion that longer traces reflect inference-time scaling.
6. The effectiveness of intermediate tokens does not arise from their seemingly interpretable semantic content.
7. Interpreting tokens like 'aha' in DeepSeek R1 as semantically meaningful requires an often-overlooked assumption that traces are interpretable to end users in the same way as the traces the model was 
8. DeepSeek R1's training procedure pays attention only to the correctness of the solution, ignoring the content of the traces; incorrect traces that happen to lead to correct answers are treated identic
9. Rewarding intermediate correctness during RL training might actually be counterproductive for final answer accuracy.
10. For large production RL-post-trained models like DeepSeek R1, formally verifying reasoning traces is practically impossible due to natural language ambiguity.

## Capabilities

- Transformer models achieve task accuracy using semantically irrelevant intermediate tokens — tokens describing the solution process for a completely different problem — performing comparably to or better than models trained on semantically correct reasoning traces
- GRPO-based RL post-training consistently improves solution accuracy on both in-distribution and out-of-distribution tasks regardless of whether training traces are semantically valid or entirely irrelevant to the problem

## Limitations

- Chain-of-thought traces do not reliably reflect actual model computation — models frequently produce correct solutions via invalid traces, and valid traces do not guarantee correct solutions; trace validity is a poor predictor of solution accuracy
- RL post-training (GRPO) does not improve the semantic correctness of reasoning traces and actively degrades trace validity while improving solution accuracy — trace fidelity and performance are orthogonal objectives under reward-only optimization
- Reasoning trace length does not correlate with the computational complexity of the underlying problem — generated trace lengths are largely agnostic to problem difficulty, undermining the 'inference-time scaling' interpretation of longer reasoning chains
- Safety monitoring of reasoning models via chain-of-thought inspection is empirically unreliable in controlled settings — conclusions about deception, deliberation, or 'aha moments' drawn from trace content are not warranted by the evidence
- Models that learn to mimic formal algorithm traces internalize stylistic patterns but fail to acquire the underlying algorithmic mechanisms — trace validity degrades sharply as problem difficulty increases, and the trace-solution correlation is an artifact of training distribution, not learned reaso
- Models trained on semantically correct traces catastrophically fail on out-of-distribution maze types (0% on Drunkard's Walk for Wilson-trained normal model), while models trained on irrelevant swapped traces generalize substantially better — semantic grounding in traces may cause overfitting to tra
- On hard out-of-distribution problems, models generate intermediate tokens up to the maximum context limit (32k tokens) without ever producing a valid solution — trace generation becomes unmoored from solution convergence
- Anthropomorphic interpretations of specific CoT tokens (e.g., 'aha' moments, deliberation patterns) have no empirical grounding — such interpretations are Rorschach projections onto ambiguous natural language outputs that lack formal ground truth
- The controlled findings (small 0.5B models, maze pathfinding domain with formal verifiability) may not generalize to frontier LLMs with natural language traces — the paper explicitly notes this gap and cannot check frontier models
- The proposed 'prompt augmentation' (PA = fθ(T, LLM)) framework explaining CoT effectiveness is speculative and lacks a principled method for learning or discovering optimal augmentations

## Bottlenecks

- No training methodology exists to simultaneously optimize solution accuracy and semantic validity of reasoning traces under RL — GRPO and similar reward-only methods treat trace content as irrelevant, making trace fidelity and performance improvement structurally orthogonal objectives
- The effectiveness of intermediate token sequences cannot be predicted from their semantic content or logical relationship to the problem — the mapping from task to effective prompt augmentation (the Skolem function PA = fθ(T, LLM)) is opaque, making principled CoT design impossible

## Breakthroughs

- Controlled experimental proof that intermediate token semantics are causally unnecessary for Chain-of-Thought performance gains — models trained on deliberately irrelevant reasoning traces (swapped from unrelated problems) achieve equivalent or superior accuracy, while GRPO post-training improves ac

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/latent_reasoning|latent_reasoning]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Key Concepts

- [[entities/chain-of-thought-cot|Chain of Thought (CoT)]]
- [[entities/group-relative-policy-optimization-grpo|Group Relative Policy Optimization (GRPO)]]
