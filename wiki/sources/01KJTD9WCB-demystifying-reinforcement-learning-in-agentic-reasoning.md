---
type: source
title: Demystifying Reinforcement Learning in Agentic Reasoning
source_id: 01KJTD9WCB2YJZKQN6CMFR7VZS
source_type: paper
authors:
- Zhaochen Yu
- Ling Yang
- Jiaru Zou
- Shuicheng Yan
- Mengdi Wang
published_at: '2025-10-13 00:00:00'
theme_ids:
- agent_systems
- policy_optimization
- reinforcement_learning
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- tool_use_and_agent_protocols
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Demystifying Reinforcement Learning in Agentic Reasoning

**Authors:** Zhaochen Yu, Ling Yang, Jiaru Zou, Shuicheng Yan, Mengdi Wang
**Published:** 2025-10-13 00:00:00
**Type:** paper

## Analysis

# Demystifying Reinforcement Learning in Agentic Reasoning
2025-10-13 · paper · Zhaochen Yu, Ling Yang, Jiaru Zou, Shuicheng Yan, Mengdi Wang
https://arxiv.org/pdf/2510.11701

---

### Motivation & Prior Limitations
- Directly applying GRPO-based policy optimization to agentic LLM training produces suboptimal and unstable results, yet the key design choices that cause or prevent this remain poorly understood.
  - Observed failure modes include inefficient on-policy rollout sampling, reward and entropy collapse, and unstable training dynamics when naïve GRPO is applied to multi-turn tool-use settings.
- Existing agentic SFT data pipelines rely on stitch-style synthesis — manually replacing reasoning steps with tool outputs — which fails to capture the natural decision structure of real tool-use trajectories.
  - Stitched data cannot encode when or why to invoke a tool, nor does it represent pre-call analysis, guarded execution, error recovery, or self-reflection behaviors observed in genuine multi-turn interactions.
- The optimal RLVR recipe for agentic training is unclear: methods disagree on optimization granularity (token vs. sequence level), clipping strategy, and KL regularization, and no principled account existed for when to apply each.
- The allocation of reasoning budget between internal inference tokens and external tool calls — and how this interacts with agent performance — was uncharacterized, leaving open whether "overthinking" (long loops) or "undertinking" (premature tool reliance) is the dominant failure mode.

---

### Proposed Approach
- The paper conducts a systematic empirical investigation across three axes — data curation, GRPO algorithm design, and reasoning mode — to extract actionable principles for agentic RL, and releases datasets, cold-start models, and a strong 4B baseline (DemyAgent-4B).
- On the data axis, the authors curate a 3k real end-to-end agentic SFT dataset (capturing pre-call analysis, guarded execution, error recovery, and self-reflection) and a 30k high-diversity RL dataset, replacing synthetic stitch-style trajectories.
  - For models where base capability is too weak relative to dataset difficulty (competence–difficulty mismatch), a model-aware dataset is constructed by filtering problems to those in a learnable difficulty range (0% < accuracy < 100%), using 8 rollouts per problem as a proxy for per-model difficulty.
- On the algorithm axis, three GRPO recipes are compared: GRPO-T (baseline token-level, standard clip), GRPO-TCR (token-level loss + clip higher + overlong reward shaping), and GRPO-SCR (sequence-level loss + clip higher + overlong reward shaping).
  - Overlong reward shaping applies zero penalty within a safe length budget, a linear penalty between `Lmax − Lcache` and `Lmax`, and −1 beyond `Lmax`, preserving learning signal near the boundary while discouraging verbosity.
  - Asymmetric clipping (higher `ϵhigh` than `ϵlow`) is used to expand exploration budget without destabilizing the lower bound, and token-level loss is preferred over sequence-level to leverage each token's contribution equally.
- On the reasoning mode axis, the authors characterize two regimes — Reactive Mode (short-think, frequent tool calls) and Deliberative Mode (deliberate-think, fewer tool calls) — and measure tool-call success rate as a proxy for reasoning quality, linking mode to overall performance.
  - Long-CoT models (e.g., Qwen3-4B-Thinking-2507) are tested directly in agentic RL and found to avoid tool calls on reasoning-intensive tasks; SFT initialization on real multi-turn trajectories is proposed as a remediation strategy.

---

### Results & Capabilities
- Real end-to-end trajectories dramatically outperform synthetic stitch-style data for SFT cold-start: Qwen3-4B-Instruct-2507 trained on real data achieves 29.79% average@32, 72.88% pass@32, and 45.82% maj@32 on AIME2025, versus below 10% average@32 with unstable performance for the synthetic baseline.
  - Improvements of +28.85% average@32 and +50.66% pass@32 on AIME2025 were observed for Qwen3-4B-Instruct-2507, with similarly large gains on AIME2024.
- Diverse RL datasets sustain higher policy entropy throughout training and improve convergence speed: with the diverse dataset, the agent surpasses 50% average@32 on AIME2025 within 150 steps, compared to 220 steps required by the math-only DAPO-Math-17k baseline.
- GRPO-TCR achieves 70.93%/68.13% average@32 on AIME2024/AIME2025 for Qwen3-4B-RA-SFT within 450 steps; GRPO-T reaches only 54.7%/40.93% as its best, and GRPO-TCR matches GRPO-T's best performance using only 25% of training computation.
- Increasing clip upper bound `ϵhigh` from 0.28 to 0.315 for GRPO-TCR delivers equivalent performance 40% faster (reaching at step 60 what otherwise requires step 100), but further increasing to 0.35 degrades convergence for Qwen3-4B-RA-SFT, revealing a non-monotonic optimum.
- Deliberative Mode agents (higher response length per round, fewer tool calls) achieve over 70% tool-call success rate, versus substantially lower rates for Reactive Mode agents, directly explaining the performance gap.
- DemyAgent-4B (4B parameters) matches or outperforms models up to 32B across benchmarks: AIME2024 72.6%, AIME2025 70.0%, GPQA-Diamond 58.5%, LiveCodeBench-v6 26.8%, surpassing ReTool-32B (72.5%/54.3% on AIME2024/2025) and rStar2-Agent-14B (80.6%/69.8% — DemyAgent-4B is competitive on AIME2024, surpasses on AIME2025), and outperforming DeepSeek-R1-Zero (671B) on AIME2025.
- In agentic RL with exploration-friendly algorithms (GRPO-TCR, GRPO-SCR), both pass@k and average@k improve simultaneously — a qualitative departure from conventional RL, where RL training typically suppresses pass@k while improving pass@1. The conservative GRPO-T baseline still exhibits the classical trade-off.
- Long-CoT models initialized with SFT on real multi-turn trajectories acquire tool-invocation priors and improve over uninitialzed Long-CoT, but ultimately achieve only comparable (not sup

## Key Claims

1. Real end-to-end tool-use trajectories for SFT initialization dramatically outperform synthetic stitch-style trajectories, with Qwen3-4B trained on real data achieving 29.79% average@32 on AIME2025 ver
2. Synthetic stitch-style data synthesis misses critical decision cues about when and why tools should be invoked, preventing agents from learning optimal tool integration.
3. High-diversity RL datasets sustain higher policy entropy throughout training and yield faster learning, reaching 50% accuracy on AIME2025 in 150 steps versus 220 steps for a math-only dataset.
4. Dataset diversity directly drives richer exploration by maintaining higher policy entropy, preventing premature collapse to narrow deterministic strategies.
5. A competence-difficulty mismatch occurs when the base policy is too weak relative to the training dataset, causing reward stagnation around zero and failure to extract meaningful gradients.
6. Model-aware datasets tailored to a model's current difficulty level provide stronger gradient signals and overcome performance bottlenecks for weaker models in RL training.
7. GRPO-TCR (clip higher + overlong reward shaping + token-level loss) achieves 70.93%/68.13% average@32 on AIME2024/AIME2025 versus GRPO-T's best of 54.7%/40.93%, using only 25% of the training compute.
8. Token-level loss outperforms sequence-level loss for models with strong initial exploration ability, exceeding it by 3.95% on AIME2024 and 3.86% on AIME2025 under the same training budget.
9. Token-level loss and sequence-level loss achieve comparable performance for weaker models with limited initial exploration ability.
10. Agentic RL with exploration-friendly recipes can jointly improve both pass@k and average@k simultaneously, unlike conventional RL which trades exploration for exploitation.

## Capabilities

- Agentic RL with exploration-friendly GRPO variants (clip higher + overlong reward shaping) can simultaneously improve both pass@k (exploration ceiling) and average@k (exploitation reliability), breaking the conventional RL trade-off where RL improves exploitation at the expense of exploration
- 4B-parameter models trained with optimal agentic RL recipes (real trajectories + diverse model-aware datasets + GRPO-TCR) match or outperform 32B models on challenging reasoning benchmarks including AIME 2024/2025 and GPQA-Diamond
- Deliberative-mode agentic RL agents that invest more inference tokens in internal reasoning before tool calls achieve over 70% tool-use success rates, dramatically outperforming reactive agents that rely on frequent but shallow tool calls
- Model-aware RL dataset construction — filtering problems by per-model empirical difficulty and discarding problems with 0% or 100% accuracy — overcomes competence-difficulty mismatch and enables effective RL training for weaker models that would otherwise stagnate at zero reward
- Real end-to-end multi-turn tool-use trajectories as SFT initialization for agentic RL produce dramatically stronger cold-start baselines than synthetic stitch-style data, with improvements of up to 51.63% absolute on maj@32 metrics for Qwen3-4B on AIME 2024
- High-diversity RL training datasets sustain policy entropy at elevated levels throughout training, yielding faster convergence (33% fewer training steps to reach the same accuracy threshold) and more stable agentic RL compared to narrow math-only datasets

## Limitations

- Open-source Long-CoT models optimized for reasoning tasks avoid invoking tools when facing reasoning-intensive problems, instead relying exclusively on internal reasoning — tool-call count converges to zero during agentic RL training on reasoning tasks
- Long-CoT models with SFT agentic initialization achieve only comparable — not superior — performance to instruction-based models in agentic RL, because conflicting optimization objectives fragment learning efficiency
- Synthetic stitch-style agentic trajectories fail to teach models when and why to invoke tools — they miss pre-call analysis, guarded execution, error recovery, and self-reflection, producing unreliable tool-invocation signals and weak RL initialization
- Agentic RL training insights are validated only on 4B and 7B models; hyperparameter sensitivities for larger models are unknown and likely different, limiting the generalizability of reported recipes to production-scale models
- Standard conservative GRPO (restrictive clip upper bound + strong KL regularization) causes early entropy collapse in agentic RL, forcing models to maintain self-contained generation patterns and preventing leverage of tool-call feedback
- Collecting real end-to-end agentic SFT trajectories is computationally costly, creating a data bottleneck that constrains the scale and quality of agentic cold-start initialization — the qualitatively superior data type is not easily scalable
- The gap between pass@k and average@k creates an intrinsic ceiling on RL training efficiency — the amount of average@k improvement achievable from RL is bounded by the existing pass@k ceiling, not by algorithm quality
- Reactive-mode agents using frequent tool calls with minimal internal reasoning exhibit substantially lower tool-use success rates, indicating a performance cliff where call frequency inversely correlates with per-call quality
- Entropy has a non-monotonic relationship with agentic RL performance: above a model-specific threshold, excessive entropy destabilizes training and reduces peak accuracy, making entropy management a brittle and model-dependent hyperparameter
- Competence-difficulty mismatch: when a base policy is too weak relative to RL dataset difficulty, reward stagnates near zero and gradient signals collapse entirely — training failure is silent and requires model-aware data filtering to detect and resolve
- Current agentic RL research is conducted in static single-tool environments (code interpreter only), leaving multi-tool coordination, dynamic tool selection, and real-world heterogeneous tool environments entirely unexplored
- Optimal RL hyperparameters (clip bounds, entropy targets) are model-capability-dependent — weaker models require larger clip upper bounds, stronger models require tighter bounds — meaning there is no universal agentic RL recipe

## Bottlenecks

- Computational cost of real end-to-end agentic trajectory collection creates a data scarcity bottleneck for agentic SFT initialization — synthetic alternatives are qualitatively inferior by large margins, but real trajectory pipelines do not scale
- Long-CoT models' deeply embedded internal reasoning priors create conflicting optimization objectives in agentic RL, preventing them from achieving superior performance despite stronger base capabilities — limits the ability to use SOTA reasoning models as agentic RL starting points
- The pass@k ceiling determines an intrinsic bound on average@k improvement from RL — when the ability boundary is saturated, RL training efficiency collapses regardless of algorithm quality, blocking further reliable performance improvements
- Absence of agent-specific reasoning frameworks that prioritize high-level tool-planning over internal reasoning blocks effective inference scaling for complex agentic tasks — current models either over-reason internally or over-rely on tools with no principled middle ground

## Breakthroughs

- Exploration-friendly agentic RL (GRPO-TCR with clip higher + overlong reward shaping) breaks the conventional RL exploration-exploitation trade-off, achieving simultaneous >10% improvement on both pass@k and average@k on hard math benchmarks by leveraging external tool feedback to expand cognitive c
- Real end-to-end tool-use trajectories versus synthetic stitch-style data show a qualitative performance gap of up to 51.63% absolute improvement on majority-vote metrics, establishing trajectory authenticity — not data scale — as the primary determinant of agentic SFT quality

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/rl_theory_and_dynamics|rl_theory_and_dynamics]]
- [[themes/tool_use_and_agent_protocols|tool_use_and_agent_protocols]]

## Key Concepts

- [[entities/grpo|GRPO]]
- [[entities/passk|pass@k]]
- [[entities/policy-entropy|policy entropy]]
