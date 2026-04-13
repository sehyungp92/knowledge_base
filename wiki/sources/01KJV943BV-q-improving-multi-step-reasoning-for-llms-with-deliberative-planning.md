---
type: source
title: 'Q*: Improving Multi-step Reasoning for LLMs with Deliberative Planning'
source_id: 01KJV943BVJCEEEKHF27A2CWP1
source_type: paper
authors:
- Chaojie Wang
- Yanchen Deng
- Zhiyi Lyu
- Liang Zeng
- Jujie He
- Shuicheng Yan
- Bo An
published_at: '2024-06-20 00:00:00'
theme_ids:
- mathematical_and_formal_reasoning
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- search_and_tree_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Q*: Improving Multi-step Reasoning for LLMs with Deliberative Planning

**Authors:** Chaojie Wang, Yanchen Deng, Zhiyi Lyu, Liang Zeng, Jujie He, Shuicheng Yan, Bo An
**Published:** 2024-06-20 00:00:00
**Type:** paper

## Analysis

# Q*: Improving Multi-step Reasoning for LLMs with Deliberative Planning
2024-06-20 · paper · Chaojie Wang, Yanchen Deng, Zhiyi Lyu, Liang Zeng, Jujie He et al. (7 total)
https://arxiv.org/pdf/2406.14283

---

### Motivation & Prior Limitations
- Auto-regressive generation causes LLMs to compound errors across reasoning steps, producing hallucinations and inconsistent statements as chain length grows, because each token is generated with fixed computation regardless of problem difficulty.
  - This "System 1" mode means LLMs cannot allocate more deliberative effort to harder problems — there is no mechanism to spend more compute on difficult steps.
- Existing approaches to improve multi-step reasoning each carry significant costs that limit generality. Prompt engineering requires per-task expertise; fine-tuning imposes computational burden and risks catastrophic forgetting on other tasks; reward models trained for verification provide no intermediate step guidance.
- Prior deliberative planning methods (Tree-of-Thoughts, MCTS-based approaches, A*) require task-specific utility functions designed by domain experts, making them difficult to generalise across reasoning domains.
  - MCTS-based deliberation requires complete rollouts before scoring, creating substantial inference-time overhead that scales poorly with reasoning depth.

---

### Proposed Approach
- Q* frames multi-step reasoning as a Markov Decision Process and applies A* heuristic search, where a learned plug-and-play Q-value model serves as the heuristic function to score and select the most promising next reasoning step at each node in the search tree.
  - Unlike MCTS-based methods that require full trajectory rollouts for evaluation, Q* evaluates only a single step forward at a time, making deliberation significantly cheaper per decision.
  - Unlike task-specific utility functions in prior planning methods, the Q-value model is trained from ground-truth labels alone and can be applied to any reasoning task without modification to the base LLM.
- The f-value of each state is computed as `f(st) = g(st) + λh(st)`, where `g(st)` is the aggregated process reward along the path to the current state, and `h(st)` is the optimal Q-value estimate for the best available next action, restricted to the top-K candidates from the LLM policy.
- Three methods are proposed for constructing Q-value labels: (1) offline fitted Q-iteration using Bellman bootstrapping over collected trajectories; (2) rollout-based labelling, where the best trajectory from a pool of random or MCTS rollouts assigns the label; and (3) completion with a stronger LLM (e.g., GPT-4) that finishes partial trajectories to estimate downstream reward.
  - Empirically, the rollout-based method proved most effective and robust in practice.
- At inference time, Q* maintains an unvisited frontier and a visited set, always expanding the highest f-value state by querying the LLM for K=6 next-step candidates, collecting N=6 complete trajectories per problem, and returning the trajectory with the highest f-value as the final answer.

---

### Results & Capabilities
- On GSM8K, Q* applied to Llama-2-7b (fine-tuned on MetaMath) achieves 80.8% accuracy using a combined PRM+QVM setup, surpassing ChatGPT-turbo (77.7%) despite using a much smaller open-source model.
  - Best-of-N with the same QVM achieves only 74.5%, and PPO alignment with QVM reaches 67.6%, demonstrating that planning-time use of the value model outperforms both verification-only and alignment-based uses of the same signal.
- On MATH, Q* applied to DeepSeek-Math-7b achieves 55.4%, surpassing Gemini Ultra 4-shot (53.2%) and GPT-4 0-shot (42.5%) on this benchmark; Best-of-N with the same model reaches only 54.3%.
  - Applied to Llama-2-7b fine-tuned on Synthetic Data, Q* reaches 49.1% versus Best-of-N's 46.8%, demonstrating consistent improvement across base models.
- On MBPP code generation, Q* with CodeQwen1.5-7b-Chat achieves 77.0%, compared to 75.0% for Best-of-N and 74.6% for the base model, also surpassing GPT-3.5 Turbo with self-debug (72.8%).
- The Q-value model is plug-and-play: the base LLM is never fine-tuned for the target task, preserving its general capabilities while improving task-specific reasoning performance at inference time.

---

### Implications
- Q* demonstrates that inference-time compute can substitute for fine-tuning, suggesting a paradigm where small frozen LLMs equipped with learned value models can match or exceed much larger proprietary models on structured reasoning tasks without any gradient updates to the base model.
- The MDP framing of multi-step reasoning as a heuristic search problem provides a principled, general interface for plugging in any process reward signal — whether learned from human feedback, ground-truth, rules, or LLM confidence logits — enabling modular improvement of reasoning without architectural changes.
- The result that a 7B open-source model surpasses Gemini Ultra on MATH via planning-time search strengthens the case that test-time compute scaling is a viable alternative or complement to parameter scaling, a trajectory with significant implications for efficient deployment of capable reasoning systems.

---

### Remaining Limitations & Next Steps
- The experiments are restricted to three benchmarks (GSM8K, MATH, MBPP) covering math reasoning and code generation; generalisation to other reasoning domains (e.g., logical reasoning, scientific question answering, planning) is asserted but not demonstrated empirically.
- Q* requires pre-collecting rollout trajectories to construct Q-value labels before training the value model, which itself involves significant compute — this data collection cost is not analysed or compared against the fine-tuning costs it claims to avoid.
- The approach expands K=6 candidates per step and collects N=6 trajectories per problem; the sensitivity of performance to these hyperparameters and the total inference-time compute cost relative to

## Key Claims

1. LLMs are prone to produce errors, hallucinations and inconsistent statements when performing multi-step reasoning due to their auto-regressive nature.
2. Q* guides LLMs during decoding via deliberative planning using a plug-and-play Q-value model as a heuristic function, without fine-tuning the LLM.
3. Avoiding LLM fine-tuning prevents significant computational overhead and risk of performance degeneration on other tasks.
4. The auto-regressive generation process of LLMs corresponds to 'System 1' thinking — fast, instinctive, but less accurate.
5. Solving complex reasoning problems requires 'System 2' thinking — in-depth, deliberative, and logical reasoning.
6. Existing deliberation methods using BFS, DFS, MCTS, and A* require laborious domain-specific utility function design that is hard to extend to new scenarios.
7. MCTS-based deliberation requires a significant number of rollouts before finding high-quality responses for problems with many reasoning steps, substantially slowing decoding.
8. Q* formalizes multi-step LLM reasoning as a Markov Decision Process where state is the concatenation of input prompt and reasoning steps, and action is the next reasoning step.
9. Q* uses an outcome-based reward function that assigns reward 1 if the generated code passes all test cases or the final answer matches the ground-truth, and 0 otherwise.
10. Q* uses the optimal Q-value of a state as the heuristic function h(st) in the A* search f-value computation.

## Capabilities

- A* search guided by learned Q-value models (Q*) improves LLM multi-step reasoning without fine-tuning the base LLM, achieving state-of-the-art results on math and code benchmarks
- Open-source 7B LLMs augmented with test-time deliberative planning can surpass closed-source frontier models on competition math benchmarks
- Process reward models and Q-value models can be combined in A* search to provide step-level guidance, outperforming both PPO alignment and Best-of-N verification on the same base model
- Multi-step reasoning of LLMs can be formalized as an MDP and Q-value labels constructed from ground-truth-only data via offline RL (Fitted Q-iteration) or rollout, without human preference annotations

## Limitations

- Auto-regressive LLM generation cannot dynamically allocate more compute to harder reasoning steps — every token receives equal compute regardless of difficulty
- Error propagation in multi-step reasoning is severe: any incorrect intermediate step cascades to incorrect final answers, compounding with chain length — MATH (11 avg steps) gains less than GSM8K (4.5 avg steps)
- MCTS-based deliberation is too slow for practical use in long multi-step reasoning due to the large number of costly full-trajectory rollouts required before finding high-quality paths
- Process reward models trained on datasets derived from benchmark test sets (PRM800K derived from MATH) introduce contamination that invalidates their use in fair evaluations on those benchmarks
- Q* inference multiplies compute by K×N (K=6 candidates per step, N=6 trajectories collected), imposing substantial overhead relative to standard greedy decoding — costs not analyzed in the paper
- Q-value model training via rollout requires expensive trajectory collection: for every state-action pair, random rollout or MCTS must be run to build the value label pool
- Q* is only validated on verifiable tasks (math with exact numerical answers, code with test cases) — the approach is inapplicable to open-ended tasks, commonsense reasoning, or any domain without automatic correctness checking
- The utility aggregation function (min, max, sum, last) and reward signal source must be manually designed per task, contradicting claims of full task-agnostic generalization
- Fine-tuning LLMs on task-specific data risks catastrophic forgetting and performance degradation on other tasks, creating a fundamental tension between specialization and general capability
- All experiments are limited to 7B parameter open-source models; how Q* scales with larger base models or whether it provides diminishing returns on stronger models is untested

## Bottlenecks

- Standard autoregressive decoding provides no difficulty-adaptive compute allocation, blocking LLMs from reliably solving multi-step problems that require sustained accuracy across many intermediate steps
- Designing task-specific heuristic/utility functions for tree-search planning requires domain expertise per task, blocking generalizable deployment of deliberative planning across diverse reasoning domains
- Lack of automatic verifiable reward signals outside math and code prevents applying test-time compute search methods to open-ended tasks, natural language reasoning, and most real-world domains
- Process reward model training data derived from benchmark test sets contaminates evaluation, preventing use of the best available PRMs for fair measurement of planning-augmented reasoning systems

## Breakthroughs

- Test-time deliberative planning via learned Q-value models (Q*) enables 7B open-source models to surpass closed-source frontier models (Gemini Ultra, ChatGPT-turbo) on math reasoning benchmarks without modifying base model weights

## Themes

- [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/search_and_tree_reasoning|search_and_tree_reasoning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/direct-preference-optimization-dpo|Direct Preference Optimization (DPO)]]
- [[entities/gsm8k|GSM8K]]
- [[entities/metamath|MetaMath]]
- [[entities/monte-carlo-tree-search-mcts|Monte Carlo Tree Search (MCTS)]]
- [[entities/prm800k|PRM800K]]
- [[entities/process-reward-model-prm|Process Reward Model (PRM)]]
- [[entities/reinforcement-learning-from-human-feedback-rlhf|Reinforcement Learning from Human Feedback (RLHF)]]
- [[entities/supervised-fine-tuning-sft|Supervised Fine-Tuning (SFT)]]
- [[entities/system-1-system-2-thinking|System 1 / System 2 Thinking]]
