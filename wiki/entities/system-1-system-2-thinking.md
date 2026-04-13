---
type: entity
title: System 1 / System 2 Thinking
entity_type: theory
theme_ids:
- agent_systems
- ai_business_and_economics
- ai_governance
- ai_market_dynamics
- alignment_and_safety
- chain_of_thought
- frontier_lab_competition
- hallucination_and_reliability
- latent_reasoning
- mathematical_and_formal_reasoning
- model_commoditization_and_open_source
- multi_agent_coordination
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- scaling_laws
- search_and_tree_reasoning
- software_engineering_agents
- startup_and_investment
- startup_formation_and_gtm
- test_time_compute_scaling
- vertical_ai_and_saas_disruption
created: '2026-04-08'
updated: '2026-04-08'
source_count: 6
sources_since_update: 0
update_count: 1
influence_score: 0.001440137715428549
staleness: 0.0
status: active
tags: []
---
# System 1 / System 2 Thinking

> The dual-process framework from cognitive science — where System 1 denotes fast, automatic, heuristic cognition and System 2 denotes slow, deliberate, rule-governed reasoning — has become one of the most generative conceptual imports into AI research. Applied to large language models, the analogy maps auto-regressive token generation onto System 1 and planning-augmented inference (search, verification, iterative reflection) onto System 2. This framing has directly motivated an entire class of techniques — test-time compute scaling, process reward models, deliberative planning, and inference-time search — that define the current frontier of reasoning research.

**Type:** theory
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/ai_business_and_economics|ai_business_and_economics]], [[themes/ai_governance|ai_governance]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/alignment_and_safety|alignment_and_safety]], [[themes/chain_of_thought|chain_of_thought]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/hallucination_and_reliability|hallucination_and_reliability]], [[themes/latent_reasoning|latent_reasoning]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/model_commoditization_and_open_source|model_commoditization_and_open_source]], [[themes/multi_agent_coordination|multi_agent_coordination]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/scaling_laws|scaling_laws]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/startup_and_investment|startup_and_investment]], [[themes/startup_formation_and_gtm|startup_formation_and_gtm]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/vertical_ai_and_saas_disruption|vertical_ai_and_saas_disruption]]

---

## Overview

The System 1 / System 2 distinction, originally articulated by Daniel Kahneman, describes two modes of thought: one rapid, associative, and low-effort; the other slow, effortful, and governed by explicit rules. In AI research, the framework serves less as a precise technical specification and more as a productive organising metaphor. Standard auto-regressive LLM inference — generating the next token conditioned on all prior tokens — fits System 1 naturally: it is fast, parallel, requires no explicit search, and cannot revise itself mid-generation. System 2 cognition, by contrast, demands the ability to pause, evaluate intermediate states, backtrack, and allocate more computation to hard subproblems. The central question the framework poses for AI is whether and how a model can be made to exhibit genuinely deliberative behaviour — not just the *appearance* of reasoning produced by a sophisticated pattern matcher.

---

## The Q* Paper as a Concrete Instantiation

The most technically direct embodiment of this framework in the source corpus is Q*: Improving Multi-step Reasoning for LLMs with Deliberative Planning. Q* formalises multi-step LLM reasoning as a Markov Decision Process in which the state is the concatenation of the input prompt and all reasoning steps produced so far, and each action is the next reasoning step. This formulation immediately imports the machinery of reinforcement learning and classical search: rather than decoding greedily or via beam search (System 1-style), Q* runs A* search guided by a learned Q-value model that estimates the expected future reward from each intermediate state.

Critically, the Q-value model is plug-and-play — the base LLM is not fine-tuned. This is a deliberate architectural choice: System 2 behaviour is overlaid on a frozen System 1 generator. The heuristic function h(s_t) is set to the optimal Q-value of state s_t, and the f-value combines this with the cost-so-far in the standard A* manner. At each step the system expands K=6 candidate actions drawn from the LLM's top-K policy and collects N=6 full trajectories per question, selecting the trajectory maximising the f-value.

The approach yields striking empirical results. On GSM8K, Q* with a process reward model (PRM) trained on PRM800K and a Q-value model (QVM) pushes Llama-2-7b to 80.8% accuracy, surpassing ChatGPT-turbo at 77.7%. On the MATH dataset, DeepSeek-Math-7b enhanced with Q* reaches 55.4%, exceeding Gemini Ultra (4-shot) at 53.2%. These are headline numbers, but they should be read carefully: the gains are achieved by multiplying inference-time compute (K trajectories, beam expansion at each step), not by improving the underlying model. This is System 2 as a compute budget decision, not a representational one.

Q* proposes three families of approaches for estimating optimal Q-values: offline reinforcement learning via Fitted Q-iteration, learning from rollout by treating the best observed sequence as the target, and completion with a stronger LLM used as a grader. The third option is particularly telling — it grounds the entire search procedure in the signal quality of whatever oracle can be queried at evaluation time, which shifts the bottleneck from search to reward modelling.

---

## Test-Time Compute and the Broader Movement

Q* is not an isolated effort. OpenAI's team on o1 identifies o1 as OpenAI's first major foray into general inference-time compute and reasoning — a public acknowledgement that the field has shifted from training-time scaling alone toward deliberate inference-time deliberation. Noam Brown's talk on multi-agent civilisations reinforces the point with the case of superhuman poker AIs: systems that had already achieved superhuman performance in no-limit Texas Hold'em were not trained differently from weaker predecessors in kind, but rather were given the ability to search more carefully over action sequences. The implication — that deliberation over action spaces is what separates human-level from superhuman performance in strategic domains — maps directly onto the System 2 aspiration for LLMs.

Oriol Vinyals on Gemini 2.0 adds a constraint that complicates the picture: model weights are frozen after training, and all users receive the same fixed checkpoint. System 2 behaviour must therefore be achieved *without* any update to the model's parameters at inference time. This rules out online fine-tuning as a mechanism and places the entire burden on search, verification, and scaffolding — architectures that sit outside the model proper. Pretraining initialises the model to imitate human-generated data; everything after that is fixed. System 2, in this regime, is genuinely an inference-time overlay, not a property of the weights themselves.

---

## JEPA and the Representational Question

Yann LeCun's interview introduces a different angle on the System 1 / System 2 tension. JEPA (Joint Embedding Predictive Architecture) trains a predictor to predict the *representation* of a full input from a corrupted or transformed version, rather than reconstructing pixels or tokens directly. This is a representational bet: that the gap between fast pattern completion and slow deliberative reasoning can be closed not just by adding search on top of an existing model, but by building models that internally represent the world at the right level of abstraction. LeCun's position implicitly challenges the Q*-style approach — if the underlying representations are insufficiently structured, no amount of A* search will produce genuine planning. System 2 capability, on this view, is not separable from what the model has learned to represent.

---

## Commercial Acceleration and the Business Dimension

The System 1 / System 2 framing also illuminates why capability jumps create outsized commercial discontinuities. Why Vertical LLM Agents Are The New $1 Billion SaaS Opportunities documents the case of Casetext and Co-Counsel: within 48 hours of first seeing GPT-4, the company redirected its entire workforce to building on top of it, and within two months of launch entered acquisition talks with Thomson Reuters, closing at $650 million. The speed of this pivot reflects a threshold effect — GPT-4 represented a jump in reasoning capability sufficient to make a qualitatively different class of legal workflows tractable. This is System 2 threshold dynamics at the product level: the market responds not to incremental improvement in token prediction but to emergent capacity for multi-step, judgment-dependent tasks.

---

## Limitations and Open Questions

The framework is productive but carries unresolved tensions worth naming explicitly.

**The oracle problem.** Q* and related approaches depend on process reward models that score intermediate reasoning steps. But PRM quality is itself bounded by the quality of the labels used to train it, which typically come from human annotators or a stronger model. The deliberative search is only as good as its heuristic, and that heuristic is a learned approximation to an oracle that may not exist in sufficient fidelity for novel domains.

**Compute cost is not a free variable.** K=6 trajectories with beam expansion at each step multiplies inference cost dramatically. In commercial deployments where latency and token cost are binding constraints, System 2 behaviour requires explicit cost-benefit reasoning about when to engage deliberation — something the current frameworks largely elide.

**The representational adequacy question.** LeCun's JEPA challenge remains unanswered: if auto-regressive LLMs lack the right internal representations for planning, layering A* search on top may improve benchmark numbers without producing genuine deliberation. Whether Q*-style gains generalise beyond mathematical word problems to open-ended reasoning domains is an open empirical question.

**Frozen weights as a fundamental constraint.** Vinyals' observation that weights are fixed at deployment creates an asymmetry: the model's System 1 capacities are set at training time, but System 2 scaffolding must be engineered separately and cannot adapt the model's internal representations. This architectural separation may prove to be a bottleneck as tasks require deeper integration between fast pattern recognition and slow deliberation.

**Evaluation circularity.** Benchmark performance (GSM8K, MATH) is the primary evidence for System 2 effectiveness, but these benchmarks were available during training data collection and PRM training. The degree to which results reflect genuine generalisation versus sophisticated pattern-matching that mimics deliberation is difficult to establish from benchmark numbers alone.

---

## Relationships

The System 1 / System 2 framework sits at the intersection of several themes in the source corpus. It is the conceptual backbone of [[themes/test_time_compute_scaling|test-time compute scaling]] and directly motivates [[themes/search_and_tree_reasoning|search and tree reasoning]] methods. Its reliance on learned reward signals connects it to [[themes/reward_modeling|reward modeling]] and [[themes/rl_for_llm_reasoning|RL for LLM reasoning]]. The tension between representational adequacy and search-based augmentation links it to [[themes/latent_reasoning|latent reasoning]] and [[themes/pretraining_and_scaling|pretraining and scaling]]. Commercially, threshold effects in reasoning capability connect to [[themes/vertical_ai_and_saas_disruption|vertical AI and SaaS disruption]] and [[themes/startup_formation_and_gtm|startup formation and GTM]].

Key source connections: Q*, OpenAI on o1, Noam Brown on test-time compute, Oriol Vinyals on Gemini 2.0, Yann LeCun Lex Fridman #416, Why Vertical LLM Agents.

## Key Findings

## Sources
