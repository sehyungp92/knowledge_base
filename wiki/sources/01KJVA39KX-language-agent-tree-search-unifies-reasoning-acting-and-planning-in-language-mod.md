---
type: source
title: Language Agent Tree Search Unifies Reasoning Acting and Planning in Language
  Models
source_id: 01KJVA39KX5F13FQ8FZDBMKCCA
source_type: paper
authors:
- Andy Zhou
- Kai Yan
- Michal Shlapentokh-Rothman
- Haohan Wang
- Yu-Xiong Wang
published_at: '2023-10-06 00:00:00'
theme_ids:
- agent_systems
- chain_of_thought
- reasoning_and_planning
- search_and_tree_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models

**Authors:** Andy Zhou, Kai Yan, Michal Shlapentokh-Rothman, Haohan Wang, Yu-Xiong Wang
**Published:** 2023-10-06 00:00:00
**Type:** paper

## Analysis

# Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models
2023-10-06 · paper · Andy Zhou, Kai Yan, Michal Shlapentokh-Rothman, Haohan Wang, Yu-Xiong Wang
https://arxiv.org/pdf/2310.04406

---

### Motivation & Prior Limitations
Prior LM prompting methods for reasoning and acting were reflexive — they generated trajectories autoregressively without considering alternative paths, making them brittle on difficult multi-step tasks.
- Chain-of-thought and ReAct suffer from error propagation across steps because they commit to a single trajectory, and self-consistency methods (majority voting) explore alternatives only at the output level rather than at intermediate decision points.
- Search-augmented reasoning methods like Tree-of-Thought (ToT) and RAP introduced planning over multiple reasoning chains but operated in isolation from external environments, relying entirely on the LM's internal knowledge and exposing them to hallucination and a hard performance ceiling.
  - The authors demonstrate empirically that naively combining search algorithms with ReAct-style acting (their "ToT (ReAct)" and "RAP (ReAct)" baselines) actually degrades performance compared to reasoning-only variants on HotPotQA (EM 0.39 and 0.54 respectively, vs. 0.55 and 0.60 for pure reasoning), showing the adaptation is non-trivial.
- Reflexion and self-refine introduced LM-generated feedback to improve individual trajectories but did not explore alternative action choices at each step, causing agents to get stuck in local minima in complex environments like WebShop.
- RAP specifically required the LM to serve as a world model capable of predicting future states, constraining its applicability to tasks where this internal simulation is feasible.

---

### Proposed Approach
LATS (Language Agent Tree Search) is a unified framework that adapts Monte Carlo Tree Search (MCTS) to LM agents, integrating reasoning, acting, and planning by treating each node in the search tree as a state comprising the original input, action history, and observation history.

- The key insight enabling MCTS for LMs is that most LM tasks permit reverting to any prior state by simply restoring the historical text context — no learned environment model is needed, unlike in RL applications of MCTS.
  - This directly removes the world-model requirement that constrained RAP, allowing LATS to ground its search in real environment interactions rather than simulated rollouts.
- LATS executes six operations per search episode — selection (UCT-guided), expansion (sampling n actions from the LM and receiving environment observations), evaluation, simulation (greedy rollout to terminal), backpropagation, and reflection — iterating until success or a budget of k trajectories is reached.
- The value function V(s) = λ·LM(s) + (1−λ)·SC(s) combines an LM-generated scalar score (obtained after observing environment feedback, unlike ToT which scores before feedback) with a self-consistency score that rewards actions sampled consistently across multiple expansions of the same state.
  - Evaluating state value after receiving environmental feedback is identified as a critical design choice: it allows the value function to incorporate real-world signal rather than relying solely on prior LM knowledge, enabling the method to scale to harder environments.
- Upon trajectory failure, LATS prompts the LM to generate a verbal self-reflection summarizing errors and proposing alternatives; both the failed trajectory and reflection are stored in external memory and injected as context for future tree iterations, providing a "semantic gradient" without gradient-based optimization.
- The framework is modular: the base LM agent, value function, and reflection generator can each be swapped independently, and the state design and tree dimensions can be adjusted per environment and compute budget.

---

### Results & Capabilities
LATS achieves state-of-the-art pass@1 accuracy of 92.7% on HumanEval with GPT-4, surpassing Reflexion (91.0%) and the GPT-4 base LM (80.1%), and sets the highest scores across all evaluated domains.

- On HotPotQA with GPT-3.5, LATS (CoT+ReAct) reaches EM 0.71, more than doubling ReAct's 0.32 and outperforming all reasoning-only baselines including RAP (0.60) and ToT (0.55).
- On HumanEval with GPT-3.5, LATS (ReAct) achieves 83.8% pass@1, compared to Reflexion's 68.1%, RAP's 63.1%, and ReAct's 56.9%; on MBPP, LATS reaches 81.1% versus RAP's 71.4%.
- On WebShop, LATS with GPT-3.5 achieves an average score of 75.9 and a success rate of 38%, surpassing Reflexion (64.2/35%), ReAct best-of-30 (59.1/32%), and gradient-based IL+RL fine-tuning (62.4/28.7%) — approaching the fine-tuned baseline (67.5/45%) without any weight updates.
- On Game of 24, a purely internal reasoning task, LATS (CoT) reaches a 0.44 success rate versus RAP's 0.40 and ToT's 0.20, demonstrating that the self-consistency-augmented value function adds benefit even without environment interaction.
- LATS is more computationally efficient than competing tree-search methods at equivalent trajectory budgets: on HotPotQA with k=50, LATS expands an average of 66.65 nodes compared to RAP's 70.60 and ToT's 84.05, despite achieving higher accuracy, because its principled UCT-based selection reaches solutions faster.
  - LATS and other tree-based methods share O(kn) sample complexity; the efficiency advantage compounds because LATS hits the budget ceiling (failed search) less often due to higher success rates.

---

### Implications
LATS demonstrates that test-time compute in the form of structured tree search is a viable and powerful alternative to gradient-based fine-tuning for improving LM agent performance, achieving gradient-free results competitive with RL-trained models on WebShop.

- The framework legitimizes MCTS as a general-purpose inference-time planning algorithm for LMs, extending its success from game-playing (AlphaGo, MuZero) to open-ended language tasks — provi

## Key Claims

1. LATS is the first general framework that synergizes the capabilities of language models in reasoning, acting, and planning simultaneously.
2. LATS achieves state-of-the-art pass@1 accuracy of 92.7% on HumanEval with GPT-4.
3. LATS doubles the performance of ReAct on HotPotQA with GPT-3.5.
4. LATS raises the average score by 22.1 on WebShop with GPT-3.5 compared to ReAct.
5. For most LM tasks, tree-based search does not require an explicit environment model because any state can be restored by copy-pasting historical text context.
6. Existing acting-based methods such as ReAct and Reflexion refine only a single trajectory and do not consider alternative choices at each step.
7. Language models cannot self-correct their internal reasoning without external feedback, making external feedback critical.
8. Chain-of-thought prompting suffers from error propagation due to compound errors as the number of reasoning steps increases.
9. RAP is constrained to tasks where the LM can serve as a world model and accurately predict future states, limiting its generality.
10. LATS uses a value function combining a self-generated LM score and a self-consistency score, weighted by a hyperparameter lambda.

## Capabilities

- MCTS-based unified reasoning/acting/planning framework (LATS) achieves 92.7% Pass@1 on HumanEval with GPT-4 — state-of-the-art for code generation without gradient-based fine-tuning
- LM-powered value functions combining self-generated state scores and self-consistency heuristics enable zero-additional-training MCTS search over language agent trajectories
- Self-reflection on failed trajectories provides a semantic gradient signal enabling trial-and-error improvement in LM agents without expensive RL optimization
- Gradient-free prompting-based LM agent matches RL-trained fine-tuned baselines on web navigation (75.9 score on WebShop with GPT-3.5, surpassing IL+RL at 62.4)
- Unified LATS framework doubles ReAct performance on multi-hop QA and achieves +22.1 on WebShop, generalising across programming, QA, web navigation, and mathematical reasoning without task-specific adaptation

## Limitations

- LATS is architecturally restricted to environments where any prior state can be restored by replaying context — irreversible real-world actions (database writes, physical robot moves, live API calls) are outside scope
- Self-generated LM reflections in high-dimensional environments (e.g. product search) are consistently generic and fail to identify specific causal errors, causing agents to get stuck in local minima
- Principled tree search scales as O(kn) in token consumption — the multiplicative branching factor makes LATS an order of magnitude more expensive than O(k) baselines like best-of-k ReAct
- HotPotQA evaluation relies on an oracle setup where the environment reveals answer correctness on demand — this controlled condition is unavailable in realistic open-domain QA, masking true search quality
- LMs cannot self-correct internal reasoning without external feedback — reflection on self-generated content is insufficient and may systematically fail to improve reasoning quality
- Autoregressive chain-of-thought reasoning suffers compound error propagation — each incorrect intermediate step increases downstream failure probability, creating a performance cliff for long reasoning chains
- LATS success rate on WebShop is 38% vs. expert 59.6% and human expert 82.1% — a persistent large gap remains on real-world complex web navigation despite substantial improvements over all baselines
- Naive integration of tree search algorithms (ToT, RAP) with acting-based prompting (ReAct) degrades performance below reasoning-only variants — adaptation of search to decision-making is non-trivial
- Reasoning-only methods (CoT, ToT, RAP) operating from internal LM knowledge face a performance ceiling from hallucination and knowledge staleness — they cannot incorporate external observations at all
- Evaluations use small samples (100 HotPotQA questions, 50 WebShop instructions) — results may not be statistically robust enough to detect meaningful differences across methods, especially for rare failure modes
- LATS is not evaluated on any task involving irreversible real-world state — robotics, live databases, email sending, and persistent code execution are conspicuously absent from evaluation domains

## Bottlenecks

- Tree search for language agents carries O(kn) inference cost — the multiplicative branching factor makes principled planning over action trajectories prohibitively expensive for latency-sensitive or cost-constrained production deployment
- LM self-reflection quality degrades in high-dimensional environments — generic reflections fail to isolate causal errors in complex action spaces, blocking self-improving agents that learn from failures without RL
- MCTS-based language agent planning depends on environment-provided correctness signals — without oracle or verifiable reward functions, value function quality collapses and search efficiency is no better than random

## Breakthroughs

- LATS is the first framework to unify LM reasoning, acting, and planning in a single MCTS-based architecture — achieving state-of-the-art results across programming, QA, web navigation, and math without task-specific tuning or gradient-based training

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/search_and_tree_reasoning|search_and_tree_reasoning]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/exact-match-em|Exact Match (EM)]]
- [[entities/game-of-24|Game of 24]]
- [[entities/hotpotqa|HotpotQA]]
- [[entities/monte-carlo-tree-search-mcts|Monte Carlo Tree Search (MCTS)]]
- [[entities/pass1|Pass@1]]
- [[entities/react|ReAct]]
- [[entities/reflexion|Reflexion]]
- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
- [[entities/webshop|WebShop]]
