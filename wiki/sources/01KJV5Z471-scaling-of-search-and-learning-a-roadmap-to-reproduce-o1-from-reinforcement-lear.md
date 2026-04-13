---
type: source
title: 'Scaling of Search and Learning: A Roadmap to Reproduce o1 from Reinforcement
  Learning Perspective'
source_id: 01KJV5Z47180HNS6GWHJ322R11
source_type: paper
authors:
- Zhiyuan Zeng
- Qinyuan Cheng
- Zhangyue Yin
- Bo Wang
- Shimin Li
- Yunhua Zhou
- Qipeng Guo
- Xuanjing Huang
- Xipeng Qiu
published_at: '2024-12-18 00:00:00'
theme_ids:
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- search_and_tree_reasoning
- test_time_compute_scaling
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 20
tags: []
---
# Scaling of Search and Learning: A Roadmap to Reproduce o1 from Reinforcement Learning Perspective

This paper provides a systems-level roadmap for reproducing OpenAI o1's capabilities through native reinforcement learning — decomposing the problem into four interdependent components (policy initialization, reward design, search, and learning) and analyzing how they compose into a scalable reasoning pipeline. Unlike distillation-based reproduction attempts, the paper argues for RL-first approaches that can in principle surpass teacher models, while identifying the key bottlenecks — domain generalization, reward model distribution shift, and efficient training-time search — that currently constrain the frontier.

**Authors:** Zhiyuan Zeng, Qinyuan Cheng, Zhangyue Yin, Bo Wang, Shimin Li, Yunhua Zhou, Qipeng Guo, Xuanjing Huang, Xipeng Qiu
**Published:** 2024-12-18
**Type:** paper

---

## Expert Analysis

### Motivation and Prior Limitations

OpenAI o1 achieved a qualitative leap to PhD-level reasoning, but its technical mechanisms were not publicly disclosed — OpenAI stated only that reinforcement learning is the core technique, without specifying how policy initialization, reward design, search, and learning interact. This left the research community without a principled reproduction roadmap.

Dominant open-source reproduction attempts relied on **knowledge distillation from o1-style teachers**, which imposes a hard performance ceiling: distillation-based methods improve student models but cannot surpass the teacher, and they preclude discovery of superhuman strategies that pure RL enables. Existing LLM RL work also lacked a unified framework connecting training-time search, test-time compute scaling, reward design granularity, and policy learning — prior contributions (PRM papers, MCTS papers, PPO/DPO papers) remained isolated without a systems-level analysis of how they compose.

A deeper structural issue: naive random sampling during RL training is highly inefficient for o1-style long-chain reasoning. The expanded search space created by human-like reasoning behaviors makes random exploration unlikely to find high-reward trajectories, making structured search essential.

---

### The Four-Component RL Roadmap

#### 1. Policy Initialization

Policy initialization encompasses pre-training (language understanding, world knowledge, basic reasoning), instruction fine-tuning, and then the explicit activation of **six human-like reasoning behaviors**:

- Problem analysis
- Task decomposition
- Task completion
- Alternative proposal
- Self-evaluation
- Self-correction

These behaviors can be instilled via supervised fine-tuning on expert trajectories or triggered via prompt engineering. The authors frame them as manifestations of **self-reflection** — addressing the fundamental autoregressive limitation of inability to revise prior outputs. Long-text generation capability is identified as a prerequisite, since extended CoT chains require models that can generate thousands of coherent tokens without degradation.

A critical tradeoff emerges: initialization from human demonstrations constrains the action space to efficient sampling ranges, but excessive convergence to fixed human strategies may block discovery of superior non-human strategies during subsequent RL — the AlphaGo vs. AlphaGo Zero comparison being the canonical illustration.

#### 2. Reward Design

Reward design is analyzed across two orthogonal dimensions:

- **Granularity**: outcome reward (sparse, easy to construct, no intermediate supervision) vs. process reward (denser, supervises intermediate steps, expensive to annotate)
- **Source**: realistic environment feedback, learned reward models from preference or expert data, and reward shaping via potential-based transformations

**Process reward models (PRMs)** are argued to be more appropriate for long reasoning chains because outcome rewards fail to supervise intermediate steps. The paper shows DPO implicitly performs potential-based reward shaping on preference-learned rewards.

For generalization beyond task-specific rewards, the paper introduces **reward ensembles** (MoE-style per-domain models) and **world models** (jointly predicting next-state representations and reward signals) as the path toward general-purpose agentic behavior.

#### 3. Search

Search is decomposed along two orthogonal axes:

- **Guidance type**: internal (model uncertainty, self-evaluation), external (environmental feedback, heuristic rules), or combined (value functions)
- **Search strategy**: tree search (Best-of-N, beam search, MCTS) or sequential revisions (iterative self-refinement)

The authors speculate that o1 uses **tree search with external guidance during training** (parallelizable, environment-verifiable) and **sequential revisions with internal guidance during inference** (to avoid reward model OOD issues and overoptimization during large-scale test-time search).

MCTS is analyzed at three action granularities:

| Granularity | Characteristics | Tradeoff |
|---|---|---|
| Token-level | Deep trees, narrow width, sparse rewards | Computationally impractical |
| Step-level | Natural for multi-step reasoning | Large action space from sentence diversity |
| Solution-level | Full solutions as nodes, modifications as actions | MCTSr achieves GPT-4-level on math |

#### 4. Learning

Four learning methods are differentiated by gradient variance, memory cost, and data utilization:

- **Behavior cloning**: memory-efficient, fast convergence, uses only Dexpert (highest-reward solutions)
- **REINFORCE**: simple but high variance
- **PPO**: better data utilization via negative solutions from Dsearch (all searched data), higher memory cost
- **DPO**: leverages contrastive signal from negative solutions

The paper hypothesizes o1 likely combines methods: behavior cloning for warm-up, transitioning to PPO or DPO once behavior cloning plateaus to exploit negative solutions for better coverage.

---

## Key Claims

1. o1 represents two paradigm shifts: from supervised learning toward reinforcement learning, and from scaling only training compute to scaling both training and inference compute.
2. Knowledge distillation approaches are fundamentally bounded by the teacher model's capability ceiling — they cannot surpass it.
3. Search and learning are the two methods that scale arbitrarily with increased computation (citing Richard Sutton).
4. Self-reflection capability cannot be effectively learned through parameter-efficient fine-tuning — requires full fine-tuning or prompting.
5. Excessive convergence to fixed strategies during policy initialization can limit discovery of superior approaches during search phases.
6. DPO implicitly performs potential-based reward shaping on preference-learned rewards, with DPO model logits acting as an implicit Q-function.
7. Process rewards are more challenging to learn than outcome rewards, and human annotation makes them costly and difficult to scale.
8. Using human preference-based feedback for complex reasoning tasks (code, math) may actively degrade performance compared to ground-truth outcome rewards.

---

## Capabilities Enabled

- **Six human-like reasoning behaviors** (problem analysis, task decomposition, task completion, alternative proposal, self-evaluation, self-correction) as a decomposition of deliberative reasoning — *narrow_production*
- **MCTS at solution granularity** (MCTSr) achieves GPT-4-level performance on math through self-refinement combined with MCTS — *research_only*
- **Sequential revision search** achieves monotonically improving accuracy as inference-time revisions increase, using self-evaluation as internal guidance — *research_only*
- **Small models outperforming large models** via inference-time search — pass@k metrics improve consistently as samples increase — *demo*
- **DPO model logits as implicit Q-function** enabling value-guided beam search with demonstrated performance gains over standard decoding — *research_only*
- **Semantic entropy** over NLI-clustered responses detects hallucinations at semantic rather than syntactic level — *research_only*

---

## Limitations and Open Problems

### Architectural

**Autoregressive revision impossibility** — LLMs cannot revise previously generated tokens without full regeneration from scratch. Self-reflection behaviors are a workaround, not a solution. *(significant, improving)*

**Long-content generation limits** — LLMs' capacity for generating lengthy content remains insufficient for extended thinking chains despite improvements in long-context processing. *(significant, improving)*

### Reward Design

**Process reward annotation bottleneck** — PRM training requires human annotators for intermediate step labels; this does not scale. Current best-in-class PRMs (e.g., Lightman et al.) depend on human annotation throughout. *(blocking, improving)*

**Preference feedback degrades reasoning performance** — human preference-based feedback for math/code actively harms model performance relative to ground-truth outcome rewards. *(significant, unclear)*

**Reward model distribution shift** — as the policy improves, reward models trained on earlier distributions become unreliable. Scaling parameters and data mitigates but does not eliminate this; the residual fix requires iterative human re-annotation, blocking fully autonomous training loops. *(significant, improving)*

**Value function estimation inaccuracy** — inaccuracies from sparse rewards and high-dimensional outputs cascade to significantly degrade downstream search. Additionally, value estimates trained under one policy are empirically harmful when used for reward shaping under a different policy. *(significant, stable)*

**Exponential action space** — token-level reward function design faces an intractably large token-combination space. *(significant, stable)*

### Search

**Token-level MCTS is computationally impractical** — deep search trees combine with sparse rewards to prevent accurate value estimation, making efficient deployment infeasible. *(significant, unclear)*

**Test-time search causes inverse scaling via distribution shift** — policy, reward, and value models trained on one distribution degrade when evaluated on significantly different test-time distributions created by large-scale search. *(significant, unclear)*

**Unreliable self-evaluation** — models cannot accurately self-evaluate answers without external feedback signals; internal self-evaluation is insufficient as a standalone search guide. *(significant, improving)*

### Generalization

**Domain generalization is unsolved** — all open-source reproductions are restricted to mathematics and coding. No demonstrated path exists to general reasoning across arbitrary domains. *(significant, improving)*

**Human initialization blocks exploration** — initializing from human demonstrations constrains the action space, potentially blocking discovery of superior non-human strategies (the AlphaGo Zero insight applied to LLMs). *(significant, unclear)*

**Reasoning behavior sequencing is open** — systematic orchestration of human-like reasoning behaviors in logically coherent sequences remains unsolved; models lack principled meta-decision capability for when to switch between reasoning modes. *(significant, unclear)*

**Self-reflection requires full fine-tuning** — parameter-efficient fine-tuning methods cannot instill self-reflection capability; this creates a significant compute barrier for capability transfer. *(significant, unclear)*

**IRL conspicuously absent at scale** — Inverse Reinforcement Learning has no demonstrated large-scale application to LLMs despite theoretical promise and available expert data. *(minor, unclear)*

---

## Active Bottlenecks

**Domain generalization of o1-like reasoning** *(1–2 years)*
Reproducing o1-level reasoning beyond math/code is blocked by lack of verifiable reward signals. No scalable mechanism exists to design or train reasoning behaviors that generalize across arbitrary tasks without domain-specific environment feedback.

**Efficient training-time search for RL** *(1–2 years)*
Naive sampling is inadequate for long reasoning chains; advanced structured search is required to generate high-quality training data. The right search strategy and granularity for practical RL training pipelines remains an open systems question.

**Fully automated RL training loops** *(1–2 years)*
Reward model distribution shift requires iterative human involvement as policy capabilities improve. A closed-loop training system that handles its own distribution drift without human re-annotation does not yet exist.

**World model construction for general RL** *(3–5 years)*
The missing link between narrow RL successes and general-purpose autonomous agents: a world model that jointly predicts next-state representations and reward signals across real-world environments beyond closed domains.

---

## Breakthroughs Documented

**o1 validates RL + inference-time search as a new scaling dimension** *(paradigm_shifting)*
Establishing that scaling can proceed along training-time RL and inference-time search — not just data and parameters — constitutes a fundamental shift in how AI capabilities can be developed.

**Small models with search outperform large models without** *(major)*
Test-time compute can substitute for model scale, establishing a new design degree of freedom in the capability-cost tradeoff. This has direct implications for deployment economics and the viability of smaller specialized models.

---

## Themes

- [[themes/reasoning_and_planning|Reasoning and Planning]]
- [[themes/reinforcement_learning|Reinforcement Learning]]
- [[themes/reward_modeling|Reward Modeling]]
- [[themes/rl_for_llm_reasoning|RL for LLM Reasoning]]
- [[themes/search_and_tree_reasoning|Search and Tree Reasoning]]
- [[themes/test_time_compute_scaling|Test-Time Compute Scaling]]

## Key Concepts

- [[entities/behavior-cloning|Behavior Cloning]]
- [[entities/best-of-n-sampling|Best-of-N Sampling]]
- [[entities/direct-preference-optimization|Direct Preference Optimization]]
- [[entities/expert-iteration|Expert Iteration]]
- [[entities/inverse-reinforcement-learning|Inverse Reinforcement Learning]]
- [[entities/outcome-reward-model|Outcome Reward Model]]
- [[entities/policy-gradient|Policy Gradient]]
- [[entities/reinforcement-learning-from-human-feedback|Reinforcement Learning from Human Feedback]]
- [[entities/test-time-compute-scaling|Test-Time Compute Scaling]]
- [[entities/value-function|Value Function]]
- [[entities/world-model|World Model]]
