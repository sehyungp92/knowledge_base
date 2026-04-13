---
type: source
title: 'Eureka: Human-Level Reward Design via Coding Large Language Models'
source_id: 01KJVAT1TPBQ037HYKEJ6D3EQD
source_type: paper
authors:
- Yecheng Jason Ma
- William Liang
- Guanzhi Wang
- De-An Huang
- Osbert Bastani
- Dinesh Jayaraman
- Yuke Zhu
- Linxi Fan
- Anima Anandkumar
published_at: '2023-10-19 00:00:00'
theme_ids:
- code_and_software_ai
- code_generation
- reinforcement_learning
- reward_modeling
- robotics_and_embodied_ai
- robot_learning
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Eureka: Human-Level Reward Design via Coding Large Language Models

**Authors:** Yecheng Jason Ma, William Liang, Guanzhi Wang, De-An Huang, Osbert Bastani, Dinesh Jayaraman, Yuke Zhu, Linxi Fan, Anima Anandkumar
**Published:** 2023-10-19 00:00:00
**Type:** paper

## Analysis

# Eureka: Human-Level Reward Design via Coding Large Language Models
2023-10-19 · paper · Yecheng Jason Ma, William Liang, Guanzhi Wang, De-An Huang, Osbert Bastani et al. (9 total)
https://arxiv.org/pdf/2310.12931

---

### Motivation & Prior Limitations
- Reward function design is a fundamental bottleneck in reinforcement learning: a 2023 survey found that 92% of RL researchers report manual trial-and-error reward design and 89% indicate their designed rewards are sub-optimal, producing unintended behavior.
  - This bottleneck is especially acute for complex low-level manipulation tasks such as dexterous pen spinning, which prior LLM-based approaches failed to solve.
- Existing LLM-aided reward design (L2R, Yu et al. 2023) required substantial domain expertise to construct task-specific prompts, motion description templates, and predefined reward API primitives, severely limiting generalization.
  - L2R's reliance on templated reward structures constrained expressivity and left it unable to handle high-dimensional dexterity tasks even when given access to the original human reward components.
- Inverse reinforcement learning (IRL) approaches require expensive expert demonstrations and output non-interpretable black-box rewards that cannot be inspected or iteratively improved.
- Prior evolutionary reward search methods operated only over parameters within fixed, task-specific reward templates rather than over free-form reward programs, limiting their scope to narrow task families.

---

### Proposed Approach
- EUREKA (Evolution-driven Universal REward Kit for Agent) is a reward design algorithm that uses a coding LLM (GPT-4) to perform evolutionary search over free-form executable reward code, requiring no task-specific prompts, reward templates, or few-shot examples.
  - Unlike L2R, which fills in natural language templates and calls predefined reward primitives, EUREKA generates complete Python reward functions from scratch conditioned only on raw environment source code and a natural language task description.
- **Environment as context**: EUREKA feeds the raw environment source code (with an automatic extraction script to isolate state/action variable definitions and fit the context window) directly to the LLM, enabling zero-shot generation of executable reward functions without environment-specific prompt engineering.
- **Evolutionary search**: At each of N iterations, EUREKA samples K independent reward candidates (K=16 in experiments), evaluates them via GPU-accelerated distributed RL on IsaacGym (up to 3 orders of magnitude faster than standard RL), and uses the best-performing reward as the seed for the next iteration's mutation prompt — with multiple random restarts (5 independent runs per environment) to escape local optima.
- **Reward reflection**: Rather than providing only the scalar task fitness score as feedback, EUREKA tracks the per-component scalar values of the reward function alongside task fitness at intermediate training checkpoints, converts this into a textual summary, and appends it to the LLM context to enable targeted, fine-grained reward editing rather than blind re-sampling.
  - Reward reflection addresses two problems: the task fitness function lacks credit assignment (it cannot explain why a reward works), and reward effectiveness is RL-algorithm-dependent, so per-component tracking reveals which components the optimizer actually learned to maximize.
- **Gradient-free RLHF**: EUREKA's in-context improvement loop enables a new form of reinforcement learning from human feedback that requires no model weight updates — humans can either initialize EUREKA with an existing reward function or substitute the automated reward reflection with textual behavioral corrections, which are then propagated through the evolutionary loop.

---

### Results & Capabilities
- EUREKA outperforms expert human-engineered reward functions on 83% of 29 tasks across 10 distinct robot morphologies (quadruped, biped, quadcopter, cobot arm, dexterous hands), achieving an average normalized improvement of 52% over human rewards.
  - On the high-dimensional Dexterity bi-manual benchmark (20 tasks), EUREKA exceeds human performance on 15 of 20 tasks; L2R, despite having access to some of the same reward components as the human baseline, lags far behind on high-dimensional tasks.
- EUREKA's evolutionary optimization is causally necessary for its performance: an ablation sampling 32 rewards in a single non-iterative step (matching the two-iteration reward budget) performs consistently worse than two iterations of EUREKA on both benchmarks, demonstrating that iterative in-context improvement is not replaceable by increased sampling.
- Reward reflection is critical: removing it and substituting only the scalar task fitness score reduces average normalized score by 28.6% across Isaac tasks, with much larger degradation on higher-dimensional tasks.
- EUREKA generates genuinely novel reward functions: correlation analysis between EUREKA and human rewards on Isaac tasks shows that EUREKA rewards are mostly weakly correlated with human rewards, and in some cases negatively correlated yet significantly higher performing, indicating discovery of reward design principles that contradict human intuition.
- Combined with curriculum learning (first training a pen re-orientation policy, then fine-tuning on the spinning task), EUREKA for the first time achieves rapid continuous pen spinning on a simulated anthropomorphic Shadow Hand — a task that neither direct training from scratch nor the pre-trained policy alone could complete even a single cycle of.
- EUREKA (Human Init.) — seeding EUREKA with an existing human reward — uniformly outperforms both the standalone EUREKA and the original human reward across all tested Dexterity tasks regardless of the initial human reward quality, demonstrating reward assistant capability.
- In the gradient-free RLHF setting, a Humanoid trained with textual human reward 

## Key Claims

1. EUREKA generates reward functions that outperform expert human-engineered rewards on 83% of tasks across 29 RL environments, with an average normalized improvement of 52%.
2. 92% of polled RL researchers and practitioners report manual trial-and-error reward design, and 89% indicate their designed rewards are sub-optimal.
3. EUREKA requires no task-specific prompts, reward templates, or few-shot examples, unlike prior LLM-based reward design methods such as L2R.
4. EUREKA takes raw environment source code (without reward code) as context to enable zero-shot generation of executable reward functions.
5. Sampling 16 reward functions per iteration is sufficient to guarantee at least one executable reward code in the first iteration across all tested environments.
6. EUREKA's in-context evolutionary search iteratively refines the best reward from the previous iteration by appending reward reflection and a mutation prompt to the LLM context.
7. Reward reflection — a textual summary of individual reward component values and task fitness at training checkpoints — is critical for targeted reward improvement.
8. Removing reward reflection from EUREKA reduces average normalized score by 28.6% on Isaac tasks, with greater deterioration on higher-dimensional tasks.
9. Simply sampling more reward candidates in the first iteration (without evolutionary refinement) is inferior to EUREKA's iterative evolutionary optimization given the same total reward budget.
10. In some cases, EUREKA rewards are negatively correlated with human rewards yet perform significantly better, demonstrating discovery of reward principles counter to human intuition.

## Capabilities

- Zero-shot generation of executable Python reward code from raw environment source code using GPT-4, without any task-specific prompting, reward templates, or few-shot examples
- LLM-powered evolutionary reward search (iterative sampling, GPU-accelerated RL evaluation, reward reflection) that achieves human-level reward design across 29 diverse RL environments and 10 robot morphologies without domain-specific knowledge
- Gradient-free in-context RLHF: incorporating textual human feedback to steer reward generation toward safer, more aligned behavior without any model weight updates
- Automated reward reflection: textual summarisation of per-component RL training dynamics used as feedback to guide targeted in-context reward mutation, yielding 28.6% average score improvement over fitness-only feedback
- Dexterous rapid pen spinning on a simulated anthropomorphic five-finger Shadow Hand, achieved via EUREKA reward generation combined with curriculum learning — the first demonstration of this capability

## Limitations

- All EUREKA results are in simulation only (IsaacGym); no sim-to-real transfer is attempted or validated — the gap between simulated and real-world dexterous manipulation remains completely unaddressed
- Each EUREKA reward candidate requires a full RL training run to evaluate, making reward search computationally expensive: 5 runs × 5 iterations × 16 candidates = 400 GPU-accelerated RL evaluations per environment
- EUREKA fails to reach human-level performance on 5 out of 20 bi-dexterous manipulation tasks, with the performance gap increasing on the highest-dimensional tasks
- Reward design performance degrades meaningfully when GPT-4 is replaced with GPT-3.5, indicating strong dependency on frontier model capability
- Hardest dexterous tasks (e.g. pen spinning) require multi-stage curriculum learning decomposition — EUREKA alone cannot solve them from scratch in a single training run
- EUREKA relies on pre-tuned, task-specific PPO hyperparameters from the benchmark authors — the system is not validated under different RL algorithm choices or hyperparameter regimes
- Environment complexity is bounded by the LLM's context window — a preprocessing script must truncate environment code to only state/action-variable-exposing snippets, losing broader context
- No analysis of reward hacking, specification gaming, or safety properties of LLM-generated rewards — the paper evaluates only task fitness, not whether generated rewards induce safe or interpretable behaviour in general
- Initial zero-shot reward generations are frequently non-executable or highly sub-optimal — reliable performance requires iterative evolutionary search (multiple LLM calls and full RL evaluations)
- EUREKA-HF (textual human feedback) produces a safer, more preferred gait but at measurable task performance cost — a 26% reduction in forward velocity — revealing an inherent safety-capability trade-off
- EUREKA is only validated on benchmarks with well-defined, queryable fitness functions F — it provides no mechanism for tasks where no ground-truth evaluation signal exists

## Bottlenecks

- Computational cost of reward candidate evaluation in LLM-based reward search — each candidate requires a full RL training run to score, making EUREKA's search budget (400 RL evaluations per environment) prohibitively expensive for many real-world settings
- Absence of cheap reward quality proxies — reward reflection provides training dynamics feedback but cannot predict final task fitness without running full RL, forcing every evaluation through expensive policy training

## Breakthroughs

- LLM-powered evolutionary reward search (EUREKA) achieves human-level reward design across diverse robot morphologies and tasks without any task-specific prompting, templates, or domain expertise — the first automated system to broadly surpass expert human reward engineers
- First demonstration of rapid dexterous pen spinning on a simulated anthropomorphic five-finger hand — a task previously considered infeasible through manual reward engineering — enabled by EUREKA rewards combined with curriculum learning

## Themes

- [[themes/code_and_software_ai|code_and_software_ai]]
- [[themes/code_generation|code_generation]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/robotics_and_embodied_ai|robotics_and_embodied_ai]]
- [[themes/robot_learning|robot_learning]]

## Key Concepts

- [[entities/curriculum-learning|Curriculum Learning]]
- [[entities/eureka|Eureka]]
- [[entities/gpt-4|GPT-4]]
- [[entities/inverse-reinforcement-learning|Inverse Reinforcement Learning]]
- [[entities/proximal-policy-optimization|Proximal Policy Optimization]]
