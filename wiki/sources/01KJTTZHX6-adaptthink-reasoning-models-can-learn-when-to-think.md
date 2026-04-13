---
type: source
title: 'AdaptThink: Reasoning Models Can Learn When to Think'
source_id: 01KJTTZHX6Q3CQ1X1W40MFZ7QS
source_type: paper
authors:
- Jiajie Zhang
- Nianyi Lin
- Lei Hou
- Ling Feng
- Juanzi Li
published_at: '2025-05-19 00:00:00'
theme_ids:
- chain_of_thought
- policy_optimization
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# AdaptThink: Reasoning Models Can Learn When to Think

**Authors:** Jiajie Zhang, Nianyi Lin, Lei Hou, Ling Feng, Juanzi Li
**Published:** 2025-05-19 00:00:00
**Type:** paper

## Analysis

# AdaptThink: Reasoning Models Can Learn When to Think
2025-05-19 · paper · Jiajie Zhang, Nianyi Lin, Lei Hou, Ling Feng, Juanzi Li
https://arxiv.org/pdf/2505.13417

---

### Motivation & Prior Limitations
Large reasoning models (LRMs) like OpenAI o1 and DeepSeek-R1 apply long chain-of-thought thinking uniformly to all problems regardless of difficulty, creating substantial inference overhead and latency even for simple queries where thinking yields no benefit.
- Prior efficiency methods (length-reward RL, preference finetuning with shorter responses, model merging) all reduce the length of the thinking process but still force models into Thinking mode for every problem, never questioning whether thinking is warranted at all.
  - Methods such as TLMRE, DAST, DPOShortest, and O1-Pruner achieve at most 17–42% average response length reduction on math benchmarks while sometimes degrading accuracy.
- A pilot study on MATH500 with DeepSeek-R1-Distill-Qwen-7B shows that NoThinking (skipping the think segment entirely) matches or exceeds Thinking accuracy on Levels 1–3 problems while using 5–8× fewer tokens; Thinking only provides meaningful benefit at Levels 4–5, yet models spend the same compute budget regardless.
  - At Level 1, NoThinking actually outperforms Thinking (94.9% vs. 91.7%) with ~85% fewer tokens, and even at Level 4, Thinking only improves the instance-level pass rate for 49% of problems.

---

### Proposed Approach
AdaptThink is a reinforcement learning algorithm that trains reasoning models to autonomously select between Thinking mode (full chain-of-thought) and NoThinking mode (empty `<think></think>` segment, directly generating the final solution) based on problem difficulty at inference time.

- The core objective is a constrained optimization that maximizes the probability of choosing NoThinking while enforcing that overall accuracy does not fall below the reference model's performance, formulated as a PPO-style loss where the advantage function is `A(x,y) = 1(y₁=</think>)·δ + R(x,y) − R̄_ref(x)`.
  - The scalar δ acts as a tunable bias rewarding NoThinking; the algorithm only promotes NoThinking for a given problem when `R̄_nothink(x) + δ > R̄_ref(x)` and `R̄_nothink(x) + δ > R̄_think(x)`, meaning it naturally routes hard problems to Thinking.
  - This differs from all prior work by treating the binary choice of whether to think as a learnable policy decision rather than optimizing within Thinking mode.
- An importance sampling strategy overcomes the cold-start problem: since the initial model has near-zero probability of generating NoThinking responses, training is bootstrapped by a modified distribution `π_IS` that forces exactly 50% Thinking and 50% NoThinking samples per batch, with importance-sampling correction applied to the PPO ratio.
  - This also prevents mode collapse (the model fixating entirely on one mode) throughout training by ensuring both modes receive gradient signal at every step.
- NoThinking is simplified relative to Ma et al. (2025) by using a fully empty thinking segment (`<think></think>`) rather than a fake thinking phrase, making the mode boundary crisper.

---

### Results & Capabilities
AdaptThink is the only method evaluated that simultaneously reduces inference cost and improves accuracy across both model scales, achieving a 53% average response length reduction and +2.4% accuracy improvement on DeepSeek-R1-Distill-Qwen-1.5B, and 40.1% length reduction with +2.3% accuracy on the 7B model.
- On GSM8K/MATH500/AIME2024 for the 1.5B model: length reductions are 50.9%, 63.5%, and 44.7% respectively; accuracy gains are +4.1%, +1.4%, +1.6% — all versus the original Thinking baseline.
  - Every competing method either fails to improve accuracy (DAST: −0.6%, O1-Pruner: −1.0%, ModelMerging: −9.4%) or achieves far smaller length reductions (TLMRE achieves +2.0% accuracy but only −25.3% length).
- AdaptThink learns a difficulty-calibrated routing policy: on MATH500, the 7B model selects NoThinking for 97.7% of Level-1 problems and only 2.3% of Level-5 problems, producing accuracy above both pure-Thinking and pure-NoThinking baselines at nearly every difficulty level.
- The approach generalizes out-of-distribution: on MMLU (14K multi-choice questions, 57 domains), AdaptThink-1.5B achieves +6.5% accuracy over original Thinking while reducing length by 38.8%, using NoThinking for ~16% of problems without any MMLU-specific training.
- Implicit thinking (reasoning keywords appearing inside NoThinking responses) remains low: RatioIT is 7.9% for 1.5B and 4.2% for 7B in NoThinking-selected cases, comparable to the original model's NoThinking baseline, indicating RL does not smuggle reasoning back through the no-think path at meaningful scale.

---

### Implications
AdaptThink establishes difficulty-adaptive thinking-mode selection as a new efficiency paradigm for LRMs, orthogonal and complementary to all prior token-length-reduction approaches — those methods could in principle be combined with AdaptThink's routing to further improve the Thinking branch.
- The result that NoThinking can outperform Thinking on simple tasks (even when the model was trained exclusively on long-thinking data) challenges the implicit assumption that more compute always helps reasoning models, suggesting the field may be systematically over-provisioning test-time compute for a large fraction of real-world queries.
- The δ hyperparameter provides a single, interpretable dial for operators to trade off accuracy against inference cost, which is practically valuable for deployment scenarios with latency or cost constraints.
- The constrained-optimization framing (maximize efficiency subject to accuracy floor) offers a reusable template for other compute-allocation problems in inference, such as adaptive depth, speculative decoding gating, or layer-skipping policies.
- The cold-start importance sampling technique addresses a general challenge in on-policy RL whenever the initial policy 

## Key Claims

1. Large reasoning models like OpenAI o1 and DeepSeek-R1 employ long chain-of-thought across all problems, which substantially increases inference overhead and latency.
2. NoThinking achieves comparable or better performance than Thinking on relatively simple problems (up to high-school competition level) while significantly reducing token usage.
3. Thinking only improves the instance-level pass rate for less than half of problems across MATH500 difficulty Levels 1–4 compared to NoThinking.
4. AdaptThink is a novel RL algorithm that teaches reasoning models to adaptively select between Thinking and NoThinking mode based on problem difficulty.
5. AdaptThink uses a constrained optimization objective that maximizes the probability of NoThinking responses while ensuring overall accuracy does not degrade below the reference model's level.
6. Without importance sampling, naive GRPO cannot generate NoThinking samples from the start of training because the initial policy model assigns near-zero probability to NoThinking responses.
7. AdaptThink reduces the average response length of DeepSeek-R1-Distill-Qwen-1.5B by 53% and improves its accuracy by 2.4% across GSM8K, MATH500, and AIME2024.
8. AdaptThink reduces response length on GSM8K, MATH500, and AIME2024 for the 1.5B model by 50.9%, 63.5%, and 44.7% respectively, while improving accuracy by 4.1%, 1.4%, and 1.6%.
9. AdaptThink produces 86.9% NoThinking responses on GSM8K and 76.8% on MATH500 for the 1.5B model, but only 40.4% on the harder AIME2024.
10. AdaptThink outperforms all baseline methods (DPOShortest, OverThink, DAST, O1-Pruner, TLMRE, ModelMerging, RFTMixThinking) in average accuracy while achieving greater length reduction for the 1.5B mod

## Capabilities

- RL-trained adaptive thinking mode selection (AdaptThink) enables reasoning models to learn when to skip chain-of-thought entirely based on problem difficulty, reducing inference token usage by 40–53% while simultaneously improving accuracy by 2.3–2.4% on math benchmarks compared to always-Thinking b
- Prompting reasoning models with an empty thinking segment (<think></think>) achieves comparable or better accuracy than full chain-of-thought for problems up to high-school competition level, using 82–88% fewer tokens — NoThinking even slightly outperforms Thinking on easiest problems
- Importance sampling forcing 50/50 Thinking/NoThinking distribution during on-policy RL training solves the cold-start problem of mode selection, enabling training for adaptive thinking from step one without collapsing to a single mode

## Limitations

- NoThinking mode suffers a severe performance cliff on olympiad-level problems — accuracy collapses from 53.5% (Thinking) to 24.2% (NoThinking) for the 7B model on AIME 2024, a ~55% relative drop, making it unusable for frontier mathematical reasoning
- AdaptThink has only been validated on 1.5B and 7B parameter models due to compute constraints — scaling behaviour at frontier scale (70B+) is entirely unknown
- AdaptThink training is gated behind verifiable rewards — only mathematical problem-solving is validated, blocking application to open-ended tasks like writing, analysis, or code review without automated verification infrastructure
- OOD generalization benefit for larger models is marginal — the 7B model improves only 0.2% on MMLU (63.4% → 63.6%) despite adaptive mode selection, with only 16% NoThinking usage on OOD tasks vs 87–99% on in-distribution easy sets
- AdaptThink training carries substantial compute cost — the 1.5B model requires one 8×H800 node for 32 hours; the 7B model requires four 8×H800 nodes for 28 hours — limiting accessibility and iteration speed
- The δ hyperparameter controlling the efficiency-accuracy tradeoff is sensitive — at δ=0.1, AdaptThink-1.5B accuracy on AIME 2024 falls below baseline (26.7% vs 29.4%), indicating a failure mode from over-aggressive NoThinking selection
- RL training for AdaptThink can leak implicit thinking behaviour into NoThinking responses — the 7B model shows 4.2% implicit thinking ratio (vs 0.9% baseline), with outputs 25% longer than original NoThinking, indicating the Thinking/NoThinking boundary is not crisp
- AdaptThink provides negligible inference savings on hard olympiad-level problems — only 6.3% NoThinking ratio on AIME 2024 for the 7B model, meaning the approach is mostly effective for easy-to-medium difficulty workloads
- Standard on-policy RL (GRPO) without importance sampling entirely fails to produce NoThinking behaviour — response length only decreases to ~3500 tokens via truncation effects rather than the target ~1875 tokens, revealing a hard cold-start barrier for low-probability target behaviours
- All prior efficient reasoning methods (DPO, RL length penalties, model merging) still apply Thinking to every problem regardless of difficulty — no existing method before AdaptThink routes easy problems away from chain-of-thought, leaving a systematic inefficiency across the entire reasoning-model d

## Bottlenecks

- Reasoning models universally apply long chain-of-thought to all queries regardless of difficulty, creating unnecessary inference overhead for simple problems — no model-level mechanism exists to calibrate compute expenditure to actual task complexity at inference time
- Absence of verifiable reward signals for general domains gates difficulty-adaptive RL training to math-only settings — models trained with AdaptThink cannot learn optimal thinking-mode calibration for coding, writing, analysis, or science without automated domain verifiers

## Breakthroughs

- First demonstration that RL can train reasoning models to adaptively select whether to use chain-of-thought at all — breaking the assumed efficiency-accuracy tradeoff by simultaneously reducing inference cost (40–53%) and improving accuracy (2.3–2.4%) versus always-Thinking baselines

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/deepseek-r1-distill-qwen-15b|DeepSeek-R1-Distill-Qwen-1.5B]]
- [[entities/deepseek-r1-distill-qwen-7b|DeepSeek-R1-Distill-Qwen-7B]]
- [[entities/grpo-group-relative-policy-optimization|GRPO (Group Relative Policy Optimization)]]
- [[entities/gsm8k|GSM8K]]
- [[entities/math500|MATH500]]
- [[entities/mmlu|MMLU]]
- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
- [[entities/thinking-mode|Thinking Mode]]
- [[entities/verl|verl]]
