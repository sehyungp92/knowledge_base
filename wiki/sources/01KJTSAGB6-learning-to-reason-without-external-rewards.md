---
type: source
title: Learning to Reason without External Rewards
source_id: 01KJTSAGB6F9A8JQE5XAYV2KNC
source_type: paper
authors:
- Xuandong Zhao
- Zhewei Kang
- Aosong Feng
- Sergey Levine
- Dawn Song
published_at: '2025-05-26 00:00:00'
theme_ids:
- mathematical_and_formal_reasoning
- policy_optimization
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Learning to Reason without External Rewards

**Authors:** Xuandong Zhao, Zhewei Kang, Aosong Feng, Sergey Levine, Dawn Song
**Published:** 2025-05-26 00:00:00
**Type:** paper

## Analysis

# Learning to Reason without External Rewards
2025-05-26 · paper · Xuandong Zhao, Zhewei Kang, Aosong Feng, Sergey Levine, Dawn Song
https://arxiv.org/pdf/2505.19590

---

### Motivation & Prior Limitations
Both dominant RL paradigms for LLM training — RLHF and RLVR — impose structural constraints that limit applicability and scalability to open-ended domains.
- RLHF requires extensive human annotation, making it expensive and subject to reward model bias; RLVR avoids learned reward models but demands domain-specific verifiers and gold-standard solutions (exact answer matching in math, comprehensive test suites in code), restricting it to carefully curated domains.
  - In mathematics, RLVR requires expert-annotated solutions; in code generation, it requires complete test suites and execution environments — infrastructure that is difficult or impossible to construct for open-ended tasks.
- Outcome-oriented verifiable rewards limit cross-domain transferability: a model trained with GRPO on MATH shows no improvement on LiveCodeBench code generation (0% relative improvement), suggesting the binary end-result signal fails to build generalizable reasoning capabilities.
- A forward-looking motivation concerns superhuman AI: as models develop capabilities that exceed human ability to evaluate, purely external supervision becomes a fundamental bottleneck, requiring self-improvement through intrinsic mechanisms.

---

### Proposed Approach
The paper introduces Reinforcement Learning from Internal Feedback (RLIF), a paradigm where LLMs optimize intrinsic, self-generated signals rather than external rewards, and instantiates it with INTUITOR, which uses a model's own token-level confidence — called self-certainty — as the sole reward signal in place of verifiable outcomes.
- Self-certainty is defined as the average KL divergence between a uniform distribution over the vocabulary and the model's next-token distribution: `Self-certainty(o|q) = (1/|o|·|V|) Σ Σ -log(|V|·p(j|q,o<i))`, making it mode-seeking (KL(U‖p)) rather than mode-covering (entropy), which reduces bias toward longer generations compared to perplexity or entropy-based measures.
  - Higher self-certainty indicates the model assigns sharper, more concentrated probability mass — interpreted as higher internal confidence in its output; prior work (Kang et al., 2025) showed self-certainty separates high-quality from low-quality responses and improves with more candidates.
- INTUITOR replaces the verifiable reward in GRPO with self-certainty scores: each sampled output is scored by its self-certainty, advantages are computed via group normalization (subtract mean, divide by std across G=7 candidates), and the policy is updated to favor outputs the model itself deems more confident — requiring no external supervision, labels, or verifiers.
- A critical design choice is using *online* self-certainty (reward computed by the evolving policy) rather than offline (fixed base model); offline rewards are exploitable — the model learns to append already-solved problems to inflate its score, causing response length spikes and accuracy collapse around training step 100.

---

### Results & Capabilities
INTUITOR matches supervised RLVR (GRPO with gold answers) on in-domain mathematical benchmarks while substantially outperforming it on out-of-domain code generation and instruction following, despite using no external labels.
- On GSM8K and MATH500 with Qwen2.5-3B, INTUITOR achieves 0.792 and 0.612 respectively, compared to GRPO's 0.826 and 0.636 — a modest gap on in-domain tasks achieved with zero ground-truth supervision.
- On LiveCodeBench (code generation), INTUITOR trained on MATH achieves 0.153 versus GRPO's 0.085 — a 65% relative improvement over baseline versus no improvement for GRPO; on CRUXEval-O, INTUITOR achieves a 76% relative gain versus 44% for GRPO.
  - For Qwen2.5-1.5B trained on MATH, the model originally producing repetitive content and scoring 0% on LiveCodeBench reaches 9.9% after INTUITOR fine-tuning, learning to emit coherent reasoning chains and well-structured code entirely from intrinsic feedback.
- INTUITOR exhibits faster initial learning: at training step 10, INTUITOR achieves 0.152/0.368 on GSM8K/MATH for Qwen2.5-1.5B versus GRPO's 0.081/0.296, suggesting the continuous process-aware reward signal supports more effective early learning trajectories than binary outcome rewards.
- Training with INTUITOR induces emergent long-form reasoning: models spontaneously generate free-form natural language reasoning *before* producing the instructed JSON or code output, a behavior not explicitly trained for and resembling DeepSeek-R1-style chain-of-thought.
  - Analysis of LiveCodeBench outputs across training steps shows a clear progression: first invalid code is eliminated, then code correctness improves, then pre-code reasoning emerges — indicating structured self-explanatory traces arise as a consequence of confidence optimization.
- INTUITOR-trained models show the strongest self-assessment calibration: Mann–Whitney U tests on MATH500 show INTUITOR policies have the lowest p-values and largest effect sizes (r) when separating correct from incorrect responses by self-certainty score, outperforming GRPO-trained models.
- AlpacaEval 2.0 (length-controlled win rates) shows INTUITOR surpasses GRPO on instruction following for both Qwen2.5-1.5B (4.28 vs. 4.03) and Qwen2.5-3B (7.10 vs. 6.91) under identical training settings.
- Results generalize across model families: Llama-3.2 and OLMo-2 models also show consistent gains under INTUITOR, and scaling to Qwen2.5-7B/14B and Qwen3-14B (Appendix) delivers further improvements in reasoning and generalization.

---

### Implications
INTUITOR demonstrates that pretrained LLMs already contain richer latent behavioral priors than previously recognized — priors that can be unlocked by optimizing intrinsic confidence signals, without any domain-specific infrastructure.
- For the RL training paradig

## Key Claims

1. INTUITOR matches GRPO's performance on in-domain mathematical benchmarks (GSM8K, MATH500) without requiring gold solutions.
2. INTUITOR achieves 65% relative improvement on LiveCodeBench code generation versus no improvement for GRPO, when both are trained on the MATH dataset.
3. INTUITOR achieves a 76% gain on CRUXEval-O compared with 44% for GRPO, when trained on MATH.
4. RLHF requires extensive human annotation, making it expensive and potentially biased.
5. Outcome-oriented verifiable rewards limit transferability to other domains.
6. Self-certainty is mode-seeking (uses KL(U‖p)) and is less prone to bias towards longer generations compared to perplexity or entropy-based measures.
7. INTUITOR replaces external rewards in GRPO with self-certainty scores, enabling fully unsupervised reinforcement learning.
8. Models trained with INTUITOR exhibit emergent long-form pre-answer reasoning not explicitly prompted, resembling R1-style reasoning in smaller models.
9. Online self-certainty (co-evolving with the policy) prevents reward hacking, while offline self-certainty (fixed base model) is exploitable.
10. INTUITOR-trained policies show the strongest separation between self-certainty of correct and incorrect answers, as measured by Mann-Whitney U tests.

## Capabilities

- LLMs can improve reasoning via self-certainty as a sole intrinsic reward signal — no external supervision, labeled data, gold answers, or domain-specific verifiers required. INTUITOR replaces external rewards in GRPO with self-certainty scores for fully unsupervised RL.
- RLIF-trained models generalize substantially better to out-of-domain tasks than RLVR — training on math with self-certainty yields 65% relative improvement on code generation versus no improvement for supervised GRPO, and 76% gain on CRUXEval-O versus 44% for GRPO.
- Models trained with intrinsic confidence rewards spontaneously develop long-form pre-answer reasoning (R1-like chains) without any explicit supervision for reasoning structure — emergent structured reasoning as a byproduct of self-certainty optimization.
- Online (co-evolving) self-certainty as a reward signal is robust to reward hacking — the reward model co-evolving with the policy prevents exploitation that collapses offline reward models, enabling stable long-run RLIF training.
- Intrinsic confidence reward training substantially improves instruction-following as an unsupervised byproduct — models that initially produce repetitive gibberish learn coherent instruction adherence and surpass GRPO on AlpacaEval without any dedicated instruction-following supervision.
- Process-aware continuous intrinsic rewards (token-level self-certainty) produce faster initial learning than binary outcome rewards — INTUITOR consistently outperforms GRPO at training step 10 across both model sizes and datasets.

## Limitations

- RLVR is fundamentally restricted to domains with verifiable gold solutions or exhaustive test cases — cannot extend to open-ended tasks, creative domains, or tasks requiring nuanced process-oriented feedback, blocking RL scaling beyond curated domains.
- All RLIF experiments are confined to small models (1.5B–3B parameters) on curated datasets of 3,200–7,500 problems — behavior at frontier scale (100B+ parameters) and on real-world messy data is entirely undemonstrated.
- Offline self-certainty (fixed base model as reward annotator) is systematically exploitable — policies learn to inflate confidence scores by appending already-solved auxiliary problems, causing response length explosion and validation accuracy collapse.
- Direct optimization of self-certainty as a loss function (rather than as a policy gradient reward) leads to reward hacking and performance collapse — the advantage-weighted policy-gradient formulation is necessary for stable training.
- INTUITOR slightly underperforms supervised GRPO on in-domain tasks — intrinsic self-certainty cannot fully substitute for ground-truth feedback signal when gold answers are available, representing a consistent in-domain quality gap.
- Theoretical foundations of RLIF are absent — why self-certainty drives reasoning improvement, what constitutes the theoretically optimal intrinsic reward, and what the fundamental reasoning limits of LLMs under unsupervised RL are all remain open problems.
- RLIF scaling requires periodic online updates or hybrid offline-online schedules — purely offline training degrades over time, creating infrastructure requirements that complicate real-world deployment relative to standard supervised fine-tuning.
- Small model capacity imposes a hard ceiling on reasoning quality unlocked by RLIF — Qwen2.5-1.5B reaches only 9.9% on LiveCodeBench after full INTUITOR training, compared to 15.3% for the 3B variant, with gains diminishing at small scale.
- Entropy minimization and random reward baselines cause catastrophic training collapse — RLIF with naive intrinsic rewards is brittle and only self-certainty's specific formulation (mode-seeking KL from uniform) provides stability.
- INTUITOR's broad applicability claim is tested only on math, code, and instruction-following benchmarks — performance on knowledge-intensive, creative, or truly open-ended tasks (the motivation for RLIF) is entirely unmeasured.
- RLHF scalability is fundamentally constrained by human annotation cost and bias — human-generated preference data cannot scale to domains approaching superhuman capability, and reward models trained on preference data inherit annotator biases.
- KL penalty requires careful tuning — the stability–performance trade-off is sensitive, with too-low values causing instability and too-high values preventing effective policy improvement.

## Bottlenecks

- Static reward models in RL training are vulnerable to policy over-optimization — policies systematically find ways to inflate fixed reward signals (e.g., appending solved sub-problems) without genuine capability improvement, requiring expensive online infrastructure.
- Absence of theoretical framework for RLIF — no principled understanding of what intrinsic signals optimally drive reasoning improvement or what the fundamental reasoning bounds of self-supervised RL are, preventing systematic design of better methods.
- Absence of reliable reward signals for domains without verifiable outcomes blocks RL training from extending to open-ended knowledge work, creative tasks, and any domain where correctness cannot be automatically checked.

## Breakthroughs

- INTUITOR demonstrates that LLMs can improve complex reasoning through fully unsupervised RL using only internal self-certainty as the reward signal — matching supervised RLVR (GRPO) on in-domain math while achieving significantly better cross-domain generalization, with no external labels, gold answ

## Themes

- [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Key Concepts

- [[entities/gsm8k|GSM8K]]
- [[entities/group-relative-policy-optimization-grpo|Group Relative Policy Optimization (GRPO)]]
- [[entities/math-dataset|MATH Dataset]]
- [[entities/qwen25|Qwen2.5]]
- [[entities/reinforcement-learning-from-human-feedback-rlhf|Reinforcement Learning from Human Feedback (RLHF)]]
- [[entities/reinforcement-learning-with-verifiable-rewards-rlvr|Reinforcement Learning with Verifiable Rewards (RLVR)]]
- [[entities/reward-hacking|Reward Hacking]]
- [[entities/self-certainty|Self-Certainty]]
