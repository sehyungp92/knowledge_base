---
type: source
title: OpenPipe | RL For Agents
source_id: 01KKTEGC13B0Q6N3CEXCWKZKEC
source_type: article
authors: []
published_at: None
theme_ids:
- agent_evaluation
- agent_systems
- evaluation_and_benchmarks
- policy_optimization
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 18
tags: []
---
# OpenPipe | RL For Agents

**Authors:** 
**Published:** None
**Type:** article

## Analysis

# OpenPipe | RL For Agents
article
https://openpipe.ai/blog/ruler?refresh=1760739872913

---

## Briefing

**RULER (Relative Universal LLM-Elicited Rewards) eliminates the biggest bottleneck in RL agent training — the need for labeled data or hand-crafted reward functions — by using comparative LLM-as-judge scoring aligned with GRPO's within-group normalization. The result is a general-purpose reward signal that not only matches but frequently surpasses hand-crafted alternatives, democratizing RL fine-tuning for agentic tasks.**

### Key Takeaways
1. **No labeled data, no hand-crafted rewards** — RULER enables RL training with zero labeled golden data and zero human feedback by delegating reward design to an LLM judge.
2. **Beats frontier models at a fraction of the cost** — Small Qwen 2.5 models trained with GRPO+RULER outperform OpenAI o3 on all 4 tested agentic tasks despite being much cheaper to run.
3. **Beats hand-crafted reward functions** — RULER-trained models outperformed manually engineered GRPO reward functions on 3/4 tasks, including a 43-point gain on Customer Support Agent (50% → 93% vs. o3).
4. **Comparative scoring is the key insight** — Ranking N trajectories side-by-side is fundamentally easier for an LLM judge than scoring each in isolation, enabling better discrimination between good and bad agent behavior.
5. **GRPO's within-group normalization makes cross-group calibration irrelevant** — Because GRPO only uses relative within-group scores, the well-known miscalibration problem of isolated LLM scoring is completely bypassed.
6. **Clear system prompts beat custom rubrics** — Providing a detailed agent system prompt is more effective than writing a task-specific rubric, because RULER reads the system prompt as part of the trajectory to understand agent goals.
7. **Custom rubrics can hurt** — Tailoring the rubric to a task often leads to *worse* performance than the simple default rubric, suggesting over-specification harms the judge's judgment.
8. **Explainability is built in** — The judge generates brief reasoning explanations per score, enabling fault analysis and clustering of poorly-performing trajectories as a free byproduct.
9. **Test-time compute is an unexplored frontier** — The authors speculate RULER could be applied at runtime (not just training time) as a test-time compute signal to improve reliability, but this remains untested.
10. **Online learning for deployed agents is now conceivable** — RULER's label-free nature could allow agents to continuously self-improve during deployment, though this is future work.

---

### The Core Problem: Reward Engineering is the RL Bottleneck

- **Adapting RL to a new task has historically required either labeled golden data or highly task-specific success metrics**, both of which are expensive and hard to obtain.
  - This dependency makes every RL agent training pipeline unique and error-prone, creating a high barrier to entry for applying RL broadly across agentic tasks.
  - The result is that RL's power has been largely inaccessible outside of well-resourced labs with domain-specific engineering capacity.
- RULER's core proposition is that this bottleneck can be dissolved entirely by substituting LLM-based comparative judgment for human-designed reward signals.

---

### How RULER Works: The Mechanics

- **The training loop runs an agent N times per input set**, generating N trajectories each formatted as OpenAI-style chat completion messages (inputs + outputs).
- **Trajectory prefixes are deduplicated** before being passed to the judge — shared context (e.g., identical system messages) is extracted once, reducing redundant processing.
- **The LLM-as-judge receives the shared prefix plus N suffixes simultaneously** and scores each trajectory 0–1 based on a rubric, ranking them comparatively rather than absolutely.
- **RULER scores feed directly into GRPO as rewards**, completing a standard RL training step. This loop repeats for M iterations.
- **The judge also generates brief reasoning explanations per score** — these are not used in training but serve as interpretability artifacts for debugging and failure clustering.
- The configurable judge means any capable LLM can serve this role, making the system adaptable to different cost/quality tradeoffs.

---

### Why It Works: Two Structural Insights

- **Insight 1 — Comparative ranking exploits relative judgment strength.** An LLM presented with N trajectories side-by-side can identify subtle quality differences (e.g., unnecessary detours, incomplete goal achievement) far more reliably than when scoring each trajectory in isolation without context.
  - This is analogous to how human raters perform better in A/B comparisons than on absolute rating scales.
- **Insight 2 — GRPO makes cross-group calibration unnecessary.** GRPO normalizes rewards within each group using the group's mean and standard deviation, so absolute score values are irrelevant — only within-group relative ordering matters.
  - **This is a structural alignment between RULER's strength (relative ranking) and GRPO's requirement (relative rewards)**, making them a natural fit that sidesteps the classical LLM-judge calibration problem entirely.
  - Standard LLM-as-judge approaches in other contexts fail because isolated scores aren't well-calibrated across different prompts/sessions — RULER+GRPO doesn't require this property at all.

---

### Benchmark Performance: Empirical Validation

- RULER was tested on four realistic agentic tasks: ART-E, Reasoning Classifier, Voice Ordering, and Customer Support Agent.
- **Baseline Qwen 2.5 scores ranged from 41%–73%**, far below frontier model performance on all tasks.
- **GRPO+RULER brought Qwen 2.5 to 90%–96% across all tasks**, matching or exceeding OpenAI o3 (86%–95%) on every single task.
- **The Customer Support Agent result is particularly striking**: o3 scores only 50% (presumably due to prompt sensitivity or task structure), while RULER RL achieves 93% — 

## Key Claims

1. Developing task-specific reward functions for RL requires either labeled golden data or highly-task-dependent ways of measuring success, making each RL agent training pipeline unique, expensive and er
2. RULER is a general-purpose reward function that, when used with GRPO, can improve models with no labeled data, no hand-crafted reward functions, and no human feedback.
3. Models trained with GRPO+RULER outperform the best prompted frontier model on all 4 tested agentic tasks, despite being much smaller and cheaper to run.
4. RULER-trained models outperformed models trained with GRPO+hand-crafted reward functions on 3 out of 4 tasks.
5. On the ART-E task, Qwen 2.5 with RULER RL achieves 95% performance versus OpenAI o3's 90% and baseline Qwen 2.5's 41%.
6. On the Customer Support Agent task, Qwen 2.5 with RULER RL achieves 93% versus OpenAI o3's 50% and baseline Qwen 2.5's 62%.
7. On the Voice Ordering task, Qwen 2.5 with RULER RL achieves 96% versus OpenAI o3's 95% and baseline Qwen 2.5's 73%.
8. On the Reasoning Classifier task, Qwen 2.5 with RULER RL achieves 90% versus OpenAI o3's 86% and baseline Qwen 2.5's 60%.
9. RULER deduplicates trajectory prefixes before passing them to the LLM-as-judge to avoid redundant context processing.
10. RULER uses an LLM-as-judge that scores each trajectory between 0 and 1 based on a ranking rubric, and these scores are used directly as rewards in GRPO training.

## Capabilities

- General-purpose LLM-as-judge reward function (RULER) that trains RL agents using relative trajectory ranking with no labeled data, no hand-crafted reward functions, and no human feedback, while outperforming hand-crafted rewards on 3/4 tasks
- Small RULER-trained models (Qwen 2.5) outperform much larger frontier models (OpenAI o3) on all 4 evaluated agentic tasks at lower inference cost
- Relative within-group trajectory ranking sidesteps LLM-as-judge score calibration problems, enabling reliable GRPO reward signals from an otherwise poorly-calibrated judge

## Limitations

- RULER has only been tested as a training-time reward signal; its use as a runtime test-time compute mechanism for improving agent reliability remains unvalidated
- RULER does not yet support continuous online learning during deployment; agents cannot improve in real-time as they are used in production
- Adding task-specific rubric customization to RULER frequently degrades performance relative to the default generic rubric, suggesting reward specification remains brittle and expert intuition about what to measure can be counterproductive
- RULER's reward quality is entirely dependent on the capability of the configurable LLM-as-judge; a weak or misaligned judge produces degraded reward signal, with no independent verification mechanism
- RULER's evaluation scope is narrow — only 4 agentic tasks tested — leaving generalizability to broader task distributions, longer horizons, or more ambiguous goals undemonstrated
- RULER requires generating N full agent trajectories per training step for each input, multiplying inference cost compared to single-trajectory reward methods; at scale this represents a significant compute overhead
- Traditional RL reward function development for new tasks remains a blocking barrier when RULER is not applicable — requiring labeled golden data or highly task-dependent success measures

## Bottlenecks

- Constructing reliable reward signals for agentic RL without labeled data or hand-crafted functions blocks practical adoption of RL for new agent task domains

## Breakthroughs

- Relative within-group LLM trajectory ranking (RULER) enables reliable, general-purpose RL reward signals without labeled data, hand-crafted functions, or human feedback — and outperforms hand-crafted rewards on most tasks

## Themes

- [[themes/agent_evaluation|agent_evaluation]]
- [[themes/agent_systems|agent_systems]]
- [[themes/evaluation_and_benchmarks|evaluation_and_benchmarks]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Key Concepts

- [[entities/grpo|GRPO]]
- [[entities/test-time-compute|test-time compute]]
