---
type: source
title: 'Thinkless: LLM Learns When to Think'
source_id: 01KJTV54QV271XBPDQ3J5HPJ9E
source_type: paper
authors:
- Gongfan Fang
- Xinyin Ma
- Xinchao Wang
published_at: '2025-05-19 00:00:00'
theme_ids:
- chain_of_thought
- policy_optimization
- reasoning_and_planning
- reinforcement_learning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Thinkless: LLM Learns When to Think

**Authors:** Gongfan Fang, Xinyin Ma, Xinchao Wang
**Published:** 2025-05-19 00:00:00
**Type:** paper

## Analysis

# Thinkless: LLM Learns When to Think
2025-05-19 · paper · Gongfan Fang, Xinyin Ma, Xinchao Wang
https://arxiv.org/pdf/2505.13379

---

### Motivation & Prior Limitations
Applying extended chain-of-thought reasoning uniformly across all queries is computationally wasteful, since many problems admit straightforward solutions that do not benefit from elaborate inference chains, leading to redundant token generation, increased memory footprint, and substantially higher latency.
- Prior hybrid reasoning approaches — such as prompt-level "reasoning on/off" switches and fixed computational budget heuristics — relied on manually designed control signals rather than learned policies, producing suboptimal routing decisions that cannot account for the target model's own capability.
  - Router-based approaches use a separate LLM to assess query difficulty, but this external classifier lacks awareness of the target reasoning model's actual confidence; on AIME 2024, where the reasoning model achieves only 28% accuracy, router models fail to recognise the difficulty.
  - Techniques like CoT-Valve (LoRA-based controllable chain length) and model merging (parameter interpolation) expose a calibration-transfer problem: an optimal reasoning-length setting found on one benchmark (e.g., merging ratio 0.6 on Minerva Algebra) causes unexpected accuracy degradation on harder benchmarks like AIME.
- Vanilla GRPO, when applied naively to hybrid reasoning, causes mode collapse within ~120 training steps because its length-normalised gradient disproportionately suppresses the single control token relative to the hundreds-to-thousands of response tokens, causing the model to fixate on one mode entirely.
  - Two compounding imbalances: (1) mode-accuracy imbalance — one control token vs. Ti response tokens; (2) think-short imbalance — longer think sequences further dilute the `<think>` token gradient via the 1/(Ti+1) normalisation factor.

---

### Proposed Approach
Thinkless is a two-stage reinforcement learning framework that trains a single LLM to autonomously select between short-form (`<short>`) and long-form (`<think>`) reasoning by emitting a control token as the very first output token, with the selection policy jointly conditioned on input complexity and the model's own capability.
- **Stage 1 — Distillation warm-up:** A paired synthetic dataset is constructed by generating both chain-of-thought responses (from DeepSeek-R1-671B) and concise responses (from Qwen2.5-Math-1.5B-Instruct) for each prompt; the base model (DeepSeek-R1-Distill-Qwen-1.5B) is then fine-tuned via SFT to follow either control token, ensuring both modes are reachable before RL begins.
  - Paired construction is essential to ensure balanced mode distribution at the start of RL, preventing the policy from starting in a collapsed state.
- **Stage 2 — Decoupled GRPO (DeGRPO):** The RL objective is explicitly split into two independently normalised components — a control-token loss (Li,0) weighted by a scalar α, and a response-accuracy loss (average over remaining tokens) — breaking the dependence between gradient scale and sequence length.
  - The reward function assigns +1.0 for correct short responses, +(1.0−γ) for correct long responses (with 0<γ<1 encoding preference for brevity), and −1.0 for incorrect responses of either type, giving the policy a clean signal to prefer short when accuracy is preserved.
  - α is set to 1/1000 in experiments; a higher α accelerates mode-selection learning but risks premature commitment to long-form reasoning before short-form accuracy has had time to improve, effectively degrading the policy to a static binary classifier.
  - Advantage normalisation uses mean-centred (not std-normalised) relative rewards, motivated by the observation that varying question difficulty introduces bias under standard normalisation.

---

### Results & Capabilities
Thinkless reduces long-form reasoning usage by 50%–90% across standard math benchmarks while maintaining accuracy within ~1% of the full-thinking baseline, and naturally retains near-100% think-mode usage on the hardest problems.
- On Minerva Algebra, Thinkless routes only 25.88% of queries to think mode, reducing average token count from 3,029 to 1,144 (roughly one-third), while holding Pass@1 at 0.9459 vs. 0.9577 for the full reasoning baseline — a gap of ~1.2%.
- On GSM8K (elementary arithmetic), the model uses think mode for only 13.31% of queries, generating 624 tokens on average vs. 1,919 for the pure reasoning model, while achieving 0.8418 Pass@1 — competitive with and in some cases exceeding pure short-form models (QMath-1.5B: 0.8572, but with no adaptive routing).
- On AIME 2024 (hardest benchmark), Thinkless uses think mode for 100% of queries and achieves 0.2733 Pass@1, matching DeepSeek-R1-1.5B (0.2800) closely, confirming that the learned policy correctly identifies when short reasoning would be insufficient.
- Compared to router-based baselines (Router Q-7B), Thinkless is superior in adaptive calibration: Router Q-7B selects think mode for only 2.35% of GSM8K queries and achieves 0.8587 Pass@1, but for AIME it routes only 46.67% to think mode and underperforms (0.1667 vs. 0.2733), indicating it cannot account for the target model's own capability.
- A characteristic U-shaped training curve is observed: early in RL, think-mode usage rises (because long chains yield higher initial accuracy); as short-form accuracy improves through both RL quality gains and better query-to-mode assignment, short-mode usage rises and long-mode average accuracy drops — not due to capability degradation but because harder queries monopolise the think mode.
- DeGRPO also compresses the length of long-chain responses as a secondary effect, since the reward structure rewards short correct answers, creating a gradient toward more compact reasoning even within the think branch.

---

### Implications
The paper establishes that reasoning-mode selection can be learned end-to-end v

## Key Claims

1. Applying elaborate chain-of-thought reasoning uniformly to all queries results in redundant token generation, increased memory footprint, and substantially higher computational cost.
2. Vanilla GRPO, when applied to hybrid reasoning, causes mode collapse because the single control token receives weak and biased gradient signals due to normalization by total response length.
3. In vanilla GRPO, the number of generated long-chain responses drops below 10 within just 120 update steps, preventing the model from learning a correct hybrid policy.
4. DeGRPO decomposes the hybrid reasoning objective into two components: a control token loss governing mode selection and a response loss improving answer accuracy.
5. Thinkless reduces the usage of long-form reasoning by 50%–90% on benchmarks such as Minerva Algebra, MATH-500, and GSM8K.
6. On the Minerva Algebra dataset, Thinkless activates the reasoning mode for only 25% of samples, reducing token usage to one-third of the original while maintaining performance within a 1% margin.
7. On challenging tasks like AIME, Thinkless naturally adopts a higher proportion of long-form reasoning, demonstrating capability-aware mode selection.
8. Reasoning models generate 5 to 20 times more tokens than standard instruction-following models.
9. On simpler datasets like GSM8K, extended reasoning offers no clear advantage over standard instruction-following models.
10. DeGRPO training produces a U-shaped learning curve where the proportion of long-chain outputs first increases then gradually decreases as short-chain accuracy improves.

## Capabilities

- LLMs can be trained via RL to autonomously select between short-form and long-form reasoning based on task complexity and model capability, reducing long-chain thinking by 50–90% on math benchmarks without significant accuracy loss
- DeGRPO (Decoupled Group Relative Policy Optimization) enables stable RL training of hybrid reasoning by independently normalizing control token and response token gradients, preventing mode collapse in hybrid reasoning training
- A hybrid reasoning model (1.5B) can activate thinking mode for only 25% of queries while maintaining within-1% accuracy margin on appropriate benchmarks, reducing token usage to one-third of the original reasoning model
- Hybrid reasoning models produce smooth, well-calibrated probability distributions over reasoning mode selection — correctly assigning near-zero thinking probability to straightforward arithmetic and near-1.0 to multi-concept problems requiring logical inference

## Limitations

- Reasoning models generate 5–20x more tokens than standard non-reasoning models for all queries regardless of difficulty, creating substantial compute waste on simple tasks that admit direct answers
- Vanilla GRPO causes mode collapse in hybrid reasoning training: length normalization systematically under-weights the control token gradient, causing the model to converge entirely to one reasoning mode within ~120 training steps
- Hybrid reasoning training and evaluation only validated on math benchmarks (AIME, MATH-500, GSM8K, Minerva Algebra) — applicability to code, science, medical, or open-ended domains is entirely undemonstrated
- Thinkless is only trained and tested on a 1.5B parameter model — scalability of DeGRPO and the hybrid mode-selection framework to larger frontier models is not established and may face different collapse dynamics
- Hybrid reasoning efficiency gains completely vanish on the hardest tasks — Thinkless uses 100% thinking mode on AIME with no token savings, providing essentially no benefit over pure reasoning mode on frontier-difficulty problems
- External router-based hybrid reasoning approaches fail at the capability frontier — routers trained independently cannot estimate how difficult a task is relative to the specific target model's competence, causing systematic misrouting on the hardest problems
- Fixed heuristics for hybrid reasoning mode selection (interpolation ratios, prompt-level on/off toggles) transfer poorly across datasets — a coefficient tuned on one benchmark causes unexpected accuracy degradation on others
- SFT warm-up distillation introduces accuracy degradation that propagates into downstream RL — the hybrid model begins RL training from a weaker baseline than the original reasoning model due to catastrophic forgetting during multi-style fine-tuning
- SFT dataset scaling shows rapidly diminishing returns for hybrid warm-up: a 10x scale increase from 114K to 1M examples yields only ~1% accuracy gain, suggesting data quality and diversity matter far more than volume
- Aggressive control token weighting (high α) in DeGRPO causes premature mode lock-in — the model assigns queries to long-chain mode based on initial low short-mode accuracy before RL can improve it, degenerating to a static difficulty classifier rather than an adaptive policy

## Bottlenecks

- No principled, model-capability-aware mechanism for routing LLM inference between reasoning depths blocks efficient deployment of reasoning models — existing approaches rely on suboptimal dataset-specific heuristics or external routers blind to the target model's competence profile
- Math-domain constraint on hybrid reasoning RL training data blocks generalization of learned mode selection to task types lacking easily verifiable reward signals

## Breakthroughs

- Decoupled Group Relative Policy Optimization (DeGRPO) solves the mode collapse problem in hybrid reasoning RL training by independently normalizing control-token and response-token gradients, enabling stable end-to-end learning of when to think

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/deepseek-r1-distill-qwen-15b|DeepSeek-R1-Distill-Qwen-1.5B]]
- [[entities/gsm8k|GSM8K]]
