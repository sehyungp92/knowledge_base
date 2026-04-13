---
type: source
title: 'The Majority is not always right: RL training for solution aggregation'
source_id: 01KJTK49M5PZ0W3WXMQ5N2EJK6
source_type: paper
authors:
- Wenting Zhao
- Pranjal Aggarwal
- Swarnadeep Saha
- Asli Celikyilmaz
- Jason Weston
- Ilia Kulikov
published_at: '2025-09-08 00:00:00'
theme_ids:
- mathematical_and_formal_reasoning
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# The Majority is not always right: RL training for solution aggregation

**Authors:** Wenting Zhao, Pranjal Aggarwal, Swarnadeep Saha, Asli Celikyilmaz, Jason Weston, Ilia Kulikov
**Published:** 2025-09-08 00:00:00
**Type:** paper

## Analysis

# The Majority is not always right: RL training for solution aggregation
2025-09-08 · paper · Wenting Zhao, Pranjal Aggarwal, Swarnadeep Saha, Asli Celikyilmaz, Jason Weston et al. (6 total)
https://arxiv.org/pdf/2509.06870

---

### Motivation & Prior Limitations
Majority voting and reward-model ranking — the dominant approaches for aggregating multiple LLM solutions at test time — systematically fail when the correct answer appears only in minority modes, amplifying errors rather than surfacing ground truth.
- Correct answers can be assigned low probability by the model due to modeling errors (Stahlberg & Byrne, 2019), meaning both majority voting and top-score selection will actively choose wrong answers in these cases.
  - Reward-model selection (AceMath-7B/72B best-of-N and weighted majority) is often *inferior* to plain majority voting on competitive math benchmarks, indicating that simply adding a learned scorer introduces more regression than improvement.
- Existing aggregation methods leave unexploited the partial correctness within otherwise incorrect reasoning traces: they select among candidates rather than synthesizing a new, corrected solution from complementary partial steps.
- Concurrent work (Qi et al., 2025) on a learned Sample Set Aggregator (SSA) also trains an aggregator via RL but reports only modest gains, suggesting that the choice of base model and training mixture composition are critical variables that prior work had not resolved.

---

### Proposed Approach
AggLM trains a dedicated aggregation model with GRPO-based reinforcement learning from verifiable rewards (RLVR), treating solution aggregation as an explicit learned reasoning skill rather than a fixed heuristic.
- Given a problem and m candidate solutions from a generator LLM, AggLM is prompted to review, reconcile, correct mistakes, fill gaps, and synthesize a single final answer — behaviors trained end-to-end via binary reward (correct/incorrect against ground truth).
  - This differs from USC/prompting baselines (Chen et al., 2024; Qi et al., 2025) in that the aggregation policy is explicitly optimized via RL rather than relying on the frozen model's zero-shot instruction following.
  - The aggregator receives only the post-`</think>` final answers (not the full chain-of-thought) from thinking-mode solution models, keeping the context tractable.
- A critical design choice is the training data mixture: all "hard" examples (where the majority answer among the 8 candidates is wrong) are retained, and a moderate fraction (5–50%) of "easy" examples (majority correct) are mixed in.
  - Hard-only training produces sparse rewards and undertrains selection of already-correct majority answers; including all easy examples drowns out the hard signal and yields near-untrained performance; the balanced regime is robust across the 5–50% range.
- The solution model and aggregator can share parameters in a multitask setting, where both skills are learned from the same training corpus using different prompt templates, enabling native incorporation into post-training pipelines.

---

### Results & Capabilities
AggLM-1.7B, initialized from Qwen3-1.7B and trained on ~446K aggregation examples derived from DeepScaler, consistently outperforms all baselines across four competitive math benchmarks (AIME24, AIME25, HMMT24, HMMT25).
- On AIME25 with Qwen3-1.7B thinking-mode solutions, AggLM-1.7B achieves 50.0% versus majority voting at 45.89%, best-of-N with AceMath-72B at 40.35%, and the prompted-but-untrained Qwen3-1.7B at 44.85%.
- AggLM-1.7B generalizes out-of-distribution to aggregating solutions from Qwen3-8B (a stronger model never seen during training), remaining the top performer — e.g., HMMT24: 53.01% versus majority voting 44.58% and AceMath-72B best-of-N at 38.54%.
- It also generalizes to non-thinking mode solutions from Qwen3-1.7B, a distribution shift from training, still achieving best overall results (e.g., AIME24: 29.96% versus majority voting 18.07%).
- The aggregator uses roughly one-third the tokens of a solution model per inference (e.g., ~3,039 versus ~10,226 tokens on AIME24), meaning AggLM@8 solutions achieves better accuracy than majority voting at k=16 while consuming substantially fewer total tokens.
- Gains are largest when majority answer size is small (diverse, uncertain solution sets), confirming that the method specifically addresses the minority-correct failure mode; performance is on par with majority voting when the majority answer size is large and the problem is easy.
- Fine-tuning the solution model on the same DeepScaler training data provides negligible or negative improvement relative to the base model, confirming that aggregation gains come from the learned aggregation skill rather than additional training data exposure.

---

### Implications
Learning aggregation as an RL-trained reasoning skill establishes a new axis for test-time compute scaling: rather than simply sampling more solutions and voting, a small aggregator model can synthesize across a fixed solution set more effectively and more cheaply.
- The token-efficiency finding is practically significant: a 1.7B aggregator operating over 8 solutions outperforms majority voting over 16 solutions on multiple benchmarks, suggesting that inference budgets can be reallocated from generation volume to aggregation quality.
- Cross-model generalization (1.7B aggregator improving Qwen3-8B outputs) raises the possibility of training cheap, specialized aggregators once and deploying them across a family of stronger generators — decoupling aggregator training from generator capability.
- The multitask result (single model performing both generation and aggregation with near-parity to the separated setup) points toward aggregation as a native post-training skill, potentially becoming a standard component of future LLM training pipelines alongside instruction following and chain-of-thought.
- The framing of aggregation as a verifiable-reward 

## Key Claims

1. Majority voting can overlook correct minority solutions because correct answers are sometimes assigned low probability under the model due to modeling errors.
2. Standard majority voting and reward model ranking for test-time aggregation may only yield limited benefits.
3. AggLM trains an aggregator model using reinforcement learning from verifiable rewards to review, reconcile, and synthesize a final correct answer from candidate solutions.
4. AggLM-1.7B raises Qwen3-1.7B's accuracy on AIME25 from 35% to 50%, outperforming majority voting at 45%.
5. AggLM-1.7B outperforms reward model selection baselines with 72B parameters on all four math competition benchmarks.
6. Balancing easy and hard training examples is critical for AggLM to learn both minority-correct answer recovery and majority-correct answer handling.
7. AggLM-1.7B generalizes effectively to solutions from stronger models (Qwen3-8B) not present in its training data.
8. AggLM-1.7B generalizes to non-thinking model solutions despite being trained exclusively on thinking-mode distributions.
9. The AggLM aggregator uses roughly one-third as many tokens per generation as the solution models.
10. On AIME25, HMMT24, and HMMT25, aggregating 8 solutions with AggLM-1.7B achieves higher performance than majority voting over 16 solutions.

## Capabilities

- RL-trained solution aggregation (AggLM) learns to review, reconcile, and synthesize a final correct answer from multiple candidate solutions using RLVR, outperforming majority voting and 72B reward-model-based selection with a 1.7B model on math competition benchmarks
- A 1.7B aggregator trained exclusively on weak (1.7B) solution distributions generalizes effectively to aggregating solutions from stronger models (8B) without retraining, maintaining top performance across all benchmarks
- RL-trained solution aggregation requires approximately one-third the tokens of solution generation, enabling higher accuracy at lower inference cost compared to scaling majority voting with additional samples
- A single LLM can be trained in multitask fashion to perform both solution generation and aggregation via different prompts, achieving performance close to separate specialized models — enabling aggregation to be natively incorporated into post-training pipelines

## Limitations

- AggLM training requires verifiable ground-truth rewards, restricting the method to domains with formally checkable solutions — it cannot be directly applied to open-ended creative, analytical, or knowledge-work tasks
- Aggregation performance collapses when base solution quality is very low — with non-thinking 1.7B models achieving pass@1 of ~10%, even the trained aggregator only reaches 12–30% absolute, showing aggregation cannot reconstruct what isn't present in the candidate pool
- Aggregation gains over majority voting vanish when solutions converge — in regimes where the majority answer is large, the trained aggregator performs only on par with simple majority voting, providing no benefit over the free baseline
- Evaluation is confined exclusively to four math competition datasets (AIME, HMMT) with only 30 examples each — there is no evidence that learned aggregation generalises to code generation, scientific reasoning, or natural language tasks
- Small evaluation sets (30 examples per benchmark) introduce high statistical variance — results are mitigated by repeated sampling protocols but the underlying benchmark size limits the confidence of aggregate comparisons
- Training data construction requires sampling 128 independent solutions per problem, creating substantial upfront sampling compute requirements before any aggregator training begins
- Reward-model-based selection (Best-of-N, weighted majority voting with AceMath-7B/72B) is often inferior to simple majority voting, revealing that current large reward models are unreliable discriminators in competitive candidate pools
- Aggregating 8 reasoning traces at up to 16384 tokens each imposes large context window and memory requirements at inference time, limiting deployment to systems with substantial serving infrastructure
- Training the solution model on additional data yields negligible or negative performance gains relative to training a dedicated aggregator — direct solution quality improvements cannot substitute for explicit aggregation skill learning

## Bottlenecks

- Test-time compute pipelines treat solution aggregation as a post-hoc rule-based step (majority voting, reward model selection) rather than a learnable reasoning skill, systematically discarding minority-but-correct answers and partial correctness distributed across candidates

## Breakthroughs

- A 1.7B RL-trained generative aggregator (AggLM) trained with RLVR and balanced easy/hard mixtures outperforms 72B reward-model-based selection and majority voting on math competition benchmarks, establishing that learned generative aggregation supersedes discriminative reward scoring for parallel te

## Themes

- [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/aime|AIME]]
- [[entities/majority-voting|Majority Voting]]
- [[entities/pass1|Pass@1]]
- [[entities/qwen3|Qwen3]]
- [[entities/reinforcement-learning-from-verifiable-rewards|Reinforcement Learning from Verifiable Rewards]]
- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
- [[entities/thinking-mode|Thinking Mode]]
