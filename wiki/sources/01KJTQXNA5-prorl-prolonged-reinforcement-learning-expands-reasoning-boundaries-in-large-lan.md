---
type: source
title: 'ProRL: Prolonged Reinforcement Learning Expands Reasoning Boundaries in Large
  Language Models'
source_id: 01KJTQXNA5QQQPTXXWJTJ2RBM0
source_type: paper
authors:
- Mingjie Liu
- Shizhe Diao
- Ximing Lu
- Jian Hu
- Xin Dong
- Yejin Choi
- Jan Kautz
- Yi Dong
published_at: '2025-05-30 00:00:00'
theme_ids:
- policy_optimization
- reasoning_and_planning
- reinforcement_learning
- rl_for_llm_reasoning
- rl_theory_and_dynamics
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# ProRL: Prolonged Reinforcement Learning Expands Reasoning Boundaries in Large Language Models

ProRL is a training methodology and empirical study that directly challenges the prevailing consensus that reinforcement learning merely redistributes probability mass over solutions already present in a base model's distribution. By extending RL training beyond 2,000 steps with entropy-stabilization techniques, the authors demonstrate that LLMs can acquire genuinely novel reasoning strategies — including solving tasks where the base model achieves 0% pass rate under unlimited sampling — and that training-time RL compute follows a scaling law analogous to inference-time scaling in O1-style models.

**Authors:** Mingjie Liu, Shizhe Diao, Ximing Lu, Jian Hu, Xin Dong, Yejin Choi, Jan Kautz, Yi Dong
**Published:** 2025-05-30
**Type:** paper
**Themes:** [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]] · [[themes/reinforcement_learning|Reinforcement Learning]] · [[themes/policy_optimization|Policy Optimization]] · [[themes/reasoning_and_planning|Reasoning and Planning]] · [[themes/rl_theory_and_dynamics|RL Theory and Dynamics]] · [[themes/test_time_compute_scaling|Test-Time Compute Scaling]]

---

## Motivation

A central debate in LLM post-training had crystallized around a pessimistic conclusion: RL-trained models do not acquire new reasoning capabilities beyond what exists latently in their base models. Multiple prior studies (Yue et al., Dang et al., Kirk et al.) cited pass@k metrics showing no improvement relative to base models, arguing that RL algorithms merely amplify dominant pretraining patterns.

ProRL's authors diagnose two compounding methodological failures behind these conclusions:

1. **Domain overfit**: prior work concentrated on mathematics, a domain where models are often already overtrained in both pre-training and post-training, leaving minimal room for RL-driven exploration.
2. **Premature termination**: prior RL runs stopped after hundreds of steps — before models could fully develop new reasoning strategies.

Both failures biased conclusions toward null results. The research question ProRL addresses is whether these conclusions hold under extended, stable training across diverse domains.

---

## The ProRL Methodology

ProRL builds on GRPO with targeted enhancements to sustain productive exploration past the point where prior approaches would collapse.

### Entropy Collapse: The Core Obstacle

The central challenge in prolonged RL training is **entropy collapse**: the policy prematurely commits to a narrow output distribution early in training, eliminating the diversity of rollouts needed for RL to discover new strategies. Standard mitigations are insufficient:

- Increasing rollout temperature only *delays* entropy collapse; it continues declining steadily and does not prevent convergence to a narrow mode.
- DAPO's decoupled clipping (`ϵ_low=0.2`, `ϵ_high=0.4`) promotes exploration of lower-probability tokens by applying asymmetric bounds, reducing premature mode collapse but not eliminating it.

### Stability Stack

ProRL adds two mechanisms on top of GRPO+DAPO:

**KL divergence penalty.** An explicit term penalizes divergence between the current policy and a reference policy: `L_KL-RL = L_GRPO − β·D_KL(π_θ||π_ref)`. This provides stronger and more stable entropy stabilization than temperature adjustment alone.

**Periodic reference policy resets.** As training progresses, the KL penalty term increasingly dominates the loss, causing diminishing policy updates — the regularization begins to strangle learning. ProRL periodically hard-resets the reference policy to a recent snapshot of the online policy and reinitializes optimizer states, allowing continued divergence while retaining the benefits of regularization. This is an explicit workaround for a fundamental tension in the approach.

### Training Corpus

A diverse dataset of 136K verifiable problems spanning math, code, STEM, logic puzzles, and instruction following. Task diversity is treated as a key lever, not an incidental choice — the hypothesis is that cross-domain training drives generalization. Response length is capped at 8k tokens for most training, with a final ~200-step stage at 16k tokens; increasing length too early induces "overthinking" pathology.

---

## Results

### Headline Model

**Nemotron-Research-Reasoning-Qwen-1.5B** — a 1.5B model outperforming its base (DeepSeek-R1-Distill-Qwen-1.5B) and matching or surpassing DeepSeek-R1-Distill-Qwen-7B across diverse benchmarks despite having less than a quarter of the parameters.

Average pass@1 improvements over base:

| Domain | Improvement |
|---|---|
| Math (AIME24/25, AMC, MATH, Minerva, Olympiad) | +15.7% |
| Coding | +14.4% |
| GPQA Diamond (STEM reasoning) | +25.9% |
| IFEval (instruction following) | +22.0% |
| Reasoning Gym (logic puzzles) | +54.8% |

The model also surpasses domain-specialized baselines: DeepScaleR-1.5B (math specialist) by +4.6%, and DeepCoder-1.5B (code specialist) by +6.5% — suggesting that cross-domain RL training is more effective than specialization.

### Genuinely Novel Reasoning

The most significant empirical claim is that ProRL discovers solution pathways entirely absent from the base model's distribution:

- On `family_relationships`: the base model's pass@1 was concentrated at zero; the ProRL model peaked at perfect accuracy.
- On `dice` (logic puzzle): base model achieves `pass@256 = 0.000` (zero correct solutions under unlimited sampling); ProRL model achieves `pass@1 = 0.390` and `pass@256 = 1.000`.
- On `boxnet` (OOD, not seen during training): same pattern — base `pass@256 = 0.000`, ProRL `pass@256 = 1.000`.

The **Creativity Index** (inverse overlap with DOLMA pretraining corpus) increases monotonically with training: 3.84 (base) → 4.42 (intermediate) → 4.70 (final), confirming that extended RL generates reasoning trajectories with genuinely higher novelty rather than recombining pretraining patterns.

### Training-Time Scaling Law

Performance in both pass@1 and pass@16 continued improving past 2,000 training steps — reproducing the compute-scaling law behavior reported for OpenAI O1's RL training. This directly contradicts the assumption that RL gains plateau early and is a key structural result: RL reasoning improvements are a function of training compute, not just architecture.

---

## Key Findings and Implications

**RL gain is predictable from base model competence.** There is a strong negative correlation between RL improvement and the base model's initial task competence (pass@128). Tasks where the base model already performs well see minimal or even *negative* gains in reasoning breadth — RL improves pass@1 at the cost of diversity. Tasks where the base model struggles most benefit most from ProRL. This provides a practical prior for allocating RL compute: invest where the base model is weakest.

**Diversity beats specialization.** A generalist ProRL model trained across five domains outperformed narrow domain specialists on their own benchmarks. The implication is that cross-domain [[themes/reinforcement_learning|RL training]] induces reasoning strategies that transfer, rather than domain-specific heuristics that don't.

**The prior consensus was a methodological artifact.** The claim that RL doesn't expand reasoning boundaries was likely false — not because the underlying mechanism was misunderstood, but because prior experiments stopped too early and used domains where base models had little room to improve.

---

## Limitations and Open Questions

### Technical Limitations

**Entropy collapse is not solved, only managed.** The KL penalty + reference reset stack is an engineering workaround for a fundamental instability. The KL term's tendency to dominate training and require periodic hacks suggests the underlying tension between exploration and regularization in prolonged RL is unresolved.

**RL narrows diversity on capable tasks.** For tasks where the base model already performs well, RL reduces pass@128 even as pass@1 improves. The mechanism converts exploratory diversity into exploitation of the dominant strategy — beneficial for benchmark scores, potentially harmful for robustness.

**Performance degrades with task complexity scaling.** Even with ProRL, accuracy declines consistently as task difficulty scales beyond the training distribution (e.g., larger graph sizes in `graph_color`). Reasoning boundary expansion does not eliminate difficulty scaling — it shifts the threshold.

**Early plateau on a subset of tasks.** For a significant class of tasks, RL gains are achieved early in training and extended steps provide negligible additional benefit, suggesting per-task fundamental limits.

### Scope Limitations

**Scale untested.** All results are at 1.5B parameters. Whether the training-time scaling law and reasoning boundary expansion generalize to 7B, 70B, or larger models is entirely uninvestigated. The 1.5B results may not extrapolate.

**Verifiability constraint.** ProRL applies only to tasks with automatically verifiable rewards (binary or continuous ground-truth signals). Open-ended domains — scientific reasoning, medical diagnosis, legal analysis — cannot benefit from RLVR without a solution to the reward specification problem.

**Compute barrier.** ~16,000 H100 GPU-hours for a 1.5B model creates prohibitive costs for academic research groups, concentrating this line of investigation in industrial labs and slowing iteration speed on methodology.

**Pretraining familiarity ceiling.** Tasks with low Creativity Index (high overlap with pretraining corpus) show minimal reasoning boundary expansion. The approach is structurally weaker for domains well-represented in pretraining data — potentially a fundamental limit rather than an engineering problem.

---

## Connections

- The training-time RL scaling law parallels inference-time scaling observed in O1 and related work in [[themes/test_time_compute_scaling|test-time compute scaling]] — both suggest reasoning capacity is a function of compute investment, just at different stages.
- The entropy collapse problem and reference policy reset mechanism are relevant to the broader [[themes/policy_optimization|policy optimization]] literature on stability in on-policy training.
- ProRL's finding that base model competence predicts RL gain has direct implications for [[themes/rl_theory_and_dynamics|RL theory]]: it suggests RL is operating in a regime of exploration around existing partial capabilities, not building from scratch — the reasoning boundary is an expansion, not a creation.
- The generalist-outperforms-specialist result connects to debates in [[themes/reasoning_and_planning|reasoning and planning]] about whether general-purpose vs. specialized training produces more transferable capabilities.

## Key Concepts

- [[entities/aime|AIME]]
- [[entities/chain-of-thought|Chain-of-Thought]]
- [[entities/deepseek-r1-distill-qwen-15b|DeepSeek-R1-Distill-Qwen-1.5B]]
- [[entities/entropy-collapse|Entropy Collapse]]
- [[entities/grpo|GRPO]]
- [[entities/ifeval|IFEval]]
- [[entities/kl-divergence-penalty|KL divergence penalty]]
- [[entities/minerva-math|Minerva Math]]
- [[entities/olympiadbench|OlympiadBench]]
- [[entities/ppo|PPO]]
- [[entities/rlvr|RLVR]]
- [[entities/reasoning-gym|Reasoning Gym]]
- [[entities/test-time-scaling|Test-time Scaling]]
- [[entities/passk|pass@k]]
- [[entities/verl|verl]]
