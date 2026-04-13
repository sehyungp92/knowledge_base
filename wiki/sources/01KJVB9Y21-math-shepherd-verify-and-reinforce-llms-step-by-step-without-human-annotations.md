---
type: source
title: 'Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations'
source_id: 01KJVB9Y21W6JA5JE5SP0G3Q4Y
source_type: paper
authors:
- Peiyi Wang
- Lei Li
- Zhihong Shao
- R. X. Xu
- Damai Dai
- Yifei Li
- Deli Chen
- Y. Wu
- Zhifang Sui
published_at: '2023-12-14 00:00:00'
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
# Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations

**Authors:** Peiyi Wang, Lei Li, Zhihong Shao, R. X. Xu, Damai Dai, Yifei Li, Deli Chen, Y. Wu, Zhifang Sui
**Published:** 2023-12-14 00:00:00
**Type:** paper

## Analysis

# Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations
2023-12-14 · paper · Peiyi Wang, Lei Li, Zhihong Shao, R. X. Xu, Damai Dai et al. (9 total)
https://arxiv.org/pdf/2312.08935

---

### Motivation & Prior Limitations
- Process Reward Models (PRMs) outperform Outcome Reward Models (ORMs) for mathematical reasoning verification, but the dominant bottleneck to deploying PRMs at scale was the prohibitive cost of human-annotated step-level supervision data.
  - Uesato et al. (2022) and Lightman et al. (2023) both required human annotators to label individual reasoning steps, a process that is especially expensive for multi-step math problems requiring advanced annotator expertise.
  - The resulting human-annotated dataset (PRM800K from Lightman et al.) was trained on GPT-4 outputs, creating a distribution mismatch when applied to open-source models fine-tuned on different data — undermining its practical utility even when available.
- Existing automatic annotation methods were qualitatively inferior: NLI-based approaches (e.g., DIVERSE-NLI using DeBERTa) achieved only 61.3% step-label accuracy, and rule-based string-matching methods achieved 75.0%, compared to 85–86% for MATH-SHEPHERD's Monte Carlo completion approach.

---

### Proposed Approach
- MATH-SHEPHERD is an automatically constructed Process Reward Model that assigns correctness scores to each reasoning step by estimating a step's potential to reach the correct final answer, using Monte Carlo-style completion rollouts from a fine-tuned LLM "completer."
  - Inspired by Monte Carlo Tree Search, the key insight is that step quality can be operationalised as the fraction of sampled completions from that step that ultimately produce the correct answer — sidestepping the need for explicit human judgment about intermediate correctness.
  - For each step $s_i$ in a solution, a completer LLM decodes $N$ full continuations from $s_i$; two labeling strategies are used: Hard Estimation (HE), which labels a step positive if any completion reaches the correct answer, and Soft Estimation (SE), which labels a step with the proportion of correct completions. Binary cross-entropy training is applied rather than three-class classification, which the authors found equivalent in practice.
- The PRM is used in two deployment modes: (1) best-of-N verification, where the minimum step score across a solution is used to rank 256 candidates; and (2) step-by-step PPO reinforcement learning, where rewards are issued at each reasoning step rather than only at the end of a full response, providing denser training signal than ORM-based PPO.
  - The combination of self-consistency with PRM scores uses a weighted voting scheme: solutions are grouped by final answer, and each group's aggregate RM score determines the winner, blending consistency and quality signals.

---

### Results & Capabilities
- As a verifier over 256 candidates, MATH-SHEPHERD consistently outperforms both self-consistency and ORM across all generator sizes (7B–70B) on GSM8K and MATH500, with the advantage widening on harder problems and larger candidate pools.
  - DeepSeek-67B fine-tuned on MetaMATH reaches 93.3% on GSM8K and 48.1% on MATH500 with MATH-SHEPHERD verification — results the authors describe as unprecedented for open-source models without external tools, exceeding early GPT-4 (92.0% / 42.5%) on both benchmarks.
  - On the harder MATH dataset, automatically constructed MATH-SHEPHERD training data outperforms the human-annotated PRM800K (Lightman et al.), attributed to a 4× larger dataset and better distribution alignment with open-source MetaMATH-trained generators.
- Step-by-step PPO with MATH-SHEPHERD significantly improves 7B-scale models: Mistral-7B improves from 77.9% to 84.1% on GSM8K and from 28.6% to 33.0% on MATH under greedy decoding, outperforming both RFT (+1.1% / +1.3%) and ORM-PPO (+2.3% / +1.7%).
  - Combining step-by-step PPO with subsequent MATH-SHEPHERD verification further pushes Mistral-7B to 89.1% on GSM8K and 43.5% on MATH500, showing that RL training and test-time verification are complementary.
- Out-of-distribution evaluation on the Hungarian national mathematics final exam (33 questions, 100 points) shows PRM generalises beyond its training distribution: LLemma-34B-PRM scores 63 versus LLemma-34B-ORM at 54 and unassisted LLemma-34B at 46, a 9-point margin for PRM over ORM.
- PRM demonstrates superior data efficiency over ORM: with only 10k training solutions, PRM already outperforms ORM by approximately 4% accuracy (best-of-256), and PRM's accuracy continues improving with more data while ORM appears to saturate earlier.

---

### Implications
- Automatic process supervision via Monte Carlo completion effectively breaks the human annotation bottleneck for PRMs, suggesting that scalable step-level reward signals may be achievable across any domain where ground-truth answers are verifiable — not just math.
- The finding that automatically annotated PRM data can outperform human-annotated PRM800K (despite the presence of noise) reframes the annotation quality vs. quantity trade-off: distribution alignment and scale may matter more than annotation precision for reward model effectiveness.
- The complementarity of step-by-step RL training and test-time verification, combined with the observation that a post-PPO model requires a more powerful reward model to supervise it, opens a natural path toward iterative self-improvement loops — the authors explicitly flag this as future work.
- PRM's widening advantage over ORM as task complexity increases (minimal difference on GSM8K, substantial on MATH) implies that step-level feedback becomes increasingly critical as reasoning chains lengthen, with implications for applying PRMs to formal proof verification, code generation, and scientific reasoning chains where errors accumulate across many steps.

---

### Remaining Limitations & Next Steps
- The Monte Carlo completion process is computa

## Key Claims

1. Step-by-step PPO with MATH-SHEPHERD significantly improves Mistral-7B accuracy from 77.9% to 84.1% on GSM8K and from 28.6% to 33.0% on MATH.
2. With MATH-SHEPHERD verification on top of PPO-trained Mistral-7B, accuracy is further enhanced to 89.1% on GSM8K and 43.5% on MATH.
3. DeepSeek-67B achieves 93.3% on GSM8K and 48.1% on MATH with MATH-SHEPHERD verification, which are unprecedented results for open-source models not relying on additional tools.
4. Human annotation for PRM training is costly and hinders the advancement and practical application of PRM, especially for intricate multi-step reasoning tasks requiring advanced annotator skills.
5. PRM is advantageous over ORM because it can identify the specific location of errors in reasoning, which is a valuable signal for reinforcement learning and automatic correction.
6. The quality of a reasoning step in MATH-SHEPHERD is defined as its potential to deduce the correct final answer, inspired by Monte Carlo Tree Search.
7. Hard Estimation (HE) labels a step as good if any one of N completion paths reaches the correct answer, while Soft Estimation (SE) uses the frequency of correct answers across all N paths.
8. Binary classification for PRM training shows no substantial difference from three-class classification (good/neutral/bad).
9. MATH-SHEPHERD as a verifier consistently outperforms self-consistency and ORM across two datasets with all generators tested.
10. PRM achieves a greater advantage over ORM on the more challenging MATH dataset than on the simpler GSM8K, because GSM8K requires fewer steps for problem-solving.

## Capabilities

- Automatic process supervision data construction for PRM training using Monte Carlo-inspired completion: a completer LLM samples N subsequent reasoning paths from each intermediate step, and step quality is estimated by how often those paths reach the correct final answer — eliminating costly human a
- PRM verification (best-of-256 selection) lifts open-source LLMs to unprecedented accuracy on GSM8K and MATH without external tools: DeepSeek-67B reaches 93.3% GSM8K and 48.1% MATH, exceeding GPT-4 (early) on GSM8K
- Step-by-step PPO using an automatic PRM (dense per-step rewards) achieves measurably better reasoning improvement than outcome-supervised PPO (ORM-PPO) on math benchmarks for 7B models
- Automatically constructed process supervision datasets can match or outperform human-annotated datasets (PRM800K) for training PRMs, partly due to distribution alignment with target model outputs and 4× greater data volume
- Process reward models trained on automatically constructed math data generalise to out-of-distribution exam settings, outperforming both the base generator and ORM on unseen Hungarian national final exam problems
- PRM exhibits superior data efficiency over ORM: with only 10k training instances PRM outperforms ORM by ~4% accuracy, and PRM's performance ceiling appears higher than ORM's across all data scales tested

## Limitations

- Automatic PRM construction requires decoding N completion paths per step, making annotation compute cost scale linearly with N×steps×problems — substantially more expensive than ORM annotation even if cheaper than human labelling
- Automatic process annotation introduces label noise: steps are labelled by downstream answer correctness, so a correct intermediate step following an incorrect earlier step may be mislabelled, and false positives increase as N grows large
- The automatic process annotation method requires known golden answers for every training problem — it cannot be applied to open-ended or non-verifiable tasks where correctness cannot be automatically checked
- A reward model that is smaller than the generator it verifies actively degrades performance below self-consistency (majority voting) — the verification infrastructure must be at least as capable as the model it supervises
- After PPO training, the original reward model becomes insufficient to supervise or verify the improved policy — iterative reward model updates are required but not yet implemented, leaving a capability gap
- Completer quality is a hard ceiling on annotation data quality — a weak completer produces systematically noisier step labels, and the completer must have been trained on the specific problem domain to perform adequately
- Hard estimation (HE) annotation accuracy decreases as N increases beyond an optimal value due to false positives — larger N does not monotonically improve data quality, creating a non-trivial hyperparameter sensitivity
- On easier benchmarks (GSM8K), combining PRM verification with self-consistency reduces performance compared to PRM alone — the benefit of process supervision is most pronounced on harder, multi-step tasks and negligible or negative on simpler ones
- Training sequence length is capped at 512 tokens for all experiments, implicitly limiting applicability to math problems solvable within that context — more complex multi-step proofs or coding problems requiring longer chains are excluded
- Human-annotated PRM training data (PRM800K) is distribution-mismatched to open-source model outputs — annotations grounded in GPT-4 outputs do not transfer reliably to LLaMA-family models, rendering expensive human annotation datasets partially invalidated
- Even with best-of-256 PRM verification, open-source 67B models on MATH (48.1%) remain 8+ points below GPT-4-0613 (56.2%), showing that verification and reward modelling alone cannot close the capability gap from the generator
- Step-by-step PPO training with PRM only improves Mistral-7B MATH accuracy from 28.6% to 33.0% — a modest 4.4pp gain — suggesting that RL with process rewards is still far from solving hard mathematical reasoning in small models

## Bottlenecks

- Automatic process reward model construction requires golden (correct) final answers for every training problem, confining scalable PRM training to closed-form verifiable domains — math, formal logic — and blocking application to open-ended reasoning, creative, or real-world agentic tasks
- Static reward models trained before PPO cannot adapt to the improved policy — after RL training the reward model systematically under-discriminates outputs from the stronger model, capping the benefit of iterative RL without reward model refresh
- Completer inference cost for automatic step labelling scales as O(N × steps × problems), imposing a practical compute ceiling on dataset size and annotation quality — creating an economic barrier to applying MCTS-style process supervision at frontier scale

## Breakthroughs

- Automatic process supervision data construction for PRM training: step-level correctness labels can be generated without any human annotation by using a completer LLM to sample completions from each intermediate step and estimating quality via final-answer match rate, inspired by MCTS

## Themes

- [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]

## Key Concepts

- [[entities/gsm8k|GSM8K]]
- [[entities/math500|MATH500]]
- [[entities/metamath|MetaMath]]
- [[entities/outcome-reward-model|Outcome Reward Model]]
- [[entities/prm800k|PRM800K]]
- [[entities/proximal-policy-optimization|Proximal Policy Optimization]]
