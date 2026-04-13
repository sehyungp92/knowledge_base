---
type: source
title: 'Stream of Search (SoS): Learning to Search in Language'
source_id: 01KJVAT3JDNQ5M2V5VYXGARTH2
source_type: paper
authors:
- Kanishk Gandhi
- Denise Lee
- Gabriel Grand
- Muxin Liu
- Winson Cheng
- Archit Sharma
- Noah D. Goodman
published_at: '2024-04-01 00:00:00'
theme_ids:
- chain_of_thought
- post_training_methods
- reasoning_and_planning
- search_and_tree_reasoning
- synthetic_data_generation
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Stream of Search (SoS): Learning to Search in Language

**Authors:** Kanishk Gandhi, Denise Lee, Gabriel Grand, Muxin Liu, Winson Cheng, Archit Sharma, Noah D. Goodman
**Published:** 2024-04-01 00:00:00
**Type:** paper

## Analysis

# Stream of Search (SoS): Learning to Search in Language
2024-04-01 · paper · Kanishk Gandhi, Denise Lee, Gabriel Grand, Muxin Liu, Winson Cheng et al. (7 total)
https://arxiv.org/pdf/2404.03683

---

### Motivation & Prior Limitations
Language models trained exclusively on optimal solution trajectories never observe productive mistakes, backtracking, or recovery, which causes them to treat problem-solving as a single-pass process rather than an iterative search.
- Autoregressive transformers suffer from two compounding failure modes that degrade multi-step reasoning: error snowballing, where a single mistake cascades into increasingly poor subsequent steps, and lookahead failure, where the model cannot predict consequences of actions several steps ahead.
  - LeCun (2023) and Bachmann & Nagarajan (2024) identify these as structural weaknesses of the autoregressive paradigm, not incidental training artifacts.
- Existing hybrid approaches — Tree of Thought (ToT), SayPlan, etc. — treat the language model as a sub-component of an external symbolic search system, improving search at inference time but leaving the LM's internal reasoning ability unchanged.
  - These extrinsic methods carry high inference costs, rely on a fixed, externally-specified search strategy, and do not enable the model to discover or generalize search procedures autonomously.
- Process supervision (Lightman et al., 2023) provides step-level feedback but requires large human-annotated datasets for each intermediate reasoning step and a separately trained verifier model, limiting scalability to new domains.

---

### Proposed Approach
The paper introduces Stream of Search (SoS), a framework that represents the full process of search — including exploration, backtracking, dead ends, and goal checks — as a flat serialized string in natural language, and trains a language model directly on this process rather than on cleaned optimal paths.
- A unified vocabulary of primitive search operations (Current State, State Expansion, Exploration Choice, Backtracking, Goal Check, Heuristic, Pruning) is defined to capture components shared across BFS, DFS, A*, and other symbolic strategies, enabling diverse search procedures to be expressed in a common format.
  - Some operations (backtracking, goal checks, exploration choices) are rendered explicit in text; others (heuristic values, pruning strategy) remain implicit, encouraging the model to internalize latent representations that can be refined through training.
- A synthetic dataset of 500,000 search trajectories is generated for the Countdown arithmetic game using 12 heuristic symbolic solvers combining BFS/DFS variants with two interpretable heuristics (absolute difference from target sum; distance to target's factors); crucially, ~43% of these trajectories fail to reach a solution, intentionally preserving suboptimal and unsuccessful search episodes.
  - This contrasts sharply with prior work (Yang et al., 2022; Lehnert et al., 2024) which trains transformers to imitate a single fixed search procedure (MCTS or A*); SoS exposes the model to diverse strategies simultaneously, aiming for autonomous strategy selection rather than procedural mimicry.
- After SoS pretraining, the model is further improved using two policy improvement methods: STaR (expert iteration — filter self-generated correct trajectories, finetune iteratively) and APA (Advantage-Induced Policy Alignment — an Actor-Critic RL technique using a learned value network and a shifting reference policy to stabilize training and prevent collapse).

---

### Results & Capabilities
SoS pretraining on diverse, suboptimal search trajectories substantially outperforms training on optimal paths alone, achieving 51.27% accuracy on held-out inputs versus 25.73% for the Optimal Path baseline — a 25-percentage-point absolute improvement, despite the SoS dataset containing fewer correct examples (285k vs. 500k).
- The SoS model generalizes to both seen-target/new-input and new-target/new-input splits, demonstrating the search strategy is not memorized per-target.
- The SoS model's search trajectories are not highly correlated with any single symbolic strategy in terms of states visited (highest alignment with DFS+sum heuristic at 0.57, lowest with BFS breadth=5+sum at 0.27), indicating emergent blending of strategies rather than mimicry of any training exemplar.

Policy improvement with STaR and APA further extends capability beyond the symbolic strategies used to generate the training data.
- After 3 STaR iterations, SoS+STaR solves an additional 5% of held-out problems beyond the base SoS model; SoS+APA achieves ~6% additional improvement via 3 reference policy resets.
- The finetuned models solve approximately 36% of problems that were unsolved by all symbolic strategies at dataset generation time, and ~4% of "difficult" problems that none of the 12 symbolic strategies can solve at all.
- Policy-improved models make fewer arithmetic errors per trajectory and visit fewer states on correct solutions, indicating both better world-model accuracy and more efficient search.
- The APA-finetuned model diverges more from the symbolic strategy distribution than STaR does, suggesting APA explores a broader region of strategy space — consistent with discovering genuinely novel search heuristics.

---

### Implications
Representing search as flattened language sequences rather than as external tree structures suggests that the inductive biases needed for planning and backtracking can be learned within the sequence modeling paradigm itself, without architectural changes or inference-time scaffolding.
- This directly challenges the claim that autoregressive LMs are structurally incapable of planning, showing instead that the deficit is a training data problem: models are never shown productive mistakes.

The result that LMs can solve problems no symbolic heuristic solver in the training set could solve implies that LMs trained on diverse search 

## Key Claims

1. Language models trained only on optimal solutions learn that problems must be solved in one clean pass, failing to learn search, planning, or backtracking.
2. Transformer-based autoregressive models suffer from two key planning failures: snowballing errors (single mistakes compound) and difficulty with lookahead tasks requiring multi-step consequence predic
3. Existing LM-integrated search systems (e.g., Tree of Thoughts) only use LMs at inference time and do not improve the model's reasoning ability through training.
4. Tree-of-Thoughts style approaches incur high inference costs compared to methods that learn an intrinsic search policy.
5. Process supervision outperforms outcome supervision in mathematical reasoning tasks but requires large labelled datasets with human-generated annotations for each intermediate step, limiting scalabili
6. SoS pretraining increases search accuracy by approximately 25 percentage points over models trained only on optimal trajectories.
7. The SoS model achieves 51.27% accuracy on held-out inputs compared to 25.73% for the optimal path model, despite training on fewer correct examples.
8. Only 57% of the 500,000 training search trajectories lead to a solution, yet the SoS model still outperforms models trained solely on optimal solutions.
9. The SoS model's search trajectory is not highly correlated with any single symbolic search strategy, indicating it learns a blend of strategies rather than imitating one.
10. After policy improvement with STaR and APA, finetuned SoS models solve 36% of problems previously unsolved by any symbolic search strategy.

## Capabilities

- Language models trained on diverse search trajectories (including failures and backtracking) achieve 51.27% accuracy on Countdown versus 25.73% for models trained on optimal paths only — a 2x improvement despite having fewer correct training examples
- SoS models fine-tuned via policy improvement (STaR and APA) solve 36% of problems previously unsolved by any symbolic heuristic strategy, and ~4% of problems no symbolic algorithm in training can solve — demonstrating emergent search capability beyond the training distribution
- Language models trained on search trajectories develop flexible mixed search strategies not corresponding to any single training heuristic — SoS model's state visitation correlates at most 0.57 with any individual symbolic strategy it was trained on
- LMs trained on search trajectories can simulate environment state transitions internally without external environment access — achieving valid exploration with only 0.8% state exploration error rate, effectively learning an internal world model for search

## Limitations

- SoS results are restricted to a single combinatorial puzzle domain (Countdown); generalization to real-world planning tasks, informal domains, or even other formal domains remains entirely untested
- Search trajectory length grows super-linearly with problem complexity — 5-input Countdown problems produce 60,000+ token traces that exceed standard context windows, creating a hard scaling wall for harder or real-world problems
- Bootstrapping the SoS training pipeline requires pre-existing symbolic solvers for the target domain — if no solver exists, the SoS data generation pipeline cannot be initiated at all
- SoS models solve only ~4% of 'difficult' problems (those unsolvable by any training-set symbolic strategy), indicating that emergent search capability beyond the training distribution remains marginal even after policy improvement
- Externally-structured tree search (Tree of Thought) explicitly acknowledged as more inference-efficient than internalized SoS in the short term, limiting practical deployment advantage of the approach
- All experiments conducted on a 250M parameter GPT-Neo model — whether SoS findings scale to larger models or translate to frontier-scale architectures is entirely untested
- State evaluation and pruning strategies are left implicit in the network and not represented in language, preventing these components from being directly improved via targeted training signal or extended to explicit reasoning
- Standard LM training on optimal solutions alone produces severely degraded planning capability (25.73% on Countdown), indicating that current internet-scale pre-training data systematically omits the process of problem-solving in favour of final answers
- STaR policy improvement converges after only 3 iterations and APA after ~3 reference policy resets, suggesting self-improvement loops for learned search hit diminishing returns quickly without architectural or data-diversity interventions

## Bottlenecks

- Bootstrapping SoS training requires symbolic search algorithms for the target domain — domains without pre-existing solvers cannot initiate the SoS data generation pipeline, blocking extension of learned search to novel, informal, or open-ended real-world domains
- Serialized search trace length grows exponentially with state-space complexity — this blocks SoS training and inference from scaling to problems with large branching factors or deep search horizons within current context window constraints

## Breakthroughs

- Training language models on the full search process — including failures, backtracking, and suboptimal trajectories — produces dramatically better problem-solving than training on optimal solutions alone, demonstrating that 'productive mistakes' are essential and not noise

## Themes

- [[themes/chain_of_thought|chain_of_thought]]
- [[themes/post_training_methods|post_training_methods]]
- [[themes/reasoning_and_planning|reasoning_and_planning]]
- [[themes/search_and_tree_reasoning|search_and_tree_reasoning]]
- [[themes/synthetic_data_generation|synthetic_data_generation]]
- [[themes/test_time_compute_scaling|test_time_compute_scaling]]

## Key Concepts

- [[entities/self-taught-reasoner-star|Self-Taught Reasoner (STaR)]]
