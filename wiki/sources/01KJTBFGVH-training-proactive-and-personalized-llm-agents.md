---
type: source
title: Training Proactive and Personalized LLM Agents
source_id: 01KJTBFGVHSXEWM2ASDNX9WB79
source_type: paper
authors:
- Weiwei Sun
- Xuhui Zhou
- Weihua Du
- Xingyao Wang
- Sean Welleck
- Graham Neubig
- Maarten Sap
- Yiming Yang
published_at: '2025-11-04 00:00:00'
theme_ids:
- agent_systems
- policy_optimization
- reinforcement_learning
- reward_modeling
- rl_for_llm_reasoning
- software_engineering_agents
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 18
tags: []
---
# Training Proactive and Personalized LLM Agents

**Authors:** Weiwei Sun, Xuhui Zhou, Weihua Du, Xingyao Wang, Sean Welleck, Graham Neubig, Maarten Sap, Yiming Yang
**Published:** 2025-11-04 00:00:00
**Type:** paper

## Analysis

# Training Proactive and Personalized LLM Agents
2025-11-04 · paper · Weiwei Sun, Xuhui Zhou, Weihua Du, Xingyao Wang, Sean Welleck et al. (8 total)
https://arxiv.org/pdf/2511.02208

---

### Motivation & Prior Limitations
Existing LLM agent research optimizes almost exclusively for task success rate, neglecting the quality of agent–user interaction in real-world deployment where users provide vague, underspecified instructions.
- Frontier models like GPT-5 achieve strong productivity scores but exhibit severely limited proactivity and personalization, meaning they fail to ask clarifying questions strategically and do not adapt to user communication preferences.
  - On SWE-Bench with vague prompts, GPT-5 scores only 36.60 on proactivity and 12.96 on personalization despite a 55.83 productivity score; similarly, GPT-4.1 scores only 11.35 on proactivity.
- There is no scalable training environment for agent–user interaction: collecting supervision from real human users is time-consuming and infeasible, creating a bottleneck for developing interaction-aware agents.
  - Existing related environments (SWEET-RL, CollabLLM, UserRL) either ignore user persona diversity, ignore interaction costs, or treat users purely as information providers without modeling personalization.
- When user prompts are vague and the agent has no interaction training, there is a substantial performance drop (F1 from 64.50 to 44.11 on SWE-Func-Loc), and naive RL on task reward alone causes proactivity and personalization to actively degrade over training.

---

### Proposed Approach
The paper introduces USERVILLE, an interactive simulation environment, and PPP (Productive, Proactive, and Personalized), a multi-objective RL framework that jointly optimizes agents across all three dimensions of effective interaction.

- USERVILLE converts existing agent benchmarks into interactive training environments through three pipeline stages: (i) prompt vaguenization — an LLM rewrites precise task specifications into underspecified prompts preserving original intent; (ii) preference-aware user simulation — LLM-based user simulators are parameterized by 20 configurable interaction preferences (e.g., multiple-choice only, Italian language only, JSON-wrapped responses, one question per turn); (iii) user-centric evaluation — each agent question is classified by user effort as low-, medium-, or high-effort, and preference adherence is scored per-trajectory.
  - The information asymmetry between the precise prompt (held by the simulator) and the vague prompt (given to the agent) enables the simulator to answer clarifying questions as a real user would, grounding learning signals in realistic conditions.
  - 12 preferences are used for training and 8 are reserved as unseen test preferences to measure generalization.

- PPP employs GRPO-based RL (with Clip-Higher strategy and Token-Level Policy Gradient Loss from DAPO) with a composite reward: R = R_Prod + R_Proact + R_Pers, where R_Proact penalizes medium-effort queries (−0.1 each) and high-effort queries (−0.5 each) while rewarding low-effort-only sessions (+0.05), and R_Pers rewards full preference compliance (+0.05) and penalizes violations using per-preference rule-based or LLM-as-judge reward functions.
  - The agent is modeled as a multi-turn ReAct-style tool-call agent where `ask_user` is treated as a tool alongside task-oriented tools, making interaction a first-class agent action.
  - Training uses Seed-OSS-36B-Instruct as the base model with GPT-5-Nano as the user simulator, with a 13× data repetition scheme (12 vague-preference + 1 precise per instance).

---

### Results & Capabilities
PPP achieves a +16.72 average score improvement over Seed-OSS-36B-Instruct and outperforms GPT-5 by +21.6 on average across productivity, proactivity, and personalization on SWE-Bench-Verified and BrowseComp-Plus with vague prompts.

- On SWE-Func-Loc, PPP raises productivity from 38.59 to 56.26 (+17.67), proactivity from 43.70 to 75.55 (+31.85), and personalization from 69.07 to 89.26 (+20.19) relative to the base model.
  - Agent–user interaction with RL training closes the vague-prompt performance gap: F1 rises from 44.11 (vague, no interaction) to over 60, while the base model without interaction training shows no improvement from having access to clarification.

- PPP-trained agents learn to distinguish precise from vague prompts, asking questions in 100% of vague-prompt SWE instances and 85% of BrowseComp-Plus instances, but maintaining a low ask ratio on precise prompts — demonstrating minimally-disruptive behavior.
  - The agent's interaction dynamics follow an increase-then-decrease pattern during training: medium-effort questions first rise then fall, while low-effort questions steadily increase, indicating the model learns to ask better targeted questions over time rather than just more questions.

- Personalization generalizes robustly to all 8 unseen preference types, with scores consistently improving throughout training; in contrast, training without R_Pers causes scores on unseen preferences like JSON_Format to collapse from 1.00 to 0.30.

- The model trained on SWE-Func-Loc transfers to SWE-Full: task success rate improves from 0.29 to ~0.36, and question-asking behavior transfers — interaction count increases from ~0.10 to 1.8 per session, with high-effort questions remaining low.

- PPP is robust to user simulator substitution: replacing the GPT-5-Nano training simulator with GPT-5, GPT-4o, GPT-4.1, or GPT-5-Mini at test time produces only small performance variance, confirming that the trained interaction policy is not overfit to a single simulator.

---

### Implications
This work reframes the agent development problem: task success rate alone is an insufficient optimization target for real-world deployment, and interaction quality (proactivity, personalization) must be treated as a first-class training objective alongside productivity.

- The USERVILLE framework demonstra

## Key Claims

1. Existing LLM agent work primarily optimizes for task success alone, neglecting systematic optimization of agent-user interaction quality such as proactivity and personalization.
2. Frontier LLMs like GPT-5 achieve high productivity scores but exhibit clear limitations in proactivity and personalization.
3. Agent-user interaction dramatically improves task success when users provide vague instructions, with F1 score increasing from 44.11 to 64.50 on SWE-Func-Loc.
4. Agents trained with PPP achieve +21.6 average score improvement over GPT-5 across all evaluation dimensions.
5. Without RL training, base models do not improve task performance even when agent-user interaction is allowed, due to poor interaction strategy.
6. Training with only task success reward causes degradation in proactivity and personalization metrics as training progresses.
7. PPP-trained agents learn to distinguish between precise and vague prompts, asking clarifying questions only when necessary, exhibiting an increase-then-decrease learning dynamic in question quality.
8. The PPP approach generalizes to unseen user preferences, different user simulators, and more complex downstream tasks.
9. There is a significant performance drop when user prompts are vague compared to precise under a no-interaction setting (F1 44.11 vs 64.50 on SWE-Func-Loc).
10. Existing agent RL work treats the user merely as an information provider with task-oriented objectives, neglecting user-centric objectives like interaction satisfaction and personalization.

## Capabilities

- Multi-objective RL (PPP framework) jointly trains LLM agents for productivity (task success), proactivity (strategic clarifying questions), and personalization (user preference adaptation) simultaneously, achieving +16.72 average score improvement over GPT-5 on SWE-bench and BrowseComp+ under vague 
- RL-trained agents can discriminately distinguish precise from vague user prompts and modulate clarifying question behaviour accordingly — asking in nearly 100% of vague-prompt SWE instances while remaining minimally disruptive on precise prompts
- LLM-based preference-aware user simulators with 20 configurable interaction styles can serve as RL training signal generators for agent-user interaction, enabling trained agents to generalise to 8 unseen preferences not present during training
- Interaction-quality RL training transfers from subtask (issue localisation, SWE-Func-Loc) to full task (SWE-Full): task success rate rises from 0.29 to 0.36 and interaction count increases more than tenfold, with low-effort question ratio exceeding that of the source task
- USERVILLE automatically converts existing agent benchmarks (SWE-bench, BrowseComp) into interactive training environments with vague-prompt generation and preference-aware user simulation, removing the need for human annotators to produce agent-user interaction training data

## Limitations

- Frontier LLMs (GPT-5, GPT-5-Mini, GPT-4.1) achieve extremely poor personalization without explicit training — GPT-5 scores only 12.96% personalization on SWE-Func-Loc, demonstrating that scale and standard RLHF do not automatically confer user preference adaptation
- Optimising RL agents for task success alone causes measurable degradation in proactivity and personalization over training steps — the two families of objective are in active tension without explicit multi-objective treatment
- PPP RL training on vague-prompt tasks causes regression on precise-prompt performance — SWE-Full success rate drops from 0.558 to ~0.530 on original SWE-Bench (precise prompts), indicating a fundamental tension between interaction-optimised and task-optimised behaviour
- User simulators are LLM-based rather than real humans, leaving the real-world validity of learned interaction strategies unvalidated — whether agents trained on LLM simulators generalise to actual human users with inconsistent, emotionally variable behaviour remains unproven
- The 20 user preferences used are manually designed by researchers, severely undersampling real-world preference diversity — no evidence that these cover the empirical distribution of actual user interaction styles
- Without a proactivity penalty, RL-trained agents become structurally 'lazy' — they progressively offload cognitive work to users by asking high-effort questions requiring users to read documentation or explore codebases, increasing user burden while decreasing agent autonomy
- Personalization score does not correlate with model capability or recency — GPT-4.1 substantially outperforms GPT-5 on personalization (53.04 vs 12.96 on SWE-Func-Loc), suggesting personalization is not an emergent property of scale or general RLHF quality
- Multi-objective RL creates Pareto-frontier trade-offs between dimensions — agents optimising jointly for proactivity and personalization score slightly lower on each than single-objective ablations, confirming inherent gradient conflict between interaction objectives
- Evaluation is confined to text-based verifiable tasks (SWE-bench, BrowseComp+) — no evidence for effectiveness in embodied tasks, open-ended dialogue, or domains without ground-truth answers where productivity reward cannot be computed
- RL training infrastructure requirements are substantial — 36B parameter base model, Docker environments for SWE-Full, output lengths up to 65K tokens, batch size 64, making the approach inaccessible to resource-constrained teams
- Base models without RL training cannot leverage clarification opportunities even when given the ability to ask — on vague prompts with interaction enabled, the base model shows no improvement over no-interaction, only RL training makes clarification useful

## Bottlenecks

- Absence of scalable training environments for agent-user interaction blocks RL training on interaction quality — real human data collection is infeasible at the volume required for RL convergence, and there was no automated alternative before USERVILLE
- Dominant RL training paradigm optimises for task success alone, blocking development of agents that are practically usable with real users who issue underspecified, preference-laden requests
- User simulator validity gap — LLM-based simulators may not faithfully represent real human interaction patterns, blocking confident deployment of simulator-trained agents without costly real-user validation studies
- Manually designed user preference taxonomies cannot cover the real-world distribution of user interaction styles — preference learning from actual interaction data is necessary but absent, capping generalisation ceiling

## Breakthroughs

- Multi-objective RL (PPP) demonstrates that proactivity and personalization are explicitly trainable properties of LLM agents, not emergent byproducts of capability — achieving +16.72 average score over GPT-5 while proving each objective component is independently necessary
- RL training with a proactivity reward causes agents to learn vagueness-conditional question-asking behaviour spontaneously — the increase-then-decrease learning dynamic reveals that agents first explore broad question strategies before converging to targeted, low-effort queries

## Themes

- [[themes/agent_systems|agent_systems]]
- [[themes/policy_optimization|policy_optimization]]
- [[themes/reinforcement_learning|reinforcement_learning]]
- [[themes/reward_modeling|reward_modeling]]
- [[themes/rl_for_llm_reasoning|rl_for_llm_reasoning]]
- [[themes/software_engineering_agents|software_engineering_agents]]

## Key Concepts

- [[entities/grpo|GRPO]]
