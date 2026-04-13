---
type: source
title: 'TTRL: Test-Time Reinforcement Learning'
source_id: 01KJTYK6PAKDAAE197XFFK4GZ8
source_type: paper
authors:
- Yuxin Zuo
- Kaiyan Zhang
- Li Sheng
- Shang Qu
- Ganqu Cui
- Xuekai Zhu
- Haozhan Li
- Yuchen Zhang
- Xinwei Long
- Ermo Hua
- Biqing Qi
- Youbang Sun
- Zhiyuan Ma
- Lifan Yuan
- Ning Ding
- Bowen Zhou
published_at: '2025-04-22 00:00:00'
theme_ids:
- policy_optimization
- post_training_methods
- reinforcement_learning
- rl_for_llm_reasoning
- test_time_learning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# TTRL: Test-Time Reinforcement Learning

**Authors:** Yuxin Zuo, Kaiyan Zhang, Li Sheng, Shang Qu, Ganqu Cui, Xuekai Zhu, Haozhan Li, Yuchen Zhang, Xinwei Long, Ermo Hua, Biqing Qi, Youbang Sun, Zhiyuan Ma, Lifan Yuan, Ning Ding, Bowen Zhou
**Published:** 2025-04-22 00:00:00
**Type:** paper

## Analysis

# TTRL: Test-Time Reinforcement Learning
2025-04-22 · paper · Yuxin Zuo, Kaiyan Zhang, Li Sheng, Shang Qu, Ganqu Cui et al. (16 total)
https://arxiv.org/pdf/2504.16084v1

---

### Motivation & Prior Limitations
Current RL-based training pipelines for LLM reasoning depend heavily on ground-truth labeled data, which is increasingly impractical as tasks grow in complexity and volume — the core bottleneck this work directly targets.
- State-of-the-art reasoning models like OpenAI o3 achieve 75.7% on ARC-AGI-1 but only 4% on ARC-AGI-2, illustrating that scaling labeled training cannot keep pace with the emergence of harder, unlabeled problem domains.
  - Silver & Sutton (2025) is cited as motivating the broader shift: existing AI systems that rely on human supervision face fundamental limits, and enabling self-evolution through experience is the necessary path forward.
- Test-Time Training (TTT) paradigms already adapt model parameters at test time using distributional properties of incoming data, but none had previously applied RL in this setting — and RL requires a reward signal, which is absent when labels are unavailable.
- Traditional self-training methods (e.g., selecting self-generated CoT via majority voting for SFT) are bounded by the initial model's majority-vote accuracy, meaning they cannot exceed the performance ceiling encoded in the pre-trained weights.

---

### Proposed Approach
TTRL (Test-Time Reinforcement Learning) performs RL on unlabeled test data by using majority voting over multiple sampled outputs as a proxy reward signal, eliminating the need for ground-truth labels during training.
- Given a prompt x, the model generates N candidate outputs; majority voting derives a consensus answer y*, which is then used as an estimated label to compute rule-based rewards — reward 1 if a sampled output matches y*, else 0.
  - This reframes Test-Time Scaling (TTS), which normally only improves inference-time answers without updating weights, into a training signal that drives RL parameter updates via gradient ascent.
  - The algorithm (implemented using GRPO) uses a "vote-then-sample" strategy: 64 responses are sampled for voting-based label estimation, then 32 are downsampled for training — explicitly trading off compute against signal quality.
- A key mechanism enabling TTRL to function even under incorrect label estimation is "Lucky Hit": when the majority-voted label is wrong but differs from a particular incorrect prediction, the verifier still assigns the correct negative reward to that prediction, maintaining high reward accuracy even at low label accuracy.
  - On AIME 2024, label accuracy can be low while reward accuracy remains near 85–90%, because the probability that a wrong estimated label happens to equal a wrong prediction is low in a high-cardinality answer space.
- The reward signal is dynamic: as training progresses and the model improves, majority voting becomes more accurate, which in turn generates higher-quality supervision — creating a self-reinforcing loop that breaks the static upper bound of traditional self-training.

---

### Results & Capabilities
TTRL consistently improves performance across diverse models, tasks, and scales, with no access to labeled data.
- On AIME 2024, TTRL boosts Qwen2.5-Math-7B from 12.9 to 40.2 pass@1 (+211.6%) and Qwen2.5-Math-1.5B from 7.7 to 15.8 (+105.2%), with average gains of 76.5% and 74.4% respectively across AIME 2024, AMC, MATH-500, and GPQA.
- TTRL surpasses the expected training upper bound (the initial model's maj@n) — on AMC, the final avg@16 after TTRL exceeds the initial maj@16 by more than 20 points, demonstrating that the method escapes the performance ceiling that bounds SFT-based self-training.
  - On MATH-500, the performance curve of TTRL closely tracks that of "RL (leakage)" — direct RL on test data with ground-truth labels — despite TTRL having no label access, indicating near-supervised efficiency in an unsupervised setting.
- TTRL generalizes out-of-distribution: training on AIME 2024 data substantially improves performance on AMC and MATH-500 (e.g., AMC improves from 39.8 to 60.1), indicating the method does not cause overfitting to the training benchmark.
- TTRL is compatible with PPO, GRPO, and PRIME, with closely aligned accuracy and entropy trajectories across all three algorithms on MATH-500.
- TTRL scales naturally with model size: larger models produce more accurate majority voting rewards, leading to more effective self-improvement — confirmed across 1.5B → 7B → 32B Qwen2.5 variants.
- TTRL remains effective on LRMs that have already undergone expensive post-training: applying TTRL to Skywork-OR1-Math-7B and Qwen3-8B (thinking mode) yields approximately 10-point improvements on AIME 2024 for both models.

---

### Implications
TTRL demonstrates that the labeled-data requirement for RL training is not fundamental — reward signals can be bootstrapped from the model's own distributional priors, opening a path toward continual, unsupervised self-improvement at test time.
- This directly weakens the core bottleneck of RL-for-reasoning pipelines: the annotation wall. TTRL suggests that as tasks become harder and labels scarcer, the same unlabeled test data that challenges the model can also train it.
- The "Lucky Hit" mechanism implies that reward accuracy in discrete-answer domains is surprisingly robust to label estimation error, which may generalize the applicability of majority-voting-based pseudo-rewards beyond mathematics to other verifiable domains.
- TTRL bridges Test-Time Scaling (TTS) and Test-Time Training (TTT) into a unified paradigm: sampling multiple outputs improves both inference-time answers (via voting) and the model weights (via RL), compounding the benefits of test-time compute allocation.
- The observation that TTRL approaches RL-with-leakage performance challenges conventional training-evaluation separation — the most efficient adaptation regime may involve training directly on

## Key Claims

1. TTRL boosts the pass@1 performance of Qwen-2.5-Math-7B by approximately 211% on AIME 2024 using only unlabeled test data
2. TTRL consistently surpasses the upper limit of the initial model's maj@n, even though it is only supervised by maj@n during training
3. TTRL approaches the performance of models trained directly on test data with ground-truth labels
4. Common test-time scaling practices like majority voting yield surprisingly effective rewards suitable for driving RL training on unlabeled data
5. Most existing RL methods still rely heavily on labeled data, which significantly limits their scalability
6. OpenAI o3 achieves 75.7% success rate on ARC-AGI-1 but only 4% on the more recently released ARC-AGI-2
7. TTRL scales naturally with model size: larger models produce more accurate majority voting rewards, leading to more effective learning
8. TTRL generalizes well out-of-distribution: training on one benchmark achieves substantial improvements when evaluated on other benchmarks
9. TTRL is compatible with multiple RL algorithms including GRPO, PPO, and PRIME, with closely aligned performance trajectories across all three
10. During TTRL training, both avg@16 and maj@16 metrics demonstrate consistent upward trends simultaneously, indicating TTRL does not improve pass@1 at the cost of majority voting performance

## Capabilities

- LLMs can self-improve via RL on completely unlabeled test data using majority voting as a proxy reward signal (TTRL), achieving 211% improvement on AIME 2024 for Qwen2.5-Math-7B
- TTRL surpasses the traditional self-training upper bound: after RL training on majority-voted pseudo-labels, the model's pass@1 exceeds the initial model's maj@n, breaking the assumed ceiling on self-supervised improvement
- TTRL generalizes out-of-distribution: training on one benchmark's test data (e.g., AIME 2024) transfers performance improvements to other held-out benchmarks (AMC, MATH-500), indicating genuine capability gain rather than overfitting
- TTRL scales naturally with model size: larger models produce more accurate majority voting reward estimates during self-improvement, leading to more effective learning — TTRL inherits compute scaling properties
- TTRL remains effective on large reasoning models (LRMs) that have already undergone expensive RL post-training (Qwen3-8B, Skywork-OR1-Math-7B), yielding ~10 point improvements on AIME 2024
- Majority voting reward estimation is robust even under inaccurate label estimation due to a 'Lucky Hit' mechanism: when the estimated label is wrong but differs from incorrect predictions, the reward signal is still directionally correct
- TTRL is compatible with multiple RL algorithms (GRPO, PPO, PRIME), showing closely aligned performance trajectories — the majority voting reward mechanism is algorithm-agnostic

## Limitations

- TTRL fundamentally requires tasks with verifiable, extractable answers — the majority voting reward mechanism only works when outputs can be compared discretely; it cannot extend to open-ended generation, creative tasks, or agentic objectives
- TTRL quality degrades when the base model has very low accuracy: majority voting on near-random outputs produces noisy pseudo-labels that may mislead RL training; low-capability models may not have sufficient priors to bootstrap from
- TTRL requires substantial compute for rollout: 64 samples per prompt for label estimation plus 32 downsampled responses for training per step, all on 8×A100 80GB GPUs — this is 2–4× the cost of standard RL rollout
- TTRL has been evaluated exclusively on mathematical reasoning and graduate science QA (GPQA); applicability to coding, language understanding, creative tasks, or agentic domains is entirely undemonstrated
- TTRL shows marginal or negative improvement on GPQA for math-specialist models: Qwen2.5-Math-7B degrades by 1.4% on GPQA despite large gains on math benchmarks, suggesting domain mismatch limits cross-domain self-improvement
- Mistral-Nemo-Instruct regresses to 0% on AIME 2024 after TTRL, indicating that certain model families or architectures are incompatible with TTRL or actively harmed by it on very challenging tasks
- TTRL is applied per-benchmark independently — there is no single TTRL run that produces a universally improved model; practical deployment requires separate TTRL passes per domain or task distribution
- Generation length is capped at 3072 tokens for non-LRM models, potentially cutting off complex reasoning chains and limiting TTRL's effectiveness on problems requiring extended thinking
- State-of-the-art models like o3 solve only 4% of ARC-AGI-2 problems, revealing a hard performance cliff where current reasoning approaches completely fail on tasks requiring novel visual abstraction and program induction
- TTRL training dynamics are opaque without ground-truth labels — the paper relies on training-time proxies (majority ratio, label accuracy, reward accuracy) rather than true performance monitoring, making it difficult to know when to stop training

## Bottlenecks

- TTRL's self-evolution mechanism is blocked from tasks without discrete verifiable answers — the majority voting reward function requires extractable answers that can be compared via exact match, excluding open-ended domains entirely
- High rollout compute overhead for TTRL (64 samples per prompt for voting + 32 for training) creates a 2–4× inference cost multiplier that blocks practical deployment at scale or on resource-constrained systems

## Breakthroughs

- TTRL demonstrates that LLMs can exceed their own majority voting accuracy ceiling through RL, breaking the assumed upper bound on self-supervised improvement — the model lifts itself beyond what its initial vote distribution suggested was possible
- Unsupervised RL on unlabeled data (TTRL) approaches the performance of RL trained directly on ground-truth labeled test data — closing the gap between self-supervised and fully-supervised RL to near-zero on structured reasoning tasks

## Themes

- [[themes/policy_optimization|policy_optimization]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/test_time_learning|test_time_learning]]

## Key Concepts

- [[entities/amc|AMC]]
- [[entities/grpo|GRPO]]
- [[entities/prime|PRIME]]
- [[entities/qwen25-math-7b|Qwen2.5-Math-7B]]
- [[entities/test-time-reinforcement-learning-ttrl|Test-Time Reinforcement Learning (TTRL)]]
- [[entities/passk|pass@k]]
