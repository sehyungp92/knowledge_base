---
type: entity
title: System 1 thinking
entity_type: theory
theme_ids:
- agent_systems
- ai_market_dynamics
- chain_of_thought
- frontier_lab_competition
- mathematical_and_formal_reasoning
- post_training_methods
- pretraining_and_scaling
- reasoning_and_planning
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- scaling_laws
- search_and_tree_reasoning
- software_engineering_agents
- synthetic_data_generation
- test_time_compute_scaling
- test_time_learning
created: '2026-04-08'
updated: '2026-04-08'
source_count: 5
sources_since_update: 0
update_count: 1
influence_score: 0.0006324751455172017
staleness: 0.0
status: active
tags: []
---
# System 1 thinking

> System 1 thinking, borrowed from Kahneman's dual-process theory, describes the fast, automatic, pattern-matching mode of cognition — and has become a central conceptual lens for understanding what large language models actually do during inference. In AI, it maps directly onto next-token prediction from learned weights: rapid, associative, and non-deliberate. As models like OpenAI o1 and techniques like rStar-Math push toward extended test-time reasoning, System 1 has come to define the baseline against which genuine reasoning progress is measured.

**Type:** theory
**Themes:** [[themes/agent_systems|agent_systems]], [[themes/ai_market_dynamics|ai_market_dynamics]], [[themes/chain_of_thought|chain_of_thought]], [[themes/frontier_lab_competition|frontier_lab_competition]], [[themes/mathematical_and_formal_reasoning|mathematical_and_formal_reasoning]], [[themes/post_training_methods|post_training_methods]], [[themes/pretraining_and_scaling|pretraining_and_scaling]], [[themes/reasoning_and_planning|reasoning_and_planning]], [[themes/reinforcement_learning|reinforcement_learning]], [[themes/reward_modeling|reward_modeling]], [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]], [[themes/scaling_laws|scaling_laws]], [[themes/search_and_tree_reasoning|search_and_tree_reasoning]], [[themes/software_engineering_agents|software_engineering_agents]], [[themes/synthetic_data_generation|synthetic_data_generation]], [[themes/test_time_compute_scaling|test_time_compute_scaling]], [[themes/test_time_learning|test_time_learning]]

## Overview

System 1, in the human cognition literature, refers to fast, effortless, automatic processing — the kind that recognises faces, completes familiar sentences, or catches a ball. It requires no deliberate allocation of attention and operates largely below conscious awareness. The analogous operation in transformer-based language models is next-token prediction: given a context, the model's learned weights activate to produce a probability distribution over continuations in a single forward pass. There is no search, no backtracking, no verification — just pattern completion from statistical regularities compressed during pretraining and fine-tuning.

The framing matters precisely because it clarifies what pretraining *cannot* do. A System 1 LLM can reproduce the surface form of mathematical reasoning — writing out equations, naming theorems, following familiar proof templates — without actually checking whether the steps are valid. This is the core insight animating the current wave of [[themes/test_time_compute_scaling|test-time compute scaling]] research: if System 1 is the baseline, then genuine problem-solving requires something more deliberate layered on top of it.

## The Dual-Process Frame in AI Research

Sources like System 2 Reasoning Capabilities Are Nigh and Why o1 is a BIG deal position OpenAI o1 as a meaningful departure from pure System 1 inference. The argument is that o1's extended chain-of-thought — whatever its internal structure — enables the model to allocate more compute to hard problems rather than pattern-matching its way through them. This is not just a quantitative improvement; it is a qualitative shift in the type of computation being performed.

Generative AI's Act o1 and OpenAI o1 - the biggest black box of all both note the opacity of o1's reasoning traces, making it difficult to determine empirically how much of its improvement comes from genuine search versus learned heuristics that mimic search. This ambiguity is important: a model trained to produce long chains of thought might still be operating in a sophisticated System 1 mode — predicting "what a correct reasoning chain looks like" rather than actually reasoning. Distinguishing these is an open and unresolved question.

## System 1 as the Foundation, Not the Ceiling

rStar-Math makes the relationship between the two systems structurally explicit. The policy model — the SLM generating candidate reasoning steps — operates as a System 1 component: it produces next-step continuations from learned weights. The Process Preference Model (PPM) and MCTS search layer constitute the System 2 overlay, evaluating and selecting among those candidates through explicit tree search and backpropagation of outcome signals.

Critically, the quality of System 1 still matters. Step-by-step verified trajectories significantly outperform GPT-4 distillation baselines and rejection sampling as SFT training data precisely because they improve the *distribution* that the policy model (the System 1 component) learns from. The PPM is itself initialised from the fine-tuned policy model, with its next-token prediction head replaced by a scalar value head — making explicit the dependency of System 2 evaluation capacity on System 1 representation quality. Better System 1 representations produce better process reward signals, which in turn generate higher-quality training trajectories for the next round of System 1 improvement. This self-evolution loop — four rounds in rStar-Math, covering 90.25% of 747k math problems by round 4 — shows how System 1 and System 2 components can be iterated together rather than treated as fixed.

## Limitations and Open Questions

The central limitation of System 1 in reasoning contexts is its inability to self-verify. A pure System 1 model has no mechanism to detect when its output is wrong — it has only learned to produce outputs that *look like* correct outputs. This is why rStar-Math's code-augmented CoT synthesis filters intermediate steps by whether the generated Python code actually executes successfully: it substitutes an external verifier for the absent internal one.

What remains unclear is how much of the apparent System 2 capability in current frontier models — including o1 — is genuine deliberation versus highly sophisticated System 1 pattern-matching over reasoning-shaped sequences. A model trained on enough verified reasoning chains may learn to mimic search without performing it. Whether this distinction matters for downstream performance is empirically open: rStar-Math achieves 90.0% on MATH and 53.3% on AIME 2024 with an architecture that keeps the two systems explicit and separable, but that does not settle whether implicit mixing of the two is inferior.

There is also the question of efficiency. System 1 inference is fast and cheap; System 2 overlays like MCTS are expensive. The long-run trajectory of the field — whether inference-time search remains necessary or whether sufficiently trained System 1 models internalise reasoning — remains an active empirical question. Early results from rStar-Math suggest that even small (1.5B–7B parameter) models can rival OpenAI o1 on math benchmarks when given strong System 2 scaffolding, which argues against the view that raw model scale is a prerequisite for hard reasoning. Whether that scaffolding can eventually be distilled back into System 1 weights without performance loss is the key open question for the field.

## Relationships

System 1 thinking is the direct counterpart to System 2 thinking and sits at the conceptual core of debates around [[themes/test_time_compute_scaling|test-time compute scaling]], [[themes/chain_of_thought|chain-of-thought]] methods, and [[themes/search_and_tree_reasoning|search and tree reasoning]]. It is implicitly contrasted with the PPM and MCTS components in rStar-Math and with o1's reasoning process in OpenAI o1 - the biggest black box of all. The [[themes/pretraining_and_scaling|pretraining and scaling]] theme governs how System 1 capability accumulates; [[themes/post_training_methods|post-training methods]] and [[themes/rl_for_llm_reasoning|RL for LLM reasoning]] govern how it is refined and how System 2 overlays are trained on top of it.

## Key Findings

## Sources
